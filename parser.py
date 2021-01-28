import csv
from tkinter.filedialog import *
from tkinter import *
from tkinter import messagebox as mb
import numpy as N


def open_file():
    try:
        file = askopenfile(mode='r', filetypes=[('CSV files', '*.csv')])
        pars = csv.DictReader(file, delimiter=';')
        message = []
        parser = 'idps'
        signature = []
        for row in pars:
            message.append(row['message'])
        for line in message:
            if parser in line:
                signature_list = line.split('|')
                signature.extend(signature_list[5:6])
        uniq = list(set(signature))
        array_d = {}.fromkeys(uniq, 0)
        for a in signature:
            array_d[a] += 1
        cont = list(array_d.values())
        columns = ['Signature', 'count']
        with open('result.csv', 'w', newline='', encoding='utf-8') as file_obj:
            write = csv.writer(file_obj)
            write.writerow(columns)
            write.writerows(zip(uniq, cont))
        mb.showinfo(title='Информация', message='Готово')
    except:
        pass


def result_signature():
    try:
        sign = []
        with open('result.csv') as file:
            read = csv.DictReader(file, delimiter=',')
            for row in read:
                sign.append(row['Signature'])
        str(sign)
        root = Tk()
        root.resizable(width=False, height=False)
        root.geometry('800x500')
        root.title('Сигнатуры')
        root['bg'] = '#ccc'
        field = Text(root, width=80, height=50, wrap=WORD,
                     font='Arial 10')
        field.insert(0.0, f'\n'.join(sign))
        field.pack()
        root.mainloop()
    except FileNotFoundError:
        mb.showerror(title='Ошибка', message='Файл не найден')


def events():
    try:
        all_events = []
        old_events = []
        with open('all_sig.txt') as file:
            for line in file:
                rep = line.replace('\n', '')
                all_events.append(rep)
        with open('result.csv') as file_obj:
            reader = csv.DictReader(file_obj, delimiter=',')
            for row in reader:
                old_events.append(row['Signature'])
        result = list(set(old_events) - set(all_events))
        result.sort()
        counter = len(result)
        if len(result) == 0:
            mb.showinfo(title='Внимание', message='Новых сигнатур нет')
        else:
            root = Tk()
            root.resizable(width=False, height=False)
            root.geometry('800x500')
            root.title('Новых сигнатур  ' + str(counter))
            root['bg'] = '#ccc'
            field = Text(root, width=80, height=50, wrap=WORD,
                         font='Arial 10')
            field.insert(0.0, f'\n'.join(result))
            field.pack()
            root.mainloop()
            with open('all_sig.txt', 'a') as file:
                file.write('\n'.join(result))
    except FileNotFoundError:
        mb.showerror(title='Ошибка', message='Файл не найден')


def src_ip():
    def get():
        signature = name.get()
        file = askopenfile(mode='r', filetypes=[('CSV files', '*.csv')])
        pars = csv.DictReader(file, delimiter=';')
        message = []
        sor_ip = []
        print(signature)
        for row in pars:
            message.append(row['message'])
        for line in message:
            if signature in line:
                src_ip = line.split('=')
                sor_ip.extend(src_ip[10:11])
        res = N.array(sor_ip)
        unque_res = N.unique(res)
        res = f'\n'.join(unque_res)
        syka = res.replace('spt', '')
        root = Tk()
        root.resizable(width=False, height=False)
        root.geometry('800x500')
        root.title('SRC IP')
        root['bg'] = '#ccc'
        field = Text(root, width=80, height=50, wrap=WORD,
                     font='Arial 10')
        field.insert(0.0, syka)
        field.pack()
        root.mainloop()

    roof = Tk()
    roof.title("Поиск SRC ip")

    name = StringVar()

    name_label = Label(roof, text="Введите сигнатуру:")

    name_label.grid(row=0, column=0, sticky="w")

    name_entry = Entry(textvariable=name)
    name_entry.grid(row=0, column=1, padx=5, pady=5)
    message_button = Button(roof, text="Click Me", command=get)
    message_button.grid(row=2, column=1, padx=5, pady=5, sticky="e")
    roof.mainloop()


def gui():
    root = Tk()
    root.geometry("250x150+300+300")
    root.title('Парсер логов')
    btn = Button(root, text='Спарсить файл', command=open_file)
    btn_info = Button(root, text='Показать сигнатуры', command=result_signature)
    new_sign = Button(root, text='Найти новые сигнатуры', command=events)
    srt_butn = Button(root, text='Найти src.ip', command=src_ip)
    srt_butn.grid(column=1, row=1)
    btn_info.grid(column=0, row=2)
    btn.grid(column=0, row=1)
    new_sign.grid(column=0, row=3)

    root.mainloop()

gui()

