import xmltodict
import csv

xml = xmltodict.parse(open('/home/anti/Учёба/Infa/task5/task5.xml', 'r', encoding='utf-8').read())
writer = csv.writer(open('/home/anti/Учёба/Infa/task5/task5.csv', 'w', encoding='utf-8', newline=''), delimiter=';')

print(xml)

def dfs(v, tab):
    for i in v:
        if type(v[i]) != dict:
            if (type(v[i]) == list):
                writer.writerow(['' for i in range(tab)] + [i])
                for cur in v[i]:
                    writer.writerow(['' for i in range(tab+1)] + ['"' + str(cur) + '"'])
                continue
            #print('\t'*tab + i + ' - ' + str(v[i]))
            writer.writerow(['' for i in range(tab)] + [i] + ['"' + str(v[i]) + '"'])
        else:
            #print('\t'*tab + i + " : ")
            writer.writerow(['' for i in range(tab)] + [i])
            dfs(v[i], tab+1) 

dfs(xml,0)