"""Lo que se afirma de la ROM, comprobado contra sus bytes.

Corre con la ROM delante y sin ella: cuando no esta, la imagen se rehace desde
las filas defb/defw del listado, que si viaja con el repositorio. Sin la ROM
solo se comprueba lo que cae en datos.
"""

import os
import re
import subprocess
import sys
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "tools"))

ROM = os.path.join(RAIZ, "moai.rom")
ASM = os.path.join(RAIZ, "src", "moai.asm")
NOTAS = os.path.join(RAIZ, "src", "moai.notes")
ORG = 0x4000
TAM = 32768

FILA = re.compile(r"^\s+def(b|w)\s+([0-9a-fA-F,h ]+)\s*;\s*([0-9a-f]{4})")


def imagen_desde_el_listado():
    img = bytearray(TAM)
    with open(ASM, encoding="utf-8") as f:
        for ln in f:
            m = FILA.match(ln)
            if not m:
                continue
            ancho, cuerpo, dirr = m.group(1), m.group(2), int(m.group(3), 16)
            p = dirr - ORG
            for tok in cuerpo.split(","):
                tok = tok.strip().rstrip("h")
                if not tok:
                    continue
                v = int(tok, 16)
                if ancho == "b":
                    img[p] = v
                    p += 1
                else:
                    img[p] = v & 0xFF
                    img[p + 1] = v >> 8
                    p += 2
    return bytes(img)


def lee():
    if os.path.exists(ROM):
        with open(ROM, "rb") as f:
            return f.read()
    return imagen_desde_el_listado()


def b(a):
    return lee()[a - ORG]


def w(a):
    rom = lee()
    return rom[a - ORG] | (rom[a - ORG + 1] << 8)


def instruccion(dirr):
    """La instruccion del listado en esa direccion (sin el comentario)."""
    with open(ASM, encoding="utf-8") as f:
        for ln in f:
            m = re.match(r"^	(\S.*?)\s*;([0-9a-f]{4})", ln)
            if m and int(m.group(2), 16) == dirr:
                return m.group(1).replace("	", " ").strip()


def texto(a, n):
    """Casilla = letra - 0x30 (el orden de la fuente de la BIOS); 0x10 es el espacio."""
    return "".join(" " if c == 0x10 else chr(c + 0x30) for c in lee()[a - ORG:a - ORG + n])


class Cabecera(unittest.TestCase):
    def test_ab_e_init_en_0x4010(self):
        rom = lee()
        self.assertEqual(rom[:2], b"AB")
        self.assertEqual(w(0x4002), 0x4010)

    def test_init_pone_la_pagina_2_y_salta(self):
        self.assertEqual([instruccion(a) for a in (0x4033, 0x4035, 0x4038)],
                         ["ld h,080h", "call 00024h", "jp arranque"])

    def test_son_32_kb(self):
        self.assertEqual(len(lee()), TAM)


class LaInterrupcion(unittest.TestCase):
    def test_va_por_h_timi(self):
        self.assertEqual([instruccion(a) for a in (0x8023, 0x8026, 0x802B)],
                         ["ld hl,0ae9ah", "ld (0fda0h),hl", "ld (0fd9fh),a"])


class LosTextos(unittest.TestCase):
    def test_el_titulo(self):
        self.assertEqual(texto(0x41A1, 19), "PUSH TRIG1 OR SPACE")
        self.assertEqual(texto(0x41CC, 10), "GAME START")
        self.assertEqual(lee()[0x419B - ORG:0x41A1 - ORG], bytes(range(0x8A, 0x90)))

    def test_la_partida(self):
        self.assertEqual(texto(0x847B, 10), "BONUS GAME")
        self.assertEqual(texto(0x8619, 17), "PUSH TR1 TO START")
        self.assertEqual(texto(0x8A87, 9), "GAME OVER")

    def test_el_premio(self):
        self.assertEqual(texto(0x8D3C, 7), "PJM1622")
        self.assertEqual(texto(0x8D44, 13), "YOU GET BONUS")

    def test_el_marcador(self):
        self.assertEqual(texto(0x92CE, 4), "TIME")
        self.assertEqual(texto(0x92D3, 5), "SCORE")
        self.assertEqual(texto(0x92E6, 5), "FLOOR")

    def test_los_creditos(self):
        self.assertEqual(texto(0x81A4, 7), "  STAFF")


