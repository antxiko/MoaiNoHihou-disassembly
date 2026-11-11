# The music

Five tunes, in three voices. They are not hand-made recordings: `tools/musica.py` **runs the ROM's own sound
engine** with `tools/z80run.py` -the sound routine (`sonido`, 0xB376), frame by frame, with the number the game
writes- and logs what it writes to the PSG through the BIOS (WRTPSG).

**Checked against openMSX**: the tone and volume registers of the three channels match the recorded ones, **0
different** in every frame looked at, in all five. Six recordings are checked (`tools/guiones/`): the title with the
demo, a game up to GAME OVER, one with SELECT, one with the keys, one with the stage select and the forced run
through the 32 stages. Each recorded frame is paired with the engine frame that has the same RAM in the three
channels; while an effect plays on a channel, that channel is not looked at. The ending tune is checked the first
time it plays: after that the game asks for it again and again.

## The engine

The engine sits at the end of the cartridge, with a jump table at 0xB300: ask for a channel A effect, a B and C
one, a tune, the sound of one frame, PSG register 7 and silence. It runs once per frame from the interrupt and takes
three **requests**: a tune (0xE2BE), an effect for channel A (0xE2C0) and another for B and C (0xE2C2); the lower
number wins (`musica_pide`, 0xB371). The tables: six tunes at 0xB312 (number 0, nothing), six channel A effects at
0xB336, four B and C ones at 0xB342 and fourteen durations at 0xB627.

During a stage no tune plays: the background sound is an **effect** on channels B and C (number 3; number 2 in the
BONUS GAME), which the stage loop asks for on every pass.

| | Who asks for it | Length |
|---|---|---:|
| the CASIO intro | the CASIO meet (0xAC31) | 1.1 s |
| the stage | when the stage starts (0x8602) | 6.0 s |
| the stage over | the hero crosses the prize screen (0x8C25) | 11.3 s |
| the ending | the ending, over and over (0x8C61, 0x8CAB) | 9.8 s |
| GAME OVER | with no lives left (0x8A7E) | 7.6 s |

None starts again on its own: they all end.

## The CASIO intro

<audio controls src="audio/musica_casio.mp3"></audio>

## The stage

<audio controls src="audio/musica_fase.mp3"></audio>

## The stage over

<audio controls src="audio/musica_fase_acabada.mp3"></audio>

## The ending

<audio controls src="audio/musica_final.mp3"></audio>

## GAME OVER

<audio controls src="audio/musica_game_over.mp3"></audio>
