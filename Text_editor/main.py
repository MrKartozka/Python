import tkinter
import tkinter as tk
import tkinter.messagebox as mb
from tkinter import *
from tkinter.filedialog import asksaveasfile, askopenfile #для открытия, закрытия файлов
from tkinter.messagebox import showerror #для отображения ошибок
from tkinter.font import families
from tkinter import messagebox

#fl_save = False

FILE_NAME = tkinter.NONE

def new_file():
    global FILE_NAME
    FILE_NAME = "Untitled"
    text.delete('1.0', tkinter.END)
    # fl_save = False

def save_file():
    data = text.get('1.0', tkinter.END)
    out = open(FILE_NAME, 'w')
    out.write(data)
    out.close()
    # fl_save = True

def save_as():
    out = asksaveasfile(mode='w', defaultextension='txt')
    data = text.get('1.0', tkinter.END)
    try:
        out.write(data.rstrip())
    except Exception:
        showerror(title="Ошибка", message="Нельзя сохранить")
    # fl_save = True

def open_file():
    global FILE_NAME
    inp = askopenfile(mode="r")
    if inp is None:
        return
    FILE_NAME = inp.name
    data = inp.read()
    text.delete('1.0', tkinter.END)
    text.insert('1.0', data)
    # fl_save = False

def on_closing():
    if messagebox.askokcancel("Выход", "Файл не сохранён, продолжить?"):
        root.destroy()

root = tkinter.Tk()
root.title("Текстовый документ")

root.minsize(width=1000, height=600) #размер окна
root.maxsize(width=1000, height=600)

text = tkinter.Text(root, width=400, height=400, wrap="word") #размер текстового поля
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

menuBar.add_cascade(label="Файл", menu=fileMenu)
menuBar.add_cascade(label="Выход", command=root.quit)
root.config(menu=menuBar)

#if fl_save == False:
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop() #вызов интерфейса
