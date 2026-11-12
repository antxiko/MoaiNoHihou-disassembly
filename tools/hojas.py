#!/usr/bin/env python3
"""Los sprites de Moai no Hihou MONTADOS DESDE LA ROM (ninguna imagen es una captura).

Los dibujos son los 0x800 bytes de 0x5800 que `sprites_dibujos` (0xAE17) pone tal cual en 0x3800; sprites de 16 x 16.
El protagonista son dos sprites en 0xE100 y 0xE110 (16 bytes cada uno; los 4 primeros, sus atributos), y los objetos
del mapa, doce huecos de 16 bytes desde 0xE120 (+4, el tipo con el bit 7).

  protagonista.png   dos sprites en el mismo sitio: el dibujo en blanco y el + 4 en rojo. Mirando a la derecha: de pie
                     0x00, andando 0x00 y 0x08 cada 4 cuadros (`prota_paso`, 0xA612), saltando 0x20 (`salto`, 0xA879) y
                     golpeando 0x08 y 0x30 (la tabla 0xA5F2); a la izquierda, + 0x10 de pie y andando (`prota_quieto`
                     0x9E85) y + 8 saltando y golpeando; esperando, 0x58 y despues 0x50 (0x9E76); muriendo, 0x40 y 0x48
                     (la tabla 0x8A91, cada 8 cuadros)
  objetos.png        los diez tipos: el 1 (`andarin`, 0x80, cian: + 8 a la izquierda y + 4 el paso cada 16 cuadros,
                     `dibujo_lado` 0x9983), el 2 (`rodador`, 0x98), el 3 (`volador`, 0xA8), el 4 (0xC8, rojo), el 5
                     (`laberinto`, 0xE0), el 6 (`rodante`, 0xEC), el 8 (`parpadea`, 0xA8 en blanco y azul claro, 0x9972),
                     el 9 (`recto`, 0xEC) y el 10 (`giros`, 0xE0), los que cambian de dibujo por tres de cuatro en cuatro
                     (`dibujo_anima`, 0x999F); y el 7, la explosion (0xF8 + 4 cada 16 cuadros)
  andar_cuadros.gif  el protagonista andando, golpeando y muriendo, y los objetos, al ritmo del juego

Uso: hojas.py docs/imagenes | hojas.py cotejo
"""
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "tools"))
import vdp          # noqa: E402

ORG = 0x4000
ROM = open(os.path.join(RAIZ, "moai.rom"), "rb").read()
FONDO = (40, 40, 56)
DERECHA = [0x00, 0x08, 0x20, 0x30]
IZQUIERDA = [0x10, 0x18, 0x28, 0x38]
OTROS = [0x58, 0x50, 0x40, 0x48]
# (tipo, primer dibujo, cuantos, colores)
OBJETOS = [(1, 0x80, 4, (7,)), (2, 0x98, 1, (15,)), (3, 0xA8, 3, (15,)), (4, 0xC8, 3, (8,)), (5, 0xE0, 3, (8, 5, 15)),
           (6, 0xEC, 3, (15,)), (8, 0xA8, 3, (15, 5)), (9, 0xEC, 3, (15, 5)), (10, 0xE0, 3, (15, 5)),
           (7, 0xF8, 2, (15, 5))]


def b(a):
    return ROM[a - ORG]


def patrones():
    return ROM[0x5800 - ORG:0x5800 - ORG + 0x800]


def pinta(im, pat, n, x, y, color, escala=1):
    if color & 15 == 0:
        return
    n &= 0xFC
    d = pat[n * 8:n * 8 + 32]
    c = vdp.PALETA[color & 15]
    for fila in range(16):
        for col in range(16):
            if (d[fila + (16 if col >= 8 else 0)] >> (7 - (col & 7))) & 1:
                for ey in range(escala):
                    for ex in range(escala):
                        px, py = (x + col) * escala + ex, (y + fila) * escala + ey
                        if 0 <= px < im.width and 0 <= py < im.height:
                            im.putpixel((px, py), c)


def prota(im, pat, d, x, y, E, c2=8):
    pinta(im, pat, d + 4, x, y, c2, E)
    pinta(im, pat, d, x, y, 15, E)


def dibujos(t):
    _, d, n, _ = t
    return [d + 4 * k for k in range(n)]


def hoja(Image):
    pat, E = patrones(), 4
    im = Image.new("RGB", (4 * 20 * E, 3 * 20 * E), FONDO)
    for fila, poses in enumerate((DERECHA, IZQUIERDA, OTROS)):
        for k, d in enumerate(poses):
            prota(im, pat, d, 2 + 20 * k, 2 + 20 * fila, E)
    return im


