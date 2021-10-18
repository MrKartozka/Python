import tkinter
import tkinter as tk
import tkinter.messagebox as mb
from tkinter import *
from tkinter.filedialog import asksaveasfile, askopenfile #для открытия, закрытия файлов
from tkinter.messagebox import showerror #для отображения ошибок
from tkinter.font import families
from tkinter import messagebox
import tkinter.colorchooser

FILE_NAME = tkinter.NONE
check_save = False

def new_file():
    global FILE_NAME
    FILE_NAME = "Untitled"
    text.delete('1.0', tkinter.END)
    global check_save
    check_save = False

def save_file():
    data = text.get('1.0', tkinter.END)
    out = open(FILE_NAME, 'w')
    out.write(data)
    out.close()
    global check_save
    check_save = True

def save_as():
    out = asksaveasfile(mode='w', defaultextension='txt')
    data = text.get('1.0', tkinter.END)
    try:
        out.write(data.rstrip())
    except Exception:
        showerror(title="Ошибка", message="Нельзя сохранить")
    global check_save
    check_save = True

def open_file():
    global FILE_NAME
    inp = askopenfile(mode="r")
    if inp is None:
        return
    FILE_NAME = inp.name
    data = inp.read()
    text.delete('1.0', tkinter.END)
    text.insert('1.0', data)
    global check_save
    check_save = False

def on_closing():
    global check_save
    if tkinter.Text.edit_modified(text) == True:
        if check_save == False:
            if messagebox.askokcancel("Выход", "Файл не сохранён, продолжить?"):
                root.destroy()
        else:
            root.destroy()
    else:
        root.destroy()

def color():
        try:
            (rgb, hx) = tkinter.colorchooser.askcolor()
            text.tag_add('color', 'sel.first', 'sel.last')
            text.tag_configure('color', foreground=hx)
        except TclError:
            pass

def undo():
    try:
        text.edit_undo()
    except TclError:
        pass

def redo():
    try:
        text.edit_redo()
    except TclError:
        pass

root = tkinter.Tk()
root.title("Текстовый документ")

root.minsize(width=1000, height=600) #размер окна
root.maxsize(width=1000, height=600)

text = tkinter.Text(root, width=400, height=400, wrap="word", undo=True, font="times") #размер текстового поля, перенос по словам, возможность отмены/повтора.
scrollb = Scrollbar(root, orient=VERTICAL, command=text.yview)
scrollb.pack(side="right", fill="y")
text.configure(yscrollcommand=scrollb.set)

text.pack() #отображение интерфейса
menuBar = tkinter.Menu(root) #вызов на главном окне меню
fileMenu = tkinter.Menu(menuBar, tearoff=0) #хранить вызов функции меню
fileMenu.add_command(label="Новый", command=new_file) #добавление 4-х кнопок
fileMenu.add_command(label="Открыть", command=open_file)
fileMenu.add_command(label="Сохранить", command=save_file)
fileMenu.add_command(label="Сохранить как", command=save_as)

EditMenu = tkinter.Menu(menuBar, tearoff=0)
EditMenu.add_command(label="Отменить", command=undo, accelerator="Ctrl+Z")
EditMenu.add_command(label="Повторить", command=redo, accelerator="Ctrl+Y")
EditMenu.add_command(label="Цвет", command=color)

menuBar.add_cascade(label="Файл", menu=fileMenu)
menuBar.add_cascade(label="Правка", menu=EditMenu)
menuBar.add_cascade(label="Выход", command=on_closing)
root.config(menu=menuBar)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop() #вызов интерфейса
