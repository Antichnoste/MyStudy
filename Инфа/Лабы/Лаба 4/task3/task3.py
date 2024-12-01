import re

f = open("/home/anti/Учёба/Infa/task3/task3.xml",'r', encoding="utf-8").read()
out = open("/home/anti/Учёба/Infa/task3/task3.json", 'w', encoding='utf-8')

f = f.replace('\n', '').strip()
f = re.sub(r'>( +)<', '><', f)
f = f.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&apos;', "'").replace("&quot;",'"')

def head_del(f):
    if f[0:2] == '<?':
        p = 2
        while f[p-2:p] != '?>':
            p+= 1
        f = f[p:]
    return f

def commentary_del(f):
    result = ''
    in_com = False
    i = 0
    while i < len(f):
        if i+4 < len(f) and not in_com and f[i:i+4] == '<!--':
            i += 4
            in_com = True
        elif i+4 < len(f) and in_com and f[i:i+3] == '-->':
            i += 3
            in_com = False
        elif not in_com:
            result += f[i]
            i += 1
        else:
            i += 1
    return result

def atributs_convert(f):
    result = []
    buffer = []
    in_tag = False
    i = 0
    while i < len(f):
        if f[i] == '<':
            in_tag = True
        if f[i] == '>':
            in_tag = False
        
        if not in_tag:
            result.append(f[i])
            if len(buffer) > 0:
                result.extend(buffer)
            buffer.clear()
            i += 1
        elif f[i] == ' ':
            k = i + 1
            buffer.append('<@')
            while f[k] != '=':
                buffer.append(f[k])
                k += 1
            buffer.append('>')
            p1 = i + 1
            p2 = k

            i = k + 1
            k = i + 1
            while f[k] != f[i]:
                buffer.append(f[k])
                k += 1
            buffer.append('<')
            buffer.append('/')
            for i in f[p1:p2]:
                buffer.append(i)
            buffer.append('>')
            i = k + 1
        else:
            result.append(f[i])
            i += 1
    return ''.join(result)

def alongtag_convert(f):
    result = []
    tag_begin = 0
    i = 0
    while i < len(f):
        if f[i] == '<':
            tag_begin = i
        if f[i:i+2] == '/>':
            result.extend(['>', '<', '/'])
            k = tag_begin + 1
            while f[k] != ' ' and f[k] != '/':
                result.append(f[k])
                k += 1
            result.append('>')
            i += 2
        else:
            result.append(f[i])
            i += 1
    return ''.join(result)

id = 0

def correct(dik):
    cur = ''
    flag = False

    for i in dik:
        if type(i) == dict:
            flag = True
        
    if (not flag):
        return dik

    flag = False
    ind = -1
    i = 0
    while i < len(dik):
        if type(dik[i]) == str:
            cur += dik[i]
            dik.pop(i)
        elif type(dik[i]) == dict and not flag:
            ind = i
            flag = True
            i += 1
    if cur != '':
        if dik[ind].get('#text') != None:
            dik[ind]['#text'][0] += cur 
        else:
            dik[ind]['#text'] = [cur]
    return dik

def fun(dik):
    global id,f
    message = False
    while id < len(f):

        if f[id] == '<' and f[id + 1] != '/':
            if not message:
                dik.append({})
                message = True
            id += 1
            k = id
            while f[id] != '>':
                id += 1
            node = f[k:id]
            id += 1
            if len(dik) > 1:
                dik = correct(dik)
            if node in dik[-1]:
                dik[-1][node] = fun(dik[-1][node])
            else:
                dik[-1][node] = fun([])

        elif f[id] == '<' and f[id + 1] == '/':
            if len(dik) == 0 and type(dik) == list:
                dik.append('null')
            while f[id] != '>':
                id += 1
            id += 1
            return correct(dik)
        
        else:
            k = id
            while f[id] != '<':
                id += 1
            dik.append(f[k:id].replace('"', '\\"'))
    return dik

f = head_del(f)
f = commentary_del(f)
f = alongtag_convert(f)
f = atributs_convert(f)

dik = fun([])

def dfs(v, tab):
    k = -1
    for i in v:
        k += 1
        if type(v[i][0]) != dict:
            if (len(v[i]) > 1):
                out.write('\t' * tab + '"' + i + '" : [\n')
                for id in range(len(v[i])):
                    if id == len(v[i])-1:
                        out.write('\t' * (tab+1) + '"' + v[i][id] + '"\n')
                    else:
                        out.write('\t' * (tab+1) + '"' + v[i][id] + '",\n')
                if k == len(v)-1:
                    out.write('\t' * tab + ']\n')
                else:
                    out.write('\t' * tab + '],\n')
                continue

            if k == len(v)-1:
                out.write('\t'*tab + '"' + i + '" : "' + str(v[i][0]) + '"\n')
            else:
                out.write('\t'*tab + '"' + i + '" : "' + str(v[i][0]) + '",\n')
        else:
            out.write('\t'*tab + '"' + i + '" : {\n')
            dfs(v[i][0], tab+1) 

            if k == len(v)-1:
                out.write('\t' * tab + '}\n')
            else:
                out.write('\t' * tab + '},\n')


out.write('{\n')
dfs(dik[0],1)
out.write('}')