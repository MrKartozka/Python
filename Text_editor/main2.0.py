import os
import tkinter
import tkinter.colorchooser
from tkinter import ttk, filedialog, TclError
from tkinter.scrolledtext import ScrolledText
from tkinter.font import Font, families
from tkinter import *
from tkinter import messagebox
import json

class TextEditor:

  def __init__(self,root):
    self.root = root
    self.root.title("Текстовый редактор")
    self.filename = None
    self.title = StringVar()
    self.savedict = {"text" : ""}

    #Создание надписи пути
    self.titlebar = Label(self.root,textvariable=self.title,font=("Arial",14),bd=2,relief=GROOVE)
    self.titlebar.pack(side=TOP,fill=BOTH)
    self.settitle()

    #Создание меню
    self.menubar = Menu(self.root,font=("Arial",14))
    self.root.config(menu=self.menubar)

    #Создание файла меню
    self.filemenu = Menu(self.menubar,font=("Arial",14),tearoff=0)
    self.filemenu.add_command(label="Новый",accelerator="Ctrl+N",command=self.newfile)
    self.filemenu.add_command(label="Открыть",accelerator="Ctrl+O",command=self.openfile)
    self.filemenu.add_command(label="Сохранить",accelerator="Ctrl+S",command=self.savefile)
    self.filemenu.add_command(label="Сохранить как",accelerator="Ctrl+A",command=self.saveasfile)

    self.menubar.add_cascade(label="Файл", menu=self.filemenu)

    #Создание редактора
    self.editmenu = Menu(self.menubar,font=("Arial",14),tearoff=0)
    self.editmenu.add_command(label="Вырезать",accelerator="Ctrl+X",command=self.cut)
    self.editmenu.add_command(label="Копировать",accelerator="Ctrl+C",command=self.copy)
    self.editmenu.add_command(label="Вставить",accelerator="Ctrl+V",command=self.paste)
    self.editmenu.add_command(label="Вернуть",accelerator="Ctrl+Z",command=self.undo)

    self.menubar.add_cascade(label="Функции", menu=self.editmenu)

    #Создание кнопки внешний вид
    self.formmenu = Menu(self.menubar, font=("Arial", 14), tearoff=0)
    self.formmenu.add_command(label="Цвет", command=self.color)
    self.formmenu.add_command(label="Шрифт: Bold", command=self.bold)
    self.formmenu.add_command(label="Шрифт: Italic", command=self.italic)
    self.formmenu.add_command(label="Подчёркивание", command=self.underline)
    self.formmenu.add_command(label="Зачёркивание", command=self.overstrike)

    self.menubar.add_cascade(label="Внешний вид", menu=self.formmenu)

    #Создание выхода
    self.exitmenu = Menu(self.menubar, font=("Arial", 14), tearoff=0)
    self.exitmenu.add_command(label="Выход", accelerator="Ctrl+E", command=self.exit)

    self.menubar.add_cascade(label="Выход", menu=self.exitmenu)

    #Полоса прокрутки
    scrol_y = Scrollbar(self.root,orient=VERTICAL)
    self.txtarea = Text(self.root,yscrollcommand=scrol_y.set,font=("Arial",14),state="normal",relief=GROOVE)
    scrol_y.pack(side=RIGHT,fill=Y)
    scrol_y.config(command=self.txtarea.yview)
    self.txtarea.pack(fill=BOTH,expand=1)

    #Вызов горячих кнопок
    self.shortcuts()

  def settitle(self): #безымянный документ
    if self.filename:
      self.title.set(self.filename)
    else:
      self.title.set("Здесь отображается путь файла при сохранении/открытии")

  def newfile(self,*args): #Функция создания нового фалйа
    self.txtarea.delete("1.0",END)
    self.filename = None
    self.settitle()

  def openfile(self,*args): #Функция отркрытия файла
    try:
      self.filename = filedialog.askopenfilename(title = "Select file",filetypes = (("All Files","*.*"),("Text Files","*.txt"),("Python Files","*.py")))
      if self.filename:
        #infile = open(self.filename,"r")
        with open('test_file.json', 'r') as j:
          self.savedict = json.load(j)
        infile = self.savedict["text"]
        self.txtarea.delete("1.0",END)
        for line in infile:
          self.txtarea.insert(END,line)
        #infile.close()
        self.settitle()
        if 'colortags' in self.savedict:
          for clr in self.savedict['colortags']:
            if clr != ['end']:
              self.txtarea.tag_add('color', clr[0], clr[1])
            else:
              break
          self.txtarea.tag_configure('color', foreground=self.savedict['color'])


    except Exception as e:
      messagebox.showerror("Exception",e)

  def savefile(self,*args): #Функция сохранить
    try:
      #Проверяет на наличие имя файла
      if self.filename:
        data = self.txtarea.get("1.0",END)
        self.savedict["text"] = data
        with open('test_file.json', 'w') as file:
          json.dump(self.savedict, file)
        #outfile = open(self.filename,"w")
        #outfile.write(data)
        #outfile.close()
        self.settitle()
      else:
        self.saveasfile()
    except Exception as e:
      messagebox.showerror("Exception",e)

  def saveasfile(self,*args): #Функция сохранить как
    #Добавление исключений
    try:
      untitledfile = filedialog.asksaveasfilename(title = "Сохранить как",defaultextension=".txt",initialfile = "Untitled.txt",filetypes = (("All Files","*.*"),("Text Files","*.txt"),("Python Files","*.py")))
      data = self.txtarea.get("1.0",END)
      outfile = open(untitledfile,"w")
      outfile.write(data)
      outfile.close()
      self.filename = untitledfile
      self.settitle()
    except Exception as e:
      messagebox.showerror("Exception",e)

  def exit(self,*args): #Функция выхода
    op = messagebox.askyesno("Предупреждение!", "Вы точно хотите выйти без сохранения?")
    if op>0:
      self.root.destroy()
    else:
      return

  def cut(self,*args): #Функция копирования
    self.txtarea.event_generate("<<Вырезать>>")

  def copy(self,*args): #Функция копировать
          self.txtarea.event_generate("<<Копировать>>")

  def paste(self,*args): #Функция вставить
    self.txtarea.event_generate("<<Вставить>>")

  def undo(self,*args): #Функция возврата
    try:
      #идёт проверка если имя файла не найдено
      if self.filename:
        self.txtarea.delete("1.0",END)
        infile = open(self.filename,"r")
        for line in infile:
          self.txtarea.insert(END,line)
        infile.close()
        self.settitle()
      else:
        self.txtarea.delete("1.0",END)
        self.filename = None
        self.settitle()
    except Exception as e:
      messagebox.showerror("Exception",e)

  def color(self):
    try:
        (rgb, hx) = tkinter.colorchooser.askcolor()
        self.txtarea.tag_add('color', 'sel.first', 'sel.last')
        self.savedict['color'] = hx
        if 'colortags' in self.savedict:
          clrs = list(self.savedict['colortags'])
          clrs.remove(['end'])
          clrs.append((self.txtarea.index("sel.first"), self.txtarea.index("sel.last")))
          clrs.append(['end'])
          self.savedict['colortags'] = clrs
        else:
          clrs = []
          clrs.append((self.txtarea.index("sel.first"), self.txtarea.index("sel.last")))
          clrs.append(['end'])
          self.savedict['colortags'] = clrs

          #self.savedict['colortags'] = (self.txtarea.index("sel.first"), self.txtarea.index("sel.last"))
        #self.txtarea.index("sel.first")#индекс начала тега
        #self.txtarea.index("sel.last")#индекс конца
        self.txtarea.tag_configure('color', foreground=hx)
    except TclError:
        pass

  def bold(self, *args):
    try:
        current_tags = self.txtarea.tag_names("sel.first")
        if "bold" in current_tags:
          self.txtarea.tag_remove("bold", "sel.first", "sel.last")
        else:
          self.txtarea.tag_add("bold", "sel.first", "sel.last")
          bold_font = Font(self.txtarea, self.txtarea.cget("font"))
          bold_font.configure(weight="bold")
          self.txtarea.tag_configure("bold", font=bold_font)
    except TclError:
        pass

  def italic(self, *args):
    try:
        current_tags = self.txtarea.tag_names("sel.first")
        if "italic" in current_tags:
          self.txtarea.tag_remove("italic", "sel.first", "sel.last")
        else:
          self.txtarea.tag_add("italic", "sel.first", "sel.last")
          italic_font = Font(self.txtarea, self.txtarea.cget("font"))
          italic_font.configure(slant="italic")
          self.txtarea.tag_configure("italic", font=italic_font)
    except TclError:
        pass

  def underline(self, *args):
    try:
        current_tags = self.txtarea.tag_names("sel.first")
        if "underline" in current_tags:
          self.txtarea.tag_remove("underline", "sel.first", "sel.last")
        else:
          self.txtarea.tag_add("underline", "sel.first", "sel.last")
          underline_font = Font(self.txtarea, self.txtarea.cget("font"))
          underline_font.configure(underline=1)
          self.txtarea.tag_configure("underline", font=underline_font)
    except TclError:
        pass

  def overstrike(self, *args):
    try:
        current_tags = self.txtarea.tag_names("sel.first")
        if "overstrike" in current_tags:
          self.txtarea.tag_remove("overstrike", "sel.first", "sel.last")
        else:
          self.txtarea.tag_add("overstrike", "sel.first", "sel.last")
          overstrike_font = Font(self.txtarea, self.txtarea.cget("font"))
          overstrike_font.configure(overstrike=1)
          self.txtarea.tag_configure("overstrike", font=overstrike_font)
    except TclError:
        pass

  def shortcuts(self): # Определение горячих клавиш
    self.txtarea.bind("<Control-n>",self.newfile)
    self.txtarea.bind("<Control-o>",self.openfile)
    self.txtarea.bind("<Control-s>",self.savefile)
    self.txtarea.bind("<Control-a>",self.saveasfile)
    self.txtarea.bind("<Control-e>",self.exit)
    self.txtarea.bind("<Control-x>",self.cut)
    self.txtarea.bind("<Control-c>",self.copy)
    self.txtarea.bind("<Control-v>",self.paste)
    self.txtarea.bind("<Control-z>",self.undo)

root = Tk()
TextEditor(root)
root.mainloop() #Вызов интерфейса