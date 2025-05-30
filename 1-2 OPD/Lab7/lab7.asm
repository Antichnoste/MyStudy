; Синтезировать команду SHR X c кодом операции 0F2X, которая сдвигает AC вправо на X разрядов, 15 бит заполняется 0
; Начало тестирующей команды - 00СF

; 0 -> C                        0000200000              E0
; if CR(7) = 1 then GOTO ED     81ED801002              E1
; if CR(6) = 1 then GOTO ED     81ED401002              E2
; if CR(5) = 0 then GOTO ED     80ED201002              E3
; if CR(4) = 1 then GOTO ED     81ED101002              E4

; if CR(3) = 1 then GOTO E9     81E9081002              E5
; if CR(2) = 1 then GOTO E9     81E9041002              E6
; if CR(1) = 1 then GOTO E9     81E9021002              E7
; if CR(0) = 0 then GOTO ED     80ED011002              E8

; ~0 + CR -> CR                 0002009202              E9
; ROR(AC) -> AC                 0010180010              EA
; 0 -> C                        0000200000              EB
; GOTO E5                       80E5109040              EC
; GOTO INT @ C4                 80C4101040              ED


ma
mw 0000200000
mw 81ED801002
mw 81ED401002
mw 80ED201002
mw 81ED101002
mw 81E9081002
mw 81E9041002
mw 81E9021002
mw 80ED011002
mw 0002009202
mw 0010180010
mw 0000200000
mw 80E5109040
mw 80C4101040
mdecodeall


ma mw 0000200000 mw 81ED801002 mw 81ED401002 mw 80ED201002 mw 81ED101002 mw 81E9081002 mw 81E9041002 mw 81E9021002 mw 80ED011002 mw 0002009202 mw 0010180010 mw 0000200000 mw 80E5109040 mw 80C4101040 mdecodeall


; Тестовая программа

        ORG 0x00CF
pnt:        WORD 0x0001
X1:         WORD 0xFFFE
chec1:      WORD 0x7FFF
X2:         WORD 0x70FF
chec2:      WORD 0x0007
X3:         WORD 0x0010
chec3:      WORD 0x0010

START:  CLA
        CALL TEST1
        CALL TEST2
        CALL TEST3
        HLT

TEST1:
        LD X1
        NOP
        WORD 0x0F21 ; сдвиг на 1 бит вправо
        NOP
        CMP chec1
        BEQ equal1
        RET
equal1: LD #0x01
        ST (pnt)+
        RET

TEST2:
        LD X2
        NOP
        WORD 0x0F2C ; сдвиг на 12 битов вправо
        NOP
        CMP chec2
        BEQ equal2
        RET
equal2: LD #0x01
        ST (pnt)+
        RET

TEST3:  
        LD X3
        NOP
        WORD 0x0F3F ; неверный код программы, не должно работать
        NOP
        CMP chec3
        BEQ equal3
        RET
equal3: LD #0x01
        ST (pnt)+
        RET


;-------------------
; Тоже тестовая программа, но только по проще
ORG 0x10
START: 
INC
INC
WORD 0x0F21
HLT