# Moai no Hihou - desensamblado comentado

*(Also [in English](README.md).)*

El desensamblado comentado de **Moai no Hihou** (Casio, 1986) para MSX: un cartucho de 32 KB con la cabecera en 0x4000.

- **100 %** del binario explicado: 11.848 bytes de código y 20.920 de datos con nombre, ni un byte sin asignar.
- **42,1 %** del listado comentado, 695 rutinas y etiquetas, ninguna por debajo del 10 % de comentarios.
- El listado se reensambla en la ROM original **byte a byte**.
- El título sale de ejecutar la ROM, cotejado con openMSX punto a punto; la presentación de CASIO, la demostración, las fases, el BONUS GAME, el final, el selector de fase, STOP y F1, jugados en GIF en openMSX; las cinco músicas, de su propio motor de sonido, idénticas a openMSX cuadro a cuadro.

La web: <https://antxiko.github.io/MoaiNoHihou-disassembly/es/>
(en inglés: <https://antxiko.github.io/MoaiNoHihou-disassembly/>).

## Reproducirlo

La imagen de la ROM no se distribuye. Pon la tuya en la raíz como `moai.rom` (sha1 `f924d89a...`) y ejecuta `make`. El detalle, en [POR DENTRO](docs/es/POR-DENTRO.md).

## Legal

El juego es de Casio y de sus titulares. La licencia de `LICENSE` cubre solo las herramientas, los comentarios, el análisis y la documentación de aquí. Mira [AVISO-LEGAL.md](AVISO-LEGAL.md).