class ElFalloDelMarcador(unittest.TestCase):
    def test_ld_hl_donde_iba_ld_de(self):
        self.assertEqual([instruccion(a) for a in (0x92A8, 0x92AB, 0x92AE)],
                         ["ld hl,0187ah", "ld hl,092dfh", "call texto_vram"])


class LasTeclasDelTitulo(unittest.TestCase):
    def test_select(self):
        self.assertEqual([instruccion(a) for a in (0x80A9, 0x80AE, 0x80B4)],
                         ["ld a,007h", "bit 6,a", "ld (0e023h),a"])

    def test_esc_continuar(self):
        self.assertEqual([instruccion(a) for a in (0x80BC, 0x80C3, 0x80C8)],
                         ["bit 2,a", "ld (0e039h),a", "ld (0e032h),a"])


class LaPartida(unittest.TestCase):
    def test_cinco_vidas(self):
        self.assertEqual([instruccion(a) for a in (0x821C, 0x821E)], ["ld a,005h", "ld (0e00bh),a"])

    def test_cada_cuarta_fase_el_bonus(self):
        self.assertEqual([instruccion(a) for a in (0x83D1, 0x83D3)], ["and 003h", "cp 003h"])

    def test_tras_la_32_el_final(self):
        self.assertEqual([instruccion(a) for a in (0x8BD6, 0x8BD9)], ["ld a,(0e00ah)", "cp 020h"])

    def test_32_fases_con_el_mismo_marcador(self):
        for k in range(32):
            self.assertEqual(w(0x5078 + 8 * k + 2), 0xAA68)

    def test_el_selector_lee_la_fila_2(self):
        self.assertEqual([instruccion(a) for a in (0x8319, 0x831B)], ["ld a,002h", "call 00141h"])


class Sonido(unittest.TestCase):
    def test_la_tabla_de_saltos(self):
        for k in range(6):
            self.assertEqual(b(0xB300 + 3 * k), 0xC3)

    def test_cinco_musicas(self):
        self.assertEqual({w(0xB312 + 2 * j) for j in range(3)}, {0xB75B})
        for k in range(1, 6):
            for j in range(3):
                self.assertTrue(0xB730 <= w(0xB312 + 6 * k + 2 * j) < 0xC000)


class ElListado(unittest.TestCase):
    def test_densidad_y_flojas(self):
        salida = subprocess.run(
            [sys.executable, os.path.join(RAIZ, "tools", "densidad.py"), ASM],
            capture_output=True, text=True, check=True).stdout
        m = re.search(r"(\d+) instrucciones, (\d+) comentarios", salida)
        self.assertGreaterEqual(int(m.group(2)) * 100, 40 * int(m.group(1)))
        self.assertIn("---- 0 rutinas por debajo del 10 %", salida)

    def test_ningun_call_sin_nombre(self):
        salida = subprocess.run(
            [sys.executable, os.path.join(RAIZ, "tools", "sin_bautizar.py"), ASM],
            capture_output=True, text=True, check=True).stdout
        self.assertTrue(salida.startswith("0 rutinas sin bautizar"), salida[:200])

    def test_cada_comentario_en_su_instruccion(self):
        salida = subprocess.run(
            [sys.executable, os.path.join(RAIZ, "tools", "valida_c.py"), ASM, NOTAS],
            capture_output=True, text=True, check=True).stdout
        self.assertIn("0 fuera de sitio, 0 repetidos", salida)


if __name__ == "__main__":
    unittest.main()
