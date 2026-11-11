# The texts

The letters are in the cartridge (0x6680), in the same order as the BIOS font: a letter is its code - 0x30, and
tile 0x10 is the space (`letras_pon`, 0xADBA). The game's name and CASIO are drawn tiles.

| address | original | translation | where it appears |
|---|---|---|---|
| 0xAD1F | CASIO | Casio | the intro, in drawn tiles |
| 0xAD3A | SOFTWARE | Software | the intro |
| 0x419B | CASIO | Casio | the title, in drawn tiles |
| 0x543D | モアイの秘宝 | The treasure of the moai | the title, in drawn tiles |
| 0x41B6 | COPYRIGHT 1986 © CASIO | Copyright 1986 Casio | the title |
| 0x41CC | GAME START | Game start | the title |
| 0x41A1 | PUSH TRIG1 OR SPACE | Press button 1 or the space bar | the title |
| 0x81A4 | STAFF | Staff | the credits, below the title |
| 0x81AC | K.ARISAWA, K.ASAHINA, K.SATOH, K.OKUYAMA, A.HASEGAWA, K.OHSAWA, J.ARCHER | (names) | the credits |
| 0x81F1 | PRODUCER / T.MORIYAMA | Producer: T. Moriyama | the credits, on two rows |
| 0x92EC | HIGH | High score | the scoreboard |
| 0x92D3 | SCORE | Score | the scoreboard |
| 0x92D9 | STAGE | Stage | the scoreboard |
| 0x92CE | TIME | Time | the scoreboard |
| 0x8517 | BONUS | Bonus | the scoreboard, in the BONUS GAME |
| 0x8616 | P= | Lives | the scoreboard |
| 0x8619 | PUSH TR1 TO START | Press button 1 to start | **never shown** (see below) |
| 0x847B | BONUS GAME | Bonus stage | when a BONUS GAME starts |
| 0x8D44 | YOU GET BONUS | You get a bonus | the stage over and the BONUS over |
| 0x8D52 | 1000× = 000PTS | 1000 × n = n000 points | the stage over |
| 0x8D3C | PJM1622 | (no translation) | the ending |
| 0x8A87 | GAME OVER | Game over | with no lives left |
| 0x92DF | "     0" | (the 0 after the score) | **never shown** ([Curiosities](CURIOSITIES.html)) |
| 0x92E6 | FLOOR | Floor | **no pointer reaches it** |
| 0x8D63 | GOOD LUCK TO NEXT STAGE | Good luck in the next stage | **no pointer reaches it** |

**PUSH TR1 TO START** follows P= in the same text, separated by a 0xFF: the routine that writes it (`texto_vram`,
0x92C3) stops at the 0xFF, so only P= is shown.

**PJM1622** appears in the top corner of the ending. We have not found what it means.
