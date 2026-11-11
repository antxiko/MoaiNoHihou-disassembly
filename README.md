# Moai no Hihou - commented disassembly

*(También [en castellano](README.es.md).)*

The commented disassembly of **Moai no Hihou** (Casio, 1986) for the MSX: a 32 KB cartridge with its header at 0x4000.

- **100%** of the binary explained: 11,848 bytes of code and 20,920 of named data, not one byte unassigned.
- **42.1%** of the listing commented, 695 routines and labels, none below 10% of comments.
- The listing reassembles into the original ROM **byte for byte**.
- The title comes from running the ROM, checked against openMSX point by point; the CASIO intro, the demo, the stages, the BONUS GAME, the ending, the stage select, STOP and F1, played in GIF in openMSX; the five tunes, from its own sound engine, identical to openMSX frame by frame.

The site: <https://antxiko.github.io/MoaiNoHihou-disassembly/>
(in Spanish: <https://antxiko.github.io/MoaiNoHihou-disassembly/es/>).

## Reproducing it

The ROM image is not distributed. Put yours in the root as `moai.rom` (sha1 `f924d89a...`) and run `make`. The details, in [UNDER THE HOOD](docs/UNDER-THE-HOOD.md).

## Legal

The game belongs to Casio and its rights holders. The licence in `LICENSE` covers only the tools, the comments, the analysis and the documentation here. See [LEGAL-NOTICE.md](LEGAL-NOTICE.md).
