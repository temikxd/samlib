from grab import Grab, GrabError

import re

i = 0
j = 0
t = 0

m = 0
log = 'Список обновлённых книг \n'
open('/home/a/Документы/samlib/data/log.txt', 'w').write('')
try:
    booklist = open('/home/a/Документы/samlib/data/booklist.txt', 'r').read()
except FileNotFoundError:
    print('ОШИБКА! ФАЙЛ КАТАЛОГА НЕ НАЙДЕН!\nБыл создан новый файл каталога')
    open('/home/a/Документы/samlib/data/booklist.txt', 'w').write('')
    booklist = open('/home/a/Документы/samlib/data/booklist.txt', 'r').read()

while True:
    print('Добро пожаловать \n Введите цифру для продолжения \n  1 - Загрузить новую книгу \n  2 - Обновить ранее загруженные')
    i = input()
    if i=='1':
        try:
            print('   Введите ссылку на книгу, после чего поставьте пробел и нажмите "Enter"')
        except :
            print('ОШИБКА! ВВЕДИТЕ КОРРЕКТНУЮ ССЫЛКУ!')
            continue
        link = input()
        link = link[0:-1]
        link = link.replace('http://','')
        g = Grab(log_file='/home/a/Документы/samlib/data/out.html')
        g.go(link)
        #g.go('http://samlib.ru/w/wrochek_s/deadgod.shtml')
        text = open('/home/a/Документы/samlib/data/out.html', 'r', encoding='cp1251').read()
        autor = g.xpath_text('//html/body/div/h3')
        name = g.xpath_text('//html/body/center/h2')
        book = autor+name
        book = book.replace(': другие произведения.',' - ')
        locallink = '/home/a/Документы/samlib/'+(book)+'.txt'
        #print(book)
        # Чистим от мусора
        TAG_RE = re.compile(r'<[^>]+>')
        def remove_tags(text):
            return TAG_RE.sub('', text)
        text = remove_tags(text)
        text = text.replace('&nbsp;', '')
        text = text.replace('&copy;', '')
        i = text.rfind('Copyright')
        text = text[1:i]
        # i = text.rfind('Комментарии:')
        # text = text[1:i]
        i = text.rfind('\n')
        text = text[1:i]
        i = text.rfind('\n')
        text = text[1:i]
        text = text.replace(': другие произведения', '', 1)
        i = text.find('Журнал "Самиздат"')
        j = text.find('шедевр')
        delete = text[i:j + 7]
        text = text.replace(delete, '', 1)
        a = booklist.find(link)
        if a==-1:
            print(book)
            print('Загрузить книгу? \n 1 - Да \n 2 - Нет')
            b = input()
            if b=='1':
                open(locallink, 'w').write(text)
                booklist = booklist+((book)+';'+(link)+'\n')
                open('/home/a/Документы/samlib/data/booklist.txt', 'w').write(booklist)
                print('Книга загружена. Хотите вернуться в начало? \n 1 - Да \n 2 - Нет')
                b = input()
                if b == '1':
                    continue
                elif b == '2':
                    break
                else:
                    print('Неверное значение')
                    break
            elif b=='2':
                print('Загрузка отменена. Хотите вернуться в начало? \n 1 - Да \n 2 - Нет')
                b = input()
                if b=='1':
                    continue
                elif b=='2':
                    break
                else:
                    print('Неверное значение')
                    break
            else:
                print('Неверное значение')
                break
        else:
            print(book)
            print('Данная книга уже была загружена. Обновить? \n 1 - Да \n 2 - Нет')
            b = input()
            if b=='1':
                open('/home/a/Документы/samlib/data/test.txt', 'w').write(text)
                #booklist = booklist + ((book)+';'+(link)+'\n')
                #print('Книга загружена')
                oldtext = open(locallink, 'r').read()
                if len(oldtext)<len(text):
                    open(locallink, 'w').write(text)
                    print('Книга обновлена. Хотите вернуться в начало? \n 1 - Да \n 2 - Нет')
                    b = input()
                    if b == '1':
                        continue
                    elif b == '2':
                        break
                    else:
                        print('Неверное значение')
                        break
                elif len(oldtext)>len(text):
                    print('Ранее загруженная книга больше по размеру. Вы точно хотите её обновить? \n 1 - Да \n 2 - Нет')
                    b = input()
                    if b == '1':
                        open(locallink, 'w').write(text)
                        print('Книга обновлена. Хотите вернуться в начало? \n 1 - Да \n 2 - Нет')
                        b = input()
                        if b == '1':
                            continue
                        elif b == '2':
                            break
                        else:
                            print('Неверное значение')
                            break
                    elif b == '2':
                        print('Хотите вернуться в начало? \n 1 - Да \n 2 - Нет')
                        b = input()
                        if b == '1':
                            continue
                        elif b == '2':
                            break
                        else:
                            print('Неверное значение')
                            break
                    else:
                        print('Неверное значение')
                        break
                else:
                    print('Книга не нуждается в обновлении. Хотите вернуться в начало? \n 1 - Да \n 2 - Нет')
                    b = input()
                    if b == '1':
                        continue
                    elif b == '2':
                        break
                    else:
                        print('Неверное значение')
                        break
            elif b=='2':
                print('Обновление отменено. Хотите вернуться в начало? \n 1 - Да \n 2 - Нет')
                b=input()
                if b=='1':
                    continue
                elif b=='2':
                    break
                else:
                    print('Неверное значение')
                    break
            else:
                print('Неверное значение')
                break
    elif i=='2':
        x = 0
        err = 0
        def links(booklist):
            res = []
            for s in booklist.split("\n"):
                ss = s.strip().split(";")
                if len(ss) > 1:
                    res.append(ss[1])
            return res



        if len(booklist)<2:
            print('ОШИБКА! ДЛЯ НАЧАЛА ВРУЧНУЮ ЗАГРУЗИТЕ КНИГУ!')
            continue
        while m<len(links(booklist)):
            g = Grab(log_file='/home/a/Документы/samlib/data/out.html')
            g.go(links(booklist)[m])
            text = open('/home/a/Документы/samlib/data/out.html', 'r', encoding='cp1251').read()
            autor = g.xpath_text('//html/body/div/h3')
            name = g.xpath_text('//html/body/center/h2')
            book = autor + name
            book = book.replace(': другие произведения.', ' - ')
            locallink = ('/home/a/Документы/samlib/' + (book) + '.txt')
            TAG_RE = re.compile(r'<[^>]+>')
            def remove_tags(text):
                return TAG_RE.sub('', text)
            text = remove_tags(text)
            text = text.replace('&nbsp;', '')
            text = text.replace('&copy;', '')
            i = text.rfind('Copyright')
            text = text[1:i]
            # i = text.rfind('Комментарии:')
            # text = text[1:i]
            i = text.rfind('\n')
            text = text[1:i]
            i = text.rfind('\n')
            text = text[1:i]
            text = text.replace(': другие произведения', '', 1)
            i = text.find('Журнал "Самиздат"')
            j = text.find('шедевр')
            delete = text[i:j + 7]
            text = text.replace(delete, '', 1)
            open('/home/a/Документы/samlib/data/test.txt', 'w').write(text)
            try:
                oldtext = open(locallink, 'r').read()
            except FileNotFoundError:
                err = err+1
                open(locallink, 'w').write(text)
                log = log + ((book) + '. НЕ НАЙДЕНА\n')
                open('/home/a/Документы/samlib/data/log.txt', 'w').write(log)
            if len(oldtext) < len(text):
                open(locallink, 'w').write(text)
                t = t+1
                log = log + ((book)+' \n')
                open('/home/a/Документы/samlib/data/log.txt', 'w').write(log)
                m = m + 1
            elif len(oldtext) > len(text):
                x = x+1
                log = log + ((book) + '. Ранее загруженная книга больше\n')
                open('/home/a/Документы/samlib/data/log.txt', 'w').write(log)
                m = m + 1
            else:
                m = m+1
        if err==0:
            print('Библиотека обновлена. Всего книг:',m,'. Новых книг:',t,'. Старых больше размером:',x,'.\n Хотите вернуться в начало? \n 1 - Да \n 2 - Нет')
            b = input()
            if b == '1':
                continue
            elif b == '2':
                break
            else:
                print('Неверное значение')
                break
        else:
            print('\n ОШИБКА, ',err,' книг было не найдено и загружено заново.\nБиблиотека обновлена. Всего книг:', m, '. Новых книг:', t, '. Старых больше размером:', x,
                  '.\n Хотите вернуться в начало? \n 1 - Да \n 2 - Нет')
            b = input()
            if b == '1':
                continue
            elif b == '2':
                break
            else:
                print('Неверное значение')
                break


    else:
        print('Неверное значение')
        break
