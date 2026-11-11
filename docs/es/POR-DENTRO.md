# Por dentro

## Rehacer la ROM

`make verify` ensambla `src/moai.asm` con pasmo y sale la ROM de 32 KB **byte a byte**. `make sanity` comprueba lo
que el reensamblado no cubre: que ningún byte declarado como datos se lea como código, que ningún punto de entrada
caiga en datos y que estén explicados los 32.768 bytes. `make test` pasa los tests. La ROM no está en el repositorio:
hay que ponerla en la raíz como `moai.rom` (el volcado de GoodMSX, `[!]`, sha1 `f924d89a...`).

| | bytes |
|---|---|
| código trazado | 11.848 |
| datos con nombre | 20.920 |
| sin explicar | 0 |

El listado tiene 2.341 comentarios en 5.558 instrucciones (42,1 %), 695 rutinas y etiquetas, ninguna por debajo del
10 % comentada, y ninguna rutina llamada sin nombre.

## El cartucho

32 KB en 0x4000-0xBFFF, con la cabecera en 0x4000. INIT (0x4010) pone el cartucho también en la página 2 y salta a
0x8010. Los datos van delante: los límites de la vista al mirar (0x40EB), el montón de joyas del final (0x412B), los
textos del título (0x419B), los mapas de las fases (0x41D6-0x4E1A), las listas de lo que trae cada mapa (0x4E1B), las
32 fases (0x5078, 8 bytes cada una), el dibujo de la pantalla del premio (0x51BE), el nombre del título (0x543D), la
lista de mandos de la demostración (0x5700), los dibujos de los sprites (0x5800) y las casillas con sus colores
(0x6000-0x7FFF). El código va de 0x8010 a 0xB015; detrás, los mapas de cuatro fases que no cupieron delante (0xB016) y
el sonido (0xB300-0xBFFF).

## La BIOS que usa

RSLREG y ENASLT para el slot; SETGRP, CHGCLR, WRTVDP, DISSCR y ENASCR; FILVRM, LDIRVM, WRTVRM y RDVRM, que lee la
pantalla para saber qué casilla hay en cada sitio; GTSTCK y GTTRIG para los mandos y SNSMAT para la barra, GRAPH,
STOP, F1, SELECT, ESC y el selector de fase; WRTPSG para el sonido. Las letras son del cartucho.

## La interrupción y el bucle

INIT pone un salto a 0xAE9A en el gancho H.TIMI. La interrupción hace el silencio pedido, cuenta cuadros (dieciséis
cuentas, 0xE010-0xE01F), hace el sonido, lee F1, STOP, los botones, la barra, GRAPH y la palanca; en la
demostración, lee un byte de su lista cada 16 cuadros (`interrupcion`, 0xAE9A). El juego va en el **bucle de la
fase** (`fase_bucle`, 0x8656): una vez por cuadro, el protagonista, lo que cae, lo que se rompe, su marca en el
marcador, el tiempo, los enemigos, las cosas del mapa, los colores, el récord, los puntos y si le ha caído una roca
encima; después, STOP, el sonido de fondo, tocado, F1 y la fase acabada.

**El mapa.** Cada fase se monta en la RAM (0xE800, filas de 16 bytes: 12 bloques y lo que trae la fila) y se pinta
de ahí; un bloque son 2 x 2 casillas (la tabla de 0x8E82). Las rocas son piezas con forma: cada forma dice por qué
lados se une a las de al lado (`unido_arriba`, 0xA0CF, y las tres siguientes), y el golpe rompe la pieza y las que
están unidas a ella. Lo que queda sin nada debajo cae (`caen`). Las tablas de 0xA14B pasan de la pantalla al mapa y
al revés, según la vista (0xE308).

**Las casillas se leen de la pantalla.** Para saber si el protagonista o un enemigo puede pasar, si pisa algo o si
le ha caído una roca, el juego no mira el mapa: lee la tabla de nombres de la VRAM con RDVRM (`casillas_fila`,
0xA9AA; `aplastado`, 0x8AEA).

## Cómo se hizo

El trazado sigue el código desde INIT, la interrupción y la tabla de saltos de los enemigos (0x931E), declarados en
`src/moai.entries`. El resto se **midió en openMSX** (`tools/omsx_cobertura.tcl`) en un Philips VG 8020, esperando
la demostración y jugando: nada de lo que corrió se quedó fuera del trazado.

Las grabaciones de la web (`tools/guiones/*.tcl`, grabadas con `tools/lanza_graba.ps1` en C-BIOS) apuntan, en cada
cuadro, los registros del VDP, la RAM desde 0xE000, el PSG y la VRAM que cambió. `tools/pantallas.py` ejecuta el
título con `tools/bios.py` y lo coteja con la grabación (**0 puntos distintos**), `tools/gifs.py` hace los GIF y
`tools/musica.py` ejecuta el motor de sonido.

## La RAM

| | |
|---|---|
| 0xE000 | jugando |
| 0xE00A / 0xE00B | la fase (0-31) / las vidas |
| 0xE010-0xE01F | las cuentas de cuadros |
| 0xE020-0xE02D | los botones: recién pulsados y sostenidos |
| 0xE023 / 0xE039 | SELECT / ESC en el título |
| 0xE027 / 0xE037 | la demostración / su lista de mandos |
| 0xE031-0xE033 | el récord (BCD) |
| 0xE034-0xE036 | los puntos (BCD) |
| 0xE03A | la fase acabada (la salida) |
| 0xE100 | el protagonista (dos sprites) |
| 0xE120 | los cinco enemigos (16 bytes cada uno) |
| 0xE170 | la marca del protagonista en el marcador |
| 0xE180 | la palanca |
| 0xE183 | tocado |
| 0xE1B3 / 0xE1B5 | F1 / STOP |
| 0xE280-0xE2D5 | el sonido: los tres canales y los pedidos |
| 0xE308 | la vista |
| 0xE30C / 0xE30D / 0xE30E / 0xE30F | lo que protege de los tipos 3 y 6 / las joyas / los bloques / lo que protege de los tipos 1, 2 y 5 |
| 0xE31F / 0xE320 | el tiempo: minutos / segundos (BCD) |
| 0xE321 / 0xE322 | los puntos que se suman |
| 0xE326 | mirando (STOP) |
| 0xE331 | el marco de mirar (siete sprites) |
| 0xE600 | lo que se rompe y lo que cae |
| 0xE700 | el título, en la RAM |
| 0xE800 | el mapa de la fase |
