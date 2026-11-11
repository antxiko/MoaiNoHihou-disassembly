# Under the hood

## Rebuilding the ROM

`make verify` assembles `src/moai.asm` with pasmo and out comes the 32 KB ROM **byte for byte**. `make sanity`
checks what reassembly does not cover: that no byte declared as data is read as code, that no entry point falls in
data and that all 32,768 bytes are explained. `make test` runs the tests. The ROM is not in the repository: put it in
the root as `moai.rom` (the GoodMSX dump, `[!]`, sha1 `f924d89a...`).

| | bytes |
|---|---|
| traced code | 11,848 |
| named data | 20,920 |
| unexplained | 0 |

The listing has 2,341 comments in 5,558 instructions (42.1%), 695 routines and labels, none under 10% commented, and
no called routine without a name.

## The cartridge

32 KB at 0x4000-0xBFFF, with the header at 0x4000. INIT (0x4010) also puts the cartridge in page 2 and jumps to
0x8010. The data comes first: the view limits for looking around (0x40EB), the heap of jewels of the ending
(0x412B), the title texts (0x419B), the stage maps (0x41D6-0x4E1A), the lists of what each map brings (0x4E1B), the
32 stages (0x5078, 8 bytes each), the drawing of the prize screen (0x51BE), the title's name (0x543D), the demo's
list of controls (0x5700), the sprite drawings (0x5800) and the tiles with their colours (0x6000-0x7FFF). The code
goes from 0x8010 to 0xB015; after it, the maps of four stages that did not fit in front (0xB016) and the sound
(0xB300-0xBFFF).

## The BIOS it uses

RSLREG and ENASLT for the slot; SETGRP, CHGCLR, WRTVDP, DISSCR and ENASCR; FILVRM, LDIRVM, WRTVRM and RDVRM, which
reads the screen to know which tile is in each place; GTSTCK and GTTRIG for the controls and SNSMAT for the space
bar, GRAPH, STOP, F1, SELECT, ESC and the stage select; WRTPSG for the sound. The letters are in the cartridge.

## The interrupt and the loop

INIT puts a jump to 0xAE9A in the H.TIMI hook. The interrupt does the requested silence, counts frames (sixteen
counters, 0xE010-0xE01F), runs the sound, reads F1, STOP, the buttons, the space bar, GRAPH and the joystick; in the
demo, it reads a byte of its list every 16 frames (`interrupcion`, 0xAE9A). The game runs in the **stage loop**
(`fase_bucle`, 0x8656): once per frame, the hero, what falls, what breaks, his mark on the scoreboard, the time, the
enemies, the things in the map, the colours, the high score, the points and whether a rock fell on him; then STOP,
the background sound, being hit, F1 and the stage over.

**The map.** Each stage is built in RAM (0xE800, rows of 16 bytes: 12 blocks and what the row brings) and painted
from there; a block is 2 x 2 tiles (the table at 0x8E82). The rocks are shaped pieces: each shape says on which
sides it joins its neighbours (`unido_arriba`, 0xA0CF, and the three after it), and the blow breaks the piece and the
ones joined to it. Whatever is left with nothing below falls (`caen`). The tables at 0xA14B go from the screen to the
map and back, depending on the view (0xE308).

**The tiles are read from the screen.** To know whether the hero or an enemy can pass, whether he steps on something
or whether a rock fell on him, the game does not look at the map: it reads the name table in VRAM with RDVRM
(`casillas_fila`, 0xA9AA; `aplastado`, 0x8AEA).

## How it was done

The trace follows the code from INIT, the interrupt and the enemies' jump table (0x931E), declared in
`src/moai.entries`. The rest was **measured in openMSX** (`tools/omsx_cobertura.tcl`) on a Philips VG 8020, waiting
for the demo and playing: nothing that ran was left out of the trace.

The recordings for the site (`tools/guiones/*.tcl`, recorded with `tools/lanza_graba.ps1` on C-BIOS) log, on every
frame, the VDP registers, the RAM from 0xE000, the PSG and the VRAM that changed. `tools/pantallas.py` runs the title
with `tools/bios.py` and checks it against the recording (**0 different points**), `tools/gifs.py` makes the GIFs and
`tools/musica.py` runs the sound engine.

## The RAM

| | |
|---|---|
| 0xE000 | playing |
| 0xE00A / 0xE00B | the stage (0-31) / the lives |
| 0xE010-0xE01F | the frame counters |
| 0xE020-0xE02D | the buttons: just pressed and held |
| 0xE023 / 0xE039 | SELECT / ESC on the title |
| 0xE027 / 0xE037 | the demo / its list of controls |
| 0xE031-0xE033 | the high score (BCD) |
| 0xE034-0xE036 | the score (BCD) |
| 0xE03A | the stage over (the exit) |
| 0xE100 | the hero (two sprites) |
| 0xE120 | the five enemies (16 bytes each) |
| 0xE170 | the hero's mark on the scoreboard |
| 0xE180 | the joystick |
| 0xE183 | hit |
| 0xE1B3 / 0xE1B5 | F1 / STOP |
| 0xE280-0xE2D5 | the sound: the three channels and the requests |
| 0xE308 | the view |
| 0xE30C / 0xE30D / 0xE30E / 0xE30F | protection from types 3 and 6 / the jewels / the blocks / protection from types 1, 2 and 5 |
| 0xE31F / 0xE320 | the time: minutes / seconds (BCD) |
| 0xE321 / 0xE322 | the points to add |
| 0xE326 | looking around (STOP) |
| 0xE331 | the look-around frame (seven sprites) |
| 0xE600 | what breaks and what falls |
| 0xE700 | the title, in RAM |
| 0xE800 | the stage map |
