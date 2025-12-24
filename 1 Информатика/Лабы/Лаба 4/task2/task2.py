import re

def convert(str):
    teg = re.findall(r'^<.+>.', str)[0][1:-2] 
    val = 'null' if len(re.findall(r'>.+<', str)) == 0 else re.findall(r'>.+<', str)[0][1:-1]
    return f'"{teg}" : "{val}"'


out = open('/home/anti/Учёба/Infa/task2/task2.xml', 'r', encoding='utf-8').readlines()
out = [re.sub(r'> *<', '> <', i) for i in out] # удаляем лишние пробелы в строке
out = [re.sub(r'(^ +)|(\n* *$)', '', i) for i in out] # удаляем пробелы в начале и в концe
out = (' '.join(out)).split("> <") # разделяем разные теги, если это не сделали раньше
out = [re.sub(r'(^<)|(>$)', '', i) for i in out] # делим на нужные нам строки
out = ['<' + i + '>' for i in out] # добавляем символы которые мы удалили в прошлой строке

to = open('/home/anti/Учёба/Infa/task2/task2.json', 'w', encoding='utf-8')
to.write('{\n')

j = 0
while j < len(out):
    i = out[j] # Так просто удобнее работать

    if ('<?' in i):
        j+=1
        continue

    if (j+1 < len(out) and out[j][1:-1] == out[j+1][2:-1]): # обрабатываем случай <...></...>
        if j+2 < len(out) and "</" in out[j+2] and out[j+2].count('<') == 1:
            to.write(f'"{i[1:-1]}" : null ')
        else:
            to.write(f'"{i[1:-1]}" : null, ')
        j += 2
        continue

    if i.count('</') == 1 and i.count('>') == 1: # Меняем строку (*много пробелов)</ ... > в сторку (*много пробелов)}, учитывая при этом нужность запятой
        if j+1 < len(out) and out[j+1].count('<') == 1 and out[j+1].count('>') == 1 and '</' not in out[j+1]:
            to.write('}, ')
        else:
            to.write('} ')
        j+=1
        continue

    if i.count('<') == 1 and i.count('>') == 1: # Меняем сторку (*много пробелов)< ... > в (*много пробелов)"...": {
        to.write(i.replace('<', '"').replace('>', '": { '))
        j+=1
        continue

    if i.count('<') == 2 and i.count('>') == 2: # Меняем сторку <...> ... </...> в "..." : " ... ", учитывая нужность заятой
        if "</" in out[j+1] and out[j+1].count('<') == 1:
            to.write(convert(i) + '')
        else:
            to.write(convert(i) + ', ')
        j+=1
        continue

to.write('\n}')