# Los textos

Las letras son del cartucho (0x6680), en el mismo orden que la fuente de la BIOS: una letra es su código - 0x30, y la
casilla 0x10 es el espacio (`letras_pon`, 0xADBA). El nombre del juego y CASIO son casillas dibujadas.

| dirección | original | traducción | dónde sale |
|---|---|---|---|
| 0xAD1F | CASIO | Casio | la presentación, en casillas dibujadas |
| 0xAD3A | SOFTWARE | Software | la presentación |
| 0x419B | CASIO | Casio | el título, en casillas dibujadas |
| 0x543D | モアイの秘宝 | El tesoro de los moai | el título, en casillas dibujadas |
| 0x41B6 | COPYRIGHT 1986 © CASIO | Copyright 1986 Casio | el título |
| 0x41CC | GAME START | Empieza la partida | el título |
| 0x41A1 | PUSH TRIG1 OR SPACE | Pulsa el botón 1 o la barra | el título |
| 0x81A4 | STAFF | El equipo | los créditos, debajo del título |
| 0x81AC | K.ARISAWA, K.ASAHINA, K.SATOH, K.OKUYAMA, A.HASEGAWA, K.OHSAWA, J.ARCHER | (nombres) | los créditos |
| 0x81F1 | PRODUCER / T.MORIYAMA | Productor: T. Moriyama | los créditos, en dos filas |
| 0x92EC | HIGH | Récord | el marcador |
| 0x92D3 | SCORE | Puntos | el marcador |
| 0x92D9 | STAGE | Fase | el marcador |
| 0x92CE | TIME | Tiempo | el marcador |
| 0x8517 | BONUS | Bonus | el marcador, en el BONUS GAME |
| 0x8616 | P= | Vidas | el marcador |
| 0x8619 | PUSH TR1 TO START | Pulsa el botón 1 para empezar | **no sale** (ver abajo) |
| 0x847B | BONUS GAME | Fase de bonus | al empezar un BONUS GAME |
| 0x8D44 | YOU GET BONUS | Te llevas un premio | la fase acabada y el BONUS acabado |
| 0x8D52 | 1000× = 000PTS | 1000 × n = n000 puntos | la fase acabada |
| 0x8D3C | PJM1622 | (sin traducción) | el final |
| 0x8A87 | GAME OVER | Fin de la partida | sin vidas |
| 0x92DF | "     0" | (el 0 de detrás de los puntos) | **no sale** ([Curiosidades](CURIOSIDADES.html)) |
| 0x92E6 | FLOOR | Piso | **ningún puntero llega a él** |
| 0x8D63 | GOOD LUCK TO NEXT STAGE | Suerte en la fase siguiente | **ningún puntero llega a él** |

**PUSH TR1 TO START** va detrás de P= en el mismo texto, separado por un 0xFF: la rutina que lo escribe
(`texto_vram`, 0x92C3) para en el 0xFF, así que de los dos solo sale P=.

**PJM1622** sale en la esquina de arriba del final. No hemos encontrado qué significa.
