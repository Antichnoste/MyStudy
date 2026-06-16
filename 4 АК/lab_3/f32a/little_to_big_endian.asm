    .text
\ --- Процедура: shl8 ---
\ Сдвигает TOS влево на 8 бит (x << 8).
\ Стек: ( x -- x<<8 )
shl8:
    lit 7 >r
shl8_loop:
    2*
    next shl8_loop
    ;

\ --- Процедура: shr8 ---
\ Логический сдвиг TOS вправо на 8 бит (x >> 8).
\ Стек: ( x -- x>>8 )
shr8:
    lit 7 >r
shr8_loop:
    2/
    lit 0x7FFFFFFF
    and
    next shr8_loop
    ;

\ --- Процедура: byteswap ---
\ Меняет порядок байт 32-битного слова (little-endian <-> big-endian)
\ через цикл из 4 шагов: result = (result<<8) xor (n&0xFF), n >>= 8.
\ Стек: ( n -- result )
byteswap:
    a!                        \ n -> A
    lit 0                     \ result

    lit 3 >r                  \ 4 итерации
byteswap_loop:
    shl8                      \ result <<= 8

    a 
    lit 0xFF
    and
    xor                         \ result ^= (A & 0xFF)

    a 
    shr8
    a!                           \ A >>= 8

    next byteswap_loop
    ;

\ --- Точка входа ---
_start:
    lit 0x80    \ кладем на стэк 0x80
    b!          \ B = 0x80

    @b          \ читаем n из io[0x80]: ( n ) и  кладем его на стэк

    byteswap    \ переставляем байты: ( result )

    lit 0x84    \ кладем на стэк 0x84
    b!          \ B = 0x84

    !b          \ result -> io[0x84]

    halt