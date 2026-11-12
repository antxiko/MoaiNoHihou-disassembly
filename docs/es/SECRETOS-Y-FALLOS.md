# Secretos y fallos

Lo que se ha buscado en el código y lo que se ha encontrado. Un fallo solo entra aquí si está comprobado:
ejecutando la propia rutina del juego (`tools/bios.py`) o contra las grabaciones de openMSX.

## Secretos

Todos contados, con su GIF, en [Curiosidades](CURIOSIDADES.html):

| qué | cuándo | lo que hace | comprobado |
|---|---|---|---|
| dos teclas (A o B con 0 o 5; Z-V con C-R) | al empezar (`fase_empieza`, 0x82FD) | se empieza en otra fase | en openMSX (B y 5: la fase 18) |
| SELECT | en el título | ni rocas, ni enemigos, ni el tiempo quitan vidas | en el código |
| ESC | en el título (0x80BC) | el récord a 5000 | en el código |
| STOP sostenida | jugando | el juego para y la palanca mueve la vista | en openMSX |
| F1 | jugando | una vida menos | en openMSX |

Fuera de esas teclas, los mandos se leen en la interrupción (0xAEBD-0xAF5E): la palanca de los cursores y del mando
1, los botones del mando 1, la barra y GRAPH.

## Fallo: los puntos de un enemigo aplastado

Una roca que cae encima de un enemigo le da sus puntos de la tabla de 0x99F3 (500, 300, 300, 100, 100 y 100), pero
`aplastado_objeto` (0x99CE) lee la tabla con el tipo tal como está, con el bit 7 puesto (todas las rutinas de los
enemigos lo ponen al arrancar), y lee 128 bytes más allá, en medio del código. Ejecutando aquí la suma de puntos del
juego con lo que lee para cada tipo:

| enemigo | lee el byte | suma |
|---|---|---|
| tipo 1, el que anda | 0x7E (0x9A74) | **8.400** |
| tipo 2, el que rueda | 0x01 (0x9A75) | 100 |
| tipo 3, el que vuela | 0xFE (0x9A76) | **16.400** |
| tipo 4 | 0xB9 (0x9A77) | **11.900** |
| tipo 5, el del laberinto | 0x30 (0x9A78) | **3.000** |
| tipo 6, el que va y vuelve | 0x05 (0x9A79) | 500 |

Los bytes que no son BCD (0x7E, 0xFE, 0xB9) se suman igual a las centenas y `daa` los arregla a su manera. En las
grabaciones de esta web ningún enemigo murió aplastado: estos números salen de ejecutar la rutina, no de verlos en la
pantalla.

## Fallo: los puntos sin tope

`puntos_suma_pinta` (0xAABA) suma en BCD hasta el byte de arriba (0xE034), y allí el acarreo se pierde. Ejecutándolo
aquí, 999.990 + 10 da **000000**, igual que 999.900 + 100. El récord se queda con lo que tenía.

## Fallo: los cursores y el mando se suman

La palanca (0xAF1A) **suma** los números de dirección de los cursores y del mando 1 (0xAF2A). Con los dos a la vez,
ejecutándolo aquí: derecha y abajo dan **arriba-izquierda** (8), y arriba y abajo, **abajo-izquierda** (6).

## Otras cosas, contadas en [Curiosidades](CURIOSIDADES.html)

- **Al marcador le falta un texto**: un `ld hl` donde iba un `ld de` (0x92AB), y los puntos salen sin el 0 de detrás.
- **Textos sin usar**: GOOD LUCK TO NEXT STAGE, FLOOR y PUSH TR1 TO START.
