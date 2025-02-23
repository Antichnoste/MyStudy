import xmltodict
import json

out = open('/home/anti/Учёба/Infa/task1/task1.xml', 'r', encoding='utf-8').read() # Открываем файл как строку
to = open('/home/anti/Учёба/Infa/task1/task1.json', 'w', encoding='utf-8')

out = xmltodict.parse(out) #Парсим xml-файл в словарь
json.dump(out, to, ensure_ascii=False, indent=4) #Конвертируем словарь в json-файл,ensure_ascii - записывет символы отличные от ascii без экранирования, indent - отступы делает равные одному tab