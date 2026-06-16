    .data     
n:               .word  0x0
sum:             .word  0x0
digit:           .word  0x0
mod:             .word  0xA     ; А = 1010 = 10 

.text
.org 0x100
_start:
    load_addr    0x80
    store        n
    
    bgtz          calc_loop      ; если n > 0, сразу к началу цикла (оказывается существует обновление wrench и там не знают что такое обратная совместимость и могу переименовывать команды)

positive:
    load_imm     0x0
    sub          n
    bvs          overflow       ; если мы встретили n = -2^31 = 1000...0000, то когда мы вычтим это из 0: 0000...0000 - 1000...0000 = 0000...0000 + 1000...0000 = 1000...0000(V=1, флаг появился потому что (+) - (-) != (-)) 
    store        n

calc_loop:
    load         n
    beqz         write_result

    rem          mod
    store        digit          ; digit <- n % 10

    load         n              
    div          mod
    store        n              ; n <- n / 10

    load         sum
    add          digit
    bvs          overflow       ; проверка переполнения результата
    store        sum            ; sum <- sum + digit

    jmp          calc_loop

overflow:
    load_imm     0xCCCCCCCC
    jmp          finish

write_result:
    load         sum

finish:
    store_addr   0x84
    halt