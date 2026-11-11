# FORZADA: un recorrido por las 32 fases. El piloto de partida.tcl juega cada fase y, 1700 cuadros despues de que
# cambie su numero (el cruce de la pantalla y la musica de salida duran unos 1100), se da por acabada con un poke:
# 0xE03A = 1 (la salida) o, en el BONUS GAME, 0xE183 = 1 (el BONUS acaba asi). Sin SELECT: con ella el protagonista
# se queda en los pinchos, 0xE183 se pone cada cuadro y el bucle no llega a mirar 0xE03A. Las vidas, por debajo de 3,
# se ponen a 9 (0xE00B). Tras la 31 (la ultima), sin tocar nada: 3000 cuadros de final. Tope, 90000 cuadros.
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
set ::fase -1
set ::desde 0
proc guion {n} {
    if {[m 0xE000] == 0} {
        keymatrixup 8 0xF1
        if {$n == 400} { toca 8 0x01 }
        if {[info exists ::empezada]} {
            if {![info exists ::fin]} { set ::fin $n }
            return [expr {$n >= $::fin + 600}]
        }
        return [expr {$n >= 90000}]
    }
    set ::empezada 1
    set f [m 0xE00A]
    if {$f != $::fase} { set ::fase $f; set ::desde $n }
    if {$n - $::desde >= 1700 && [m 0xE183] == 0 && ![info exists ::hecho($f)]} {
        if {($f & 3) == 3} { pon 0xE183 1 } else { pon 0xE03A 1 }
        set ::hecho($f) 1
        if {$f == 31} { set ::ultimo $n }
    }
    if {[info exists ::ultimo]} { keymatrixup 8 0xF1; return [expr {$n >= $::ultimo + 3000}] }
    if {[m 0xE00B] < 3} { pon 0xE00B 9 }
    piloto $n
    return [expr {$n >= 90000}]
}
