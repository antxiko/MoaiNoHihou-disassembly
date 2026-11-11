# INVENCIBLE: SELECT pulsada en el titulo (0xE023 = 1) y el piloto de partida.tcl. 6000 cuadros.
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
    if {$n < 390} { keymatrixdown 7 0x40 } else { keymatrixup 7 0x40 }
    if {$n == 400} { toca 8 0x01 }
    if {[m 0xE000] == 1} { piloto $n }
    return [expr {$n >= 6000}]
}
