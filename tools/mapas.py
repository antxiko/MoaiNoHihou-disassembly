"""Los mapas de las 32 fases de Moai, PINTADOS EJECUTANDO LA ROM: fase_monta (0x849D) hasta despues de fase_cosas
(0x8503): las casillas de la fase en la VRAM, su mapa en la RAM (0xE800, filas de 16 bloques, 12 usados) y lo que se
coge puesto en el mapa (los dibujos y colores de las casillas, de un cuadro grabado de la fase: los carga el juego
fuera de fase_monta); despues mapa_pinta (0x8D7B), que pinta 11 filas de bloques de 2 x 2 casillas desde el
puntero 0xE319, de 11 en 11 filas hasta el final. Sin marcador ni sprites (los enemigos y los objetos con sprite).
Cuatro PNG, ocho fases cada uno, de arriba abajo.

Cotejo: en work/forzada.bin, cada cuadro de juego con la vista quieta tiene en 0xE369 el puntero de la fila de arriba
de la pantalla: la tabla de nombres grabada (filas 1-22, columnas 1-24) contra lo montado desde esa fila.

Uso: mapas.py docs/imagenes
"""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import vdp                  # noqa: E402
from bios import Msx        # noqa: E402
from PIL import Image       # noqa: E402

RAIZ = os.path.dirname(AQUI)
ROM = open(os.path.join(RAIZ, "moai.rom"), "rb").read()
ANCHO = 24                  # 12 bloques de 2 casillas
REGS = bytes.fromhex("02e206ff033607f0")    # los registros del VDP jugando (grabados): INIT no se ejecuta aqui


GRABADO = {}                # fase -> la VRAM de un cuadro grabado de esa fase (los dibujos y colores de sus casillas)


def grabados():
    if not GRABADO:
        for c in vdp.cuadros(os.path.join(RAIZ, "work", "forzada.bin")):
            r = c["ram"]
            if r[0x000] and c["regs"][1] & 0x40 and r[0x00A] < 32 and r[0x00A] not in GRABADO:
                GRABADO[r[0x00A]] = c["vram"]
    return GRABADO


def monta(fase):
    """fase_monta hasta despues de fase_cosas; los dibujos y colores de las casillas los carga el juego al empezar la
    partida y con fase_colores (0x864E), fuera de fase_monta: salen de un cuadro grabado de la fase."""
    m = Msx(ROM, 0x4000)
    v = grabados()[fase]
    m.vdp.vram[0x0000:0x1800] = v[0x0000:0x1800]
    m.vdp.vram[0x2000:0x3800] = v[0x2000:0x3800]
    m.mem[0xE00A] = fase
    m.sp = 0xF380
    m.hasta(0x849D, 0x8503)
    return m


def filas_de(m, desde):
    """Las 22 filas de casillas (24 columnas) que pinta mapa_pinta desde la fila de bloques `desde`."""
    base = bytes(m.vdp.vram[0x1800:0x1B00])
    for f in range(22):                 # los bloques 0 no se pintan: la zona del mapa, en blanco (la casilla 0x10)
        m.vdp.vram[0x1800 + 32 * (1 + f) + 1:0x1800 + 32 * (1 + f) + 1 + ANCHO] = bytes([0x10] * ANCHO)
    p = 0xE800 + 16 * desde
    m.mem[0xE319], m.mem[0xE31A] = p & 0xFF, p >> 8
    m.llama(0x8D7B)
    t = bytes(m.vdp.vram[0x1800:0x1B00])
    m.vdp.vram[0x1800:0x1B00] = base
    return [t[32 * (1 + f) + 1:32 * (1 + f) + 1 + ANCHO] for f in range(22)]


def fase_imagen(m):
    filas = [bytes(m.mem[0xE800 + 16 * i:0xE800 + 16 * i + 16]) for i in range(121)]
    usadas = [i for i, r in enumerate(filas) if any(r)]
    primera, ultima = usadas[0], usadas[-1]
    nombres = []
    k = primera
    while k <= ultima:
        nombres += filas_de(m, k)[:2 * min(11, ultima + 1 - k)]
        k += 11
    im = Image.new("RGB", (ANCHO * 8, len(nombres) * 8))
    v = bytearray(m.vdp.vram)
    for t in range(0, len(nombres), 22):
        trozo = nombres[t:t + 22]
        for f, fila in enumerate(trozo):
            v[0x1800 + 32 * (1 + f) + 1:0x1800 + 32 * (1 + f) + 1 + ANCHO] = fila
        regs = REGS
        pant = vdp.imagen(bytes(v), bytes(regs), 1, con_sprites=False)
        im.paste(pant.crop((8, 8, 8 + ANCHO * 8, 8 + 8 * len(trozo))), (0, 8 * t))
    return im, primera


def cotejo():
    """(fase) -> las casillas distintas de cada cuadro"""
    montados = {}
    out = {}
    for c in vdp.cuadros(os.path.join(RAIZ, "work", "forzada.bin")):
        r = c["ram"]
        if not (r[0x000] and c["regs"][1] & 0x40):
            continue
        f = r[0x00A]
        if f >= 32:
            continue
        p = r[0x369] | r[0x36A] << 8
        if not 0xE800 <= p < 0xEF90 or (p - 0xE800) % 16:
            continue
        if f not in montados:
            montados[f] = monta(f)
        m = montados[f]
        m.mem[0xE800:0xEF90] = r[0x800:0xF90]          # el mapa grabado, con lo ya cogido
        esperado = filas_de(m, (p - 0xE800) // 16)
        grab = [c["vram"][0x1800 + 32 * (1 + k) + 1:0x1800 + 32 * (1 + k) + 1 + ANCHO] for k in range(22)]
        d = sum(1 for a, b in zip(b"".join(esperado), b"".join(grab)) if a != b)
        out.setdefault(f, []).append(d)
    return out


def main(salida):
    imagenes = []
    for f in range(32):
        im, _ = fase_imagen(monta(f))
        imagenes.append(im)
        print("fase %2d: %d x %d" % (f, im.size[0], im.size[1]))
    for g in range(4):
        grupo = imagenes[8 * g:8 * g + 8]
        alto = max(i.size[1] for i in grupo)
        hoja = Image.new("RGB", (8 * (ANCHO * 8 + 8) - 8, alto), (0, 0, 0))
        for k, i in enumerate(grupo):
            hoja.paste(i, (k * (ANCHO * 8 + 8), 0))
        hoja = hoja.resize((hoja.size[0] // 2, hoja.size[1] // 2), Image.NEAREST)
        ruta = os.path.join(salida, "mapas_%d.png" % (g + 1))
        hoja.save(ruta, optimize=True)
        print(ruta, hoja.size)
    todos = []
    for f, ds in sorted(cotejo().items()):
        ds.sort()
        todos += ds
        print("cotejo fase %2d: %5d cuadros; iguales %5d, con 10 o menos distintas %5d; mediana %d" % (
            f, len(ds), ds.count(0), sum(1 for d in ds if d <= 10), ds[len(ds) // 2]))
    todos.sort()
    print("en total: %d cuadros, %d iguales, %d con 10 o menos casillas distintas de %d, mediana %d" % (
        len(todos), todos.count(0), sum(1 for d in todos if d <= 10), 22 * ANCHO, todos[len(todos) // 2]))


if __name__ == "__main__":
    main(sys.argv[1])
