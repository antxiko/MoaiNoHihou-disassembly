#!/usr/bin/env python3
"""EL CONTENIDO de la web de esta ROM: lo unico que es de este juego.

jekyll.py y make_web.py son la maquinaria y no llevan dentro el nombre de
ningun juego: lo leen de aqui.

Todas las cifras de aqui estan medidas sobre esta ROM, con las herramientas
de tools/: CODIGO y DATOS los imprime tools/presupuesto.py (make sanity),
INSTRUCCIONES, COMENTARIOS y RUTINAS los da tools/densidad.py (make densidad:
"de N" rutinas, "N instrucciones, M comentarios").
"""

NOMBRE = "Moai no Hihou"
EDITOR = "Casio"
ANIO = 1986
REPOSITORIO = "https://github.com/antxiko/MoaiNoHihou-disassembly"
SHA1 = "f924d89a28966a1d08c10d5ddbc9e0e182be4669"

CODIGO = 11848
DATOS = 20920
RUTINAS = 695
INSTRUCCIONES = 5558
COMENTARIOS = 2341


def densidad(idioma):
    """El porcentaje comentado, con la coma o el punto de cada idioma."""
    d = "%.1f" % (100.0 * COMENTARIOS / INSTRUCCIONES)
    return d.replace(".", ",") if idioma == "es" else d


PIE_LEGAL = {
    "es": "<em>Moai no Hihou</em> es un juego de Casio para MSX, de 1986, en un cartucho de 32 KB. Todos los "
          "derechos sobre el juego siguen siendo de sus titulares. Este trabajo es de preservaci&oacute;n, estudio "
          "y documentaci&oacute;n, y la imagen de la ROM no se distribuye.",
    "en": "<em>Moai no Hihou</em> is a 1986 Casio game for the MSX, on a 32 KB cartridge. All rights in the game "
          "remain with their holders. This is preservation, study and documentation work, and the ROM image is not "
          "distributed.",
}

PORTADA = {
    "es": dict(
        titulo="Moai no Hihou - desensamblado comentado",
        claim="Treinta y dos laberintos de rocas, uno por pantalla, con la salida arriba y un minuto o m&aacute;s "
              "de reloj: el protagonista rompe a golpes los bloques, que caen con lo que tienen encima, pone los "
              "suyos para subir y esquiva a los que andan, ruedan y vuelan; cada cuarta fase es un BONUS GAME. El "
              "t&iacute;tulo sale de ejecutar la ROM, cotejado con openMSX punto a punto; la partida en GIF, jugada "
              "en openMSX; las cinco m&uacute;sicas, de su propio motor, id&eacute;nticas a openMSX cuadro a cuadro.",
        ficha=["Casio - <b>(c) 1986</b>",
               "Cartucho de <b>32 KB</b> (cabecera en 0x4000)",
               "<b>MSX</b>", "Volcado <b>f924d89a...</b>"],
        aviso="<b>Aqu&iacute; no hay capturas del juego.</b> El t&iacute;tulo sale de ejecutar la ROM (cotejado "
              "con openMSX) y los GIF son la ROM <b>funcionando en openMSX</b>: en cada cuadro se apuntan la VRAM, "
              "la RAM y los registros del VDP, y <b>c&oacute;digo nuestro los pinta</b>.",
    ),
    "en": dict(
        titulo="Moai no Hihou - commented disassembly",
        claim="Thirty-two mazes of rock, one per screen, with the exit at the top and a minute or more on the "
              "clock: the hero breaks the blocks with blows, they fall with whatever sits on them, he lays his own "
              "to climb and dodges the ones that walk, roll and fly; every fourth stage is a BONUS GAME. The title "
              "comes from running the ROM, checked against openMSX point by point; the game in GIF, played in "
              "openMSX; the five tunes, from its own engine, identical to openMSX frame by frame.",
        ficha=["Casio - <b>(c) 1986</b>",
               "<b>32 KB</b> cartridge (header at 0x4000)",
               "<b>MSX</b>", "Dump <b>f924d89a...</b>"],
        aviso="<b>There are no screenshots of the game here.</b> The title comes from running the ROM (checked "
              "against openMSX) and the GIFs are the ROM <b>running in openMSX</b>: on every frame the VRAM, the "
              "RAM and the VDP registers are logged, and <b>our own code paints them</b>.",
    ),
}

PAGINAS = [
    [("THE-GAME.html", "LA-PARTIDA.html", "The game", "La partida",
      "the CASIO intro, the title, the controls, the blows and the blocks, the time, the lives and the points",
      "la presentaci&oacute;n de CASIO, el t&iacute;tulo, los mandos, los golpes y los bloques, el tiempo, las "
      "vidas y los puntos"),
     ("THE-STAGES.html", "LAS-FASES.html", "The stages", "Las fases",
      "the 32 mazes, the BONUS GAME, what can be picked up, the enemies and the ending with three moai",
      "los 32 laberintos, el BONUS GAME, lo que se coge, los enemigos y el final con tres moai"),
     ("THE-TEXTS.html", "LOS-TEXTOS.html", "The texts", "Los textos",
      "every text in the ROM, with its translation",
      "todos los textos de la ROM, con su traducci&oacute;n"),
     ("THE-MUSIC.html", "LA-MUSICA.html", "The music", "La m&uacute;sica",
      "the five tunes, from its own sound engine and checked against openMSX",
      "las cinco m&uacute;sicas, de su propio motor de sonido y cotejadas con openMSX")],
    [("CURIOSITIES.html", "CURIOSIDADES.html", "Curiosities", "Curiosidades",
      "the stage select, SELECT and ESC on the title, STOP to look around, a score that misses a text, unused texts",
      "el selector de fase, SELECT y ESC en el t&iacute;tulo, STOP para mirar, un marcador al que le falta un "
      "texto, textos sin usar")],
    [("UNDER-THE-HOOD.html", "POR-DENTRO.html", "Under the hood", "Por dentro",
      "rebuilding the ROM, the cartridge, the BIOS it uses, the main loop, the map, the RAM and the tools",
      "rehacer la ROM, el cartucho, la BIOS que usa, el bucle, el mapa, la RAM y las herramientas")],
]

# Repositorio nuevo: no hay paginas viejas que redirigir.
VIEJAS = {}

LOGOTIPO = "logotipo.png"
