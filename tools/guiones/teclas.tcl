# LAS TECLAS: ESC en el titulo (hasta el cuadro 390); la barra en el 400; jugando, quieto; STOP sostenida de 900 a
# 1500, con la palanca arriba de 950 a 1100 y abajo de 1200 a 1400 (mirar); F1 en 1900. 2800 cuadros.
proc m {a} { return [debug read memory $a] }
proc pon {a v} { debug write memory $a $v }
proc toca {fila bit} {
    keymatrixdown $fila $bit
    after time 0.05 "keymatrixup $fila $bit"
}
proc piloto {n} {
    keymatrixup 8 0xF1
    if {($n / 120) % 5 != 4} { keymatrixdown 8 0x80 } else { keymatrixdown 8 0x10 }
    if {$n % 45 < 20} { keymatrixdown 8 0x01 }
}
proc guion {n} {
    if {$n < 390} { keymatrixdown 7 0x04 } else { keymatrixup 7 0x04 }
    if {$n == 400} { toca 8 0x01 }
    if {$n >= 900 && $n < 1500} { keymatrixdown 7 0x10 } else { keymatrixup 7 0x10 }
    if {$n >= 950 && $n < 1100} { keymatrixdown 8 0x20 } else { keymatrixup 8 0x20 }
    if {$n >= 1200 && $n < 1400} { keymatrixdown 8 0x40 } else { keymatrixup 8 0x40 }
    if {$n == 1900} { toca 6 0x20 }
    return [expr {$n >= 2800}]
}
