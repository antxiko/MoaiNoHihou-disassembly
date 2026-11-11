# EL SELECTOR DE FASE: la B y el 5 pulsadas al empezar la partida (de 380 a 520); la barra en el 400; despues, el
# piloto de partida.tcl. 2500 cuadros.
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
    if {$n >= 380 && $n < 520} { keymatrixdown 2 0x80; keymatrixdown 0 0x20 } else { keymatrixup 2 0x80; keymatrixup 0 0x20 }
    if {$n == 400} { toca 8 0x01 }
    if {$n >= 520 && [m 0xE000] == 1} { piloto $n }
    return [expr {$n >= 2500}]
}
