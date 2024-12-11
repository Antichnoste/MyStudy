f = open('/home/anti/Учёба/Infa/Лаба 5/SPFB.RTS-12.18_180901_181231.csv', 'r', encoding='utf-8').readlines()
out = open('data.csv', 'w', encoding="utf-8")

patern = ["14/09/18", "16/10/18", "14/11/18", "14/12/18"]
    

for i in f:
    if (f.index(i) == 0):
        continue

    cur = i.split(',')[2]

    if (cur in patern):
        mas = i.split(',')
        mas = [mas[2], str(int(float(mas[4]))), str(int(float(mas[5]))), str(int(float(mas[6]))), str(int(float(mas[7])))]
        out.write((','.join(mas)) + '\n')