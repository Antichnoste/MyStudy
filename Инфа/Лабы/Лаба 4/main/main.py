out = open('/home/anti/Учёба/Infa/main/main.xml', 'r', encoding='utf-8')
to = open('/home/anti/Учёба/Infa/main/main.json', 'w', encoding='utf-8')
mas = out.read().split('\n') # открываем наш xml-файл

def convert(s): #Конвертирует строку (*много пробелов)< ... > ... </ ... > в (*много пробелов)" ..." : " ... "
    ans = ''
    chek = 0
    for i in s:
        if chek == 2:
            return ans
        elif i == '<':
            ans += '"'
            chek += 1 
        elif i == '>':
            ans += '" : "'
        elif chek < 2:
            ans += i     

def tab(s): # Сохраняет табуляцию как в исходном тексте (count = 4 т.к. изначально в json идёт { и из-за этого табуляция изменяется на 4)
    count = 4
    for i in s:
        if i != ' ':
            return count*' '
        count += 1

to.write('{\n') # Добовляет эту злопалучную {

for j in range(len(mas)):
    i = mas[j] # Так просто удобнее работать

    if ('<?' in i):
        continue

    if i.count('</') == 1 and i.count('>') == 1: # Меняем строку (*много пробелов)</ ... > в сторку (*много пробелов)}, учитывая при этом нужность запятой
        if j+1 < len(mas) and mas[j+1].count('<') == 1 and mas[j+1].count('>') == 1 and '</' not in mas[j+1]:
            to.write(tab(i) + '},\n')
        else:
            to.write(tab(i) + '}\n')
        continue

    if i.count('<') == 1 and i.count('>') == 1: # Меняем сторку (*много пробелов)< ... > в (*много пробелов)"...": {
        s = i.replace('<', '"').replace('>', '": {\n')
        to.write('\t' + s)
        continue

    if i.count('<') == 2 and i.count('>') == 2: # Меняем сторку (*много пробелов)<...> ... </...> в (*много пробелов)"..." : " ... ", учитывая нужность заятой
        if "</" in mas[j+1] and mas[j+1].count('<') == 1:
            to.write('\t' + convert(i) + '\n')
        else:
            to.write('\t' + convert(i) + ',\n')
        continue

to.write('}') # Добовляет эту злопалучную } для закрытытия файла