def hoja_objetos(Image):
    pat, E = patrones(), 3
    im = Image.new("RGB", (5 * 80 * E, 2 * 24 * E), FONDO)
    for k, t in enumerate(OBJETOS):
        x, y = 2 + 80 * (k % 5), 4 + 24 * (k // 5)
        for j, d in enumerate(dibujos(t)):
            pinta(im, pat, d, x + 18 * j, y, t[3][0], E)
    return im


def anima(Image):
    pat, E, cuadros = patrones(), 4, []
    for n in range(32):                                    # andando: 0 u 8 cada 4 cuadros
        im = Image.new("RGB", (60 * E, 20 * E), FONDO)
        prota(im, pat, 8 if n & 4 else 0, 2, 2, E)
        cuadros.append(im)
    for n in range(18):                                    # golpeando: la tabla 0xA5F2, un paso cada 2 cuadros
        im = Image.new("RGB", (60 * E, 20 * E), FONDO)
        prota(im, pat, b(0xA5F2 + n // 2), 2, 2, E)
        cuadros.append(im)
    for n in range(9 * 8):                                 # muriendo: la tabla 0x8A91, un dibujo cada 8 cuadros
        im = Image.new("RGB", (60 * E, 20 * E), FONDO)
        prota(im, pat, b(0x8A91 + n // 8), 2, 2, E)
        cuadros.append(im)
    out = []
    for k, im in enumerate(cuadros):                       # y los objetos al lado, cambiando de dibujo
        for j, t in enumerate((OBJETOS[2], OBJETOS[5])):
            pinta(im, pat, dibujos(t)[(k // 10) % 3], 20 + 20 * j, 2, t[3][0], E)
        out.append(im)
    return out


def guarda_gif(cuadros, ruta, ms=1000 / 60):
    imgs, durs = [], []
    for im in cuadros:
        if imgs and list(im.getdata()) == list(imgs[-1].getdata()):
            durs[-1] += ms
        else:
            imgs.append(im)
            durs.append(ms)
    imgs[0].save(ruta, save_all=True, append_images=imgs[1:], duration=[max(20, int(round(d))) for d in durs],
                 loop=0, disposal=1)


def cotejo():
    """Contra las grabaciones de openMSX (work/*.bin, la RAM 0xE000-0xEFFF):
    1) la tabla de dibujos de los sprites (VRAM 0x3800-0x3FFF) contra los 0x800 bytes de 0x5800;
    2) el protagonista (0xE100 y 0xE110): en el mismo sitio, el dibujo en blanco y el + 4 en rojo (o en los colores
       de cruzar la pantalla, 9 y 10); uno de sus dibujos;
    3) los objetos (12 huecos de 16 bytes desde 0xE120; el tipo en +4 con el bit 7): un dibujo de su tipo y su color."""
    pat = patrones()
    poses = set(DERECHA + IZQUIERDA + OTROS)
    tipos = {}
    for t in OBJETOS:
        ds = set(dibujos(t)) | ({0x88, 0x8C} if t[0] == 1 else set())
        tipos[t[0]] = (ds, set(t[3]))
    tot = dict(patrones=0, pat_carga=0, pat_mal=0, prota=0, prota_sin_poner=0, prota_mal=0, objetos=0, objetos_mal=0)
    for grab in ("atraccion", "partida", "forzada", "invencible", "selector", "teclas"):
        ruta = os.path.join(RAIZ, "work", grab + ".bin")
        if not os.path.exists(ruta):
            continue
        try:
            cuadros = list(vdp.cuadros(ruta))
        except AssertionError:
            continue
        for c in cuadros:
            v, ram = c["vram"], c["ram"]
            t = v[0x3800:0x4000]
            if any(t):
                n = len(t.rstrip(bytes(1)))
                if t == pat:
                    tot["patrones"] += 1
                elif t[:n] == pat[:n]:
                    tot["pat_carga"] += 1
                else:
                    tot["pat_mal"] += 1
            a, s = ram[0x100:0x104], ram[0x110:0x114]
            if a[0] < 0xC0:
                if a[3] & 15 == 0 and s[3] & 15 in (0, 8):
                    tot["prota_sin_poner"] += 1     # sin color: aun sin poner, o fuera de la vista al mirar
                elif a[:2] == s[:2] and a[2] in poses and s[2] == a[2] + 4 and s[3] & 15 in (8, 9, 10):
                    tot["prota"] += 1
                else:
                    tot["prota_mal"] += 1
            for k in range(12):
                e = ram[0x120 + 16 * k:0x130 + 16 * k]
                tipo = e[4] & 0x7F
                if e[0] >= 0xC0 or not e[4] & 0x80 or tipo not in tipos or e[3] & 15 == 0:
                    continue
                ds, cs = tipos[tipo]
                ok = e[2] in ds and e[3] & 15 in cs
                tot["objetos"] += ok
                tot["objetos_mal"] += not ok
    return tot


def main(argv):
    if argv and argv[0] == "cotejo":
        print(cotejo())
        return 0
    from PIL import Image
    salida = argv[0]
    os.makedirs(salida, exist_ok=True)
    hoja(Image).save(os.path.join(salida, "protagonista.png"))
    hoja_objetos(Image).save(os.path.join(salida, "objetos.png"))
    guarda_gif(anima(Image), os.path.join(salida, "andar_cuadros.gif"))
    for f in ("protagonista.png", "objetos.png", "andar_cuadros.gif"):
        print(f, os.path.getsize(os.path.join(salida, f)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
