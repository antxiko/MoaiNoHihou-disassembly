"""Los GIF de la web: tramos de las grabaciones de openMSX (tools/guiones/*.tcl, grabados con
tools/lanza_graba.ps1 en C-BIOS_MSX1_JP, -bp 0xAE9A -ram "0xE000 0x1000"), pintados con tools/vdp.py; cada imagen
dura el tiempo emulado que dura en la grabacion.

Los tramos salen de la RAM grabada: 0xE000 jugando, 0xE027 la demostracion, 0xE00A la fase, 0xE00B las vidas,
0xE183 tocado, 0xE03A la fase acabada, 0xE1B5 STOP, 0xE1B3 F1, 0xE2BD la musica.

  atraccion   sin tocar nada: la presentacion de CASIO, el titulo con los creditos y la demostracion
  partida     un piloto sencillo (tools/guiones/partida.tcl): pierde las cinco vidas en la primera fase
  teclas      ESC en el titulo (el record a 5000), STOP sostenida con la palanca arriba y abajo, F1
  selector    la B y el 5 al empezar: la fase 18 (STAGE 15)
  forzada     el mismo piloto; cada fase se da por acabada con un poke (FORZADA): las 32 fases y el final

Las grabaciones son grandes: cada una se lee UNA vez.

Uso: gifs.py docs/imagenes
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vdp          # noqa: E402

# (fichero, grabacion, desde, hasta, cada)
TRAMOS = [
    ("presentacion.gif", "atraccion", 3, 205, 3),       # la presentacion de CASIO
    ("titulo.gif", "atraccion", 330, 1630, 4),          # el titulo y los creditos, que suben
    ("demostracion.gif", "atraccion", 1990, 3330, 3),   # la demostracion
    ("salida.gif", "partida", 400, 840, 2),             # la primera fase: la musica de salida y el piloto
    ("aplastado.gif", "partida", 840, 1000, 2),         # una roca le cae encima
    ("game_over.gif", "partida", 4050, 4553, 3),        # la ultima vida y GAME OVER
    ("mirar.gif", "teclas", 880, 1560, 3),              # STOP sostenida: el marco y la vista arriba y abajo
    ("f1.gif", "teclas", 1880, 2060, 2),                # F1: una vida menos
    ("selector.gif", "selector", 380, 600, 2),          # la B y el 5: la fase 18, STAGE 15
    ("premio.gif", "forzada", 2090, 2900, 3),           # la fase acabada: YOU GET BONUS y el cruce
    ("fase_2.gif", "forzada", 3300, 3700, 2),           # STAGE 2
    ("bonus.gif", "forzada", 7200, 7900, 2),            # el primer BONUS GAME
    ("bonus_cobra.gif", "forzada", 7850, 8560, 3),      # lo cogido en el BONUS
    ("fase_4.gif", "forzada", 9000, 9400, 2),           # STAGE 4
    ("fase_7.gif", "forzada", 16100, 16500, 2),         # STAGE 7
    ("fase_10.gif", "forzada", 23600, 24000, 2),        # STAGE 10
    ("fase_13.gif", "forzada", 30550, 30950, 2),        # STAGE 13
    ("fase_16.gif", "forzada", 37700, 38100, 2),        # STAGE 16
    ("fase_19.gif", "forzada", 45250, 45650, 2),        # STAGE 19
    ("final.gif", "forzada", 58060, 61100, 4),          # el final: los moai, las joyas y PJM1622
]


def main(salida):
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for grab in dict.fromkeys(t[1] for t in TRAMOS):
        mios = [t for t in TRAMOS if t[1] == grab]
        gifs = {t[0]: vdp.Gif() for t in mios}
        tope = max(t[3] for t in mios) + max(t[4] for t in mios)
        espera = {}                                    # fichero -> (imagen, t) pendiente de su duracion
        for n, c in enumerate(vdp.cuadros(os.path.join(raiz, "work", grab + ".bin"))):
            if n > tope:
                break
            for fichero, _, desde, hasta, cada in mios:
                if desde <= n <= hasta + cada and (n - desde) % cada == 0:
                    if fichero in espera:
                        im, t = espera.pop(fichero)
                        gifs[fichero].pon(im, (c["t"] - t) * 1000.0 / gifs[fichero].ms)
                    if n <= hasta:
                        espera[fichero] = (vdp.imagen(c["vram"], c["regs"], 1), c["t"])
        for fichero, _, desde, hasta, cada in mios:
            if fichero in espera:                       # la grabacion acaba antes: la ultima, un paso
                im, _t = espera.pop(fichero)
                gifs[fichero].pon(im, cada)
            ruta = os.path.join(salida, fichero)
            gifs[fichero].guarda(ruta, 4000)
            print("%-24s %4d imagenes, %8d bytes" % (fichero, len(gifs[fichero]), os.path.getsize(ruta)))


if __name__ == "__main__":
    main(sys.argv[1])
