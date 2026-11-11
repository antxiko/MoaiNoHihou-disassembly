# La música

Cinco músicas, a tres voces. No son grabaciones hechas a mano: `tools/musica.py` **ejecuta el propio motor de sonido
de la ROM** con `tools/z80run.py` -la rutina del sonido (`sonido`, 0xB376), cuadro a cuadro, con el número que escribe
el juego- y apunta lo que escribe en el PSG por la BIOS (WRTPSG).

**Cotejadas con openMSX**: los registros de tono y volumen de los tres canales casan con los grabados, **0 distintos**
en todos los cuadros mirados, en las cinco. Se cotejan seis grabaciones (`tools/guiones/`): el título con la
demostración, una partida hasta GAME OVER, una con SELECT, una con las teclas, una con el selector de fase y el
recorrido forzado por las 32 fases. Cada cuadro grabado se empareja con el cuadro del motor que tiene la misma RAM en
los tres canales; mientras suena un efecto en un canal, ese canal no se mira. La del final se mira la primera vez que
suena: después el juego la vuelve a pedir una y otra vez.

## El motor

El motor está al final del cartucho, con una tabla de saltos en 0xB300: pedir un efecto del canal A, uno de B y C,
una música, el sonido de un cuadro, el registro 7 del PSG y el silencio. Va una vez por cuadro desde la interrupción
y recibe tres **pedidos**: una música (0xE2BE), un efecto para el canal A (0xE2C0) y otro para B y C (0xE2C2); gana el
de número menor (`musica_pide`, 0xB371). Las tablas: seis músicas en 0xB312 (la 0, nada), seis efectos del canal A en
0xB336, cuatro de B y C en 0xB342 y catorce duraciones en 0xB627.

Durante la fase no suena música: el sonido de fondo es un **efecto** de los canales B y C (el 3; el 2 en el BONUS
GAME), que el bucle de la fase pide en cada vuelta.

| | Quién la pide | Dura |
|---|---|---:|
| la presentación de CASIO | los CASIO se juntan (0xAC31) | 1,1 s |
| la fase | al empezar la fase (0x8602) | 6,0 s |
| la fase acabada | el protagonista cruza la pantalla del premio (0x8C25) | 11,3 s |
| el final | el final, una y otra vez (0x8C61, 0x8CAB) | 9,8 s |
| GAME OVER | sin vidas (0x8A7E) | 7,6 s |

Ninguna vuelve a empezar sola: todas acaban.

## La presentación de CASIO

<audio controls src="../audio/musica_casio.mp3"></audio>

## La fase

<audio controls src="../audio/musica_fase.mp3"></audio>

## La fase acabada

<audio controls src="../audio/musica_fase_acabada.mp3"></audio>

## El final

<audio controls src="../audio/musica_final.mp3"></audio>

## GAME OVER

<audio controls src="../audio/musica_game_over.mp3"></audio>
