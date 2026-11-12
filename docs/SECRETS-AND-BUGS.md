# Secrets and bugs

What was searched for in the code and what was found. A bug only goes here if it has been checked: by running the
game's own routine (`tools/bios.py`) or against the openMSX recordings.

## Secrets

All of them told, with their GIF, in [Curiosities](CURIOSITIES.html):

| what | when | what it does | checked |
|---|---|---|---|
| two keys (A or B with 0 or 5; Z-V with C-R) | at the start (`fase_empieza`, 0x82FD) | the game starts on another stage | in openMSX (B and 5: stage 18) |
| SELECT | on the title | neither rocks, enemies nor time take lives | in the code |
| ESC | on the title (0x80BC) | the high score set to 5000 | in the code |
| STOP held | while playing | the game stops and the stick moves the view | in openMSX |
| F1 | while playing | one life less | in openMSX |

Apart from those keys, the controls are read in the interrupt (0xAEBD-0xAF5E): the stick from the cursor keys and
joystick 1, the joystick 1 buttons, the space bar and GRAPH.

## Bug: the points for a crushed enemy

A rock falling on an enemy gives its points from the table at 0x99F3 (500, 300, 300, 100, 100 and 100), but
`aplastado_objeto` (0x99CE) reads the table with the type as it stands, with bit 7 set (every enemy routine sets it when
starting), and reads 128 bytes further on, in the middle of the code. Running the game's score addition here with what it
reads for each type:

| enemy | reads the byte | adds |
|---|---|---|
| type 1, the walker | 0x7E (0x9A74) | **8,400** |
| type 2, the roller | 0x01 (0x9A75) | 100 |
| type 3, the flyer | 0xFE (0x9A76) | **16,400** |
| type 4 | 0xB9 (0x9A77) | **11,900** |
| type 5, the maze one | 0x30 (0x9A78) | **3,000** |
| type 6, the one that goes back and forth | 0x05 (0x9A79) | 500 |

The bytes that are not BCD (0x7E, 0xFE, 0xB9) are added to the hundreds all the same and `daa` fixes them its own way.
In the recordings on this site no enemy was crushed: these numbers come from running the routine, not from seeing them
on screen.

## Bug: the score has no cap

`puntos_suma_pinta` (0xAABA) adds in BCD up to the top byte (0xE034), and there the carry is lost. Running it here,
999,990 + 10 gives **000000**, and so does 999,900 + 100. The high score keeps what it had.

## Bug: the cursor keys and the joystick are added

The stick (0xAF1A) **adds** the direction numbers of the cursor keys and joystick 1 (0xAF2A). With both at once, running
it here: right and down give **up-left** (8), and up and down, **down-left** (6).

## Other things, told in [Curiosities](CURIOSITIES.html)

- **The scoreboard misses a text**: an `ld hl` where an `ld de` should be (0x92AB), so the score comes out without the
  0 after it.
- **Unused texts**: GOOD LUCK TO NEXT STAGE, FLOOR and PUSH TR1 TO START.
