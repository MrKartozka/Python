import os
import tkinter
import tkinter.colorchooser
from tkinter import ttk, filedialog, TclError
from tkinter.scrolledtext import ScrolledText
from tkinter.font import Font, families
from tkinter import *
from tkinter import messagebox
import json
class Hystory:
  def __init__(self):
    self.dict = {"text" : ""}


class TextEditor:
  def __init__(self,root):
    self.root = root
    self.root.title("Текстовый редактор")
    self.filename = None
    self.title = StringVar()
    hystory = {"text" : ""}
    self.story = list()
    self.story.append(hystory)
    self.num_story = 1
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
    self.filemenu.add_separator()
    self.filemenu.add_command(label="Выход", accelerator="Ctrl+E", command=self.exit)
    #Создание редактора
    self.editmenu = Menu(self.menubar,font=("Arial",14),tearoff=0)
    self.editmenu.add_command(label="Вырезать",accelerator="Ctrl+X",command=self.cut)
    self.editmenu.add_command(label="Копировать",accelerator="Ctrl+C",command=self.copy)
    self.editmenu.add_command(label="Вставить",accelerator="Ctrl+V",command=self.paste)
    self.editmenu.add_command(label="Вернуть",accelerator="Ctrl+Z",command=self.undo)
    self.editmenu.add_command(label="Повторить",accelerator="Ctrl+Y",command=self.redo)
    self.menubar.add_cascade(label="Правка", menu=self.editmenu)
    #Создание кнопки внешний вид
    self.formmenu = Menu(self.menubar, font=("Arial", 14), tearoff=0)
    self.formmenu.add_command(label="Цвет", command=self.color)
    self.formmenu.add_command(label="Задний фон", command=self.bg_color)
    self.formmenu.add_separator()
    self.formmenu.add_command(label="Шрифт: Bold", command=self.bold)
    self.formmenu.add_command(label="Шрифт: Italic", command=self.italic)
    self.formmenu.add_separator()
    self.formmenu.add_command(label="Подчёркивание", command=self.underline)
    self.formmenu.add_command(label="Зачёркивание", command=self.overstrike)
    self.menubar.add_cascade(label="Формат", menu=self.formmenu)
    #Справка
    self.helpmenu = Menu(self.menubar, font=("Arial", 14), tearoff=0)
    self.helpmenu.add_command(label="Справка", command=self.infoabout)
    self.menubar.add_cascade(label="О программе", menu=self.helpmenu)
    #Полоса прокрутки
    scrol_y = Scrollbar(self.root,orient=VERTICAL)
    self.txtarea = Text(self.root,yscrollcommand=scrol_y.set,font=("Arial",14),state="normal",relief=GROOVE)
    self.txtarea.bind('<Return>', self.changetext)
    self.txtarea.bind('<space>', self.changetext)
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
    if 'colortags' in self.story[0].dict:
      self.story[0].dict.pop('colortags')
    if 'color' in self.story[0].dict:
      self.story[0].dict.pop('color')
    if 'bold' in self.story[0].dict:
      self.story[0].dict.pop('bold')
    if 'italic' in self.story[0].dict:
      self.story[0].dict.pop('italic')
    if 'underline' in self.story[0].dict:
      self.story[0].dict.pop('underline')
    if 'overstrike' in self.story[0].dict:
      self.story[0].dict.pop('overstrike')

  def changetext(self,*args):
    if self.num_story < 10:
          h = self.story[-1]
          self.story.append(h)
          self.num_story +=1
    else:
          self.story.pop(0)
          h = self.story[-1]
          self.story.append(h)

    data = self.txtarea.get("1.0",END)
    self.story[-1].dict["text"] = data
  
  def openfile(self,*args): #Функция отркрытия файла
    try:
      self.filename = filedialog.askopenfilename(title = "Select file",filetypes = [("Text Files","*.json")])
      if self.filename:
        with open(self.filename, 'r') as j:
          self.story[0].dict = json.load(j)
        infile = self.story[0].dict["text"]
        self.txtarea.delete("1.0",END)
        for line in infile:
          self.txtarea.insert(END,line)
        self.settitle()
        if 'colortags' in self.story[0].dict:
          for clr in self.story[0].dict['colortags']:
            if clr != ['end']:
              self.txtarea.tag_add('color', clr[0], clr[1])
          self.txtarea.tag_configure('color', foreground=self.story['color'])
        if 'bg_color' in self.story[0].dict:
          self.txtarea.config(bg=self.story[0].dict['bg_color'])
        if 'bold' in self.story[0].dict:
          for bld in self.story[0].dict['bold']:
            if bld != ['end']:
              self.txtarea.tag_add('bold', bld[0], bld[1])
              bold_font = Font(self.txtarea, self.txtarea.cget("font"))
              bold_font.configure(weight="bold")
              self.txtarea.tag_configure("bold", font=bold_font)
        if 'italic' in self.story[0].dict:
          for bld in self.story[0].dict['italic']:
            if bld != ['end']:
              self.txtarea.tag_add('italic', bld[0], bld[1])
              italic_font = Font(self.txtarea, self.txtarea.cget("font"))
              italic_font.configure(slant="italic")
              self.txtarea.tag_configure("italic", font=italic_font)
        if 'underline' in self.story[0].dict:
          for bld in self.story[0].dict['underline']:
            if bld != ['end']:
              self.txtarea.tag_add('underline', bld[0], bld[1])
              underline_font = Font(self.txtarea, self.txtarea.cget("font"))
              underline_font.configure(underline=1)
              self.txtarea.tag_configure("underline", font=underline_font)
        if 'overstrike' in self.story[0].dict:
          for bld in self.story[0].dict['overstrike']:
            if bld != ['end']:
              self.txtarea.tag_add('overstrike', bld[0], bld[1])
              overstrike_font = Font(self.txtarea, self.txtarea.cget("font"))
              overstrike_font.configure(overstrike=1)
              self.txtarea.tag_configure("overstrike", font=overstrike_font)
    except Exception as e:
      messagebox.showerror("Exception",e)
  def savefile(self,*args): #Функция сохранить
    try:
      #Проверяет на наличие имя файла
      if self.filename:
        data = self.txtarea.get("1.0",END)
        self.story[-1].dict["text"] = data
        with open(self.filename, 'w') as file:
          json.dump(self.story[-1].dict, file)
        self.settitle()
      else:
        self.saveasfile()
    except Exception as e:
      messagebox.showerror("Exception",e)
  def saveasfile(self,*args): #Функция сохранить как
    #Добавление исключений
    try:
      untitledfile = filedialog.asksaveasfilename(title = "Сохранить как",defaultextension=".json",initialfile = "Text.json",filetypes = [("Text Files","*.json")])
      data = self.txtarea.get("1.0",END)
      self.story[-1].dict["text"] = data
      with open(untitledfile, 'w') as file:
        json.dump(self.story[-1].dict, file)
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

  def undo(self,*args):
    #self.undo_redo(undo=True)
    if self.num_story > 2:
        self.num_story -= 1
    else:
        pass

    infile = self.story[self.num_story-1].dict["text"]
    self.txtarea.delete("1.0",END)
    for line in infile:
          self.txtarea.insert(END,line)
    self.settitle()
    #for nm in self.txtarea.tag_names:
    self.txtarea.tag_delete(self.txtarea.tag_names)
    if 'colortags' in self.story[self.num_story-1].dict:
          for clr in self.story[self.num_story-1].dict['colortags']:
            if clr != ['end']:
              self.txtarea.tag_add('color', clr[0], clr[1])
          self.txtarea.tag_configure('color', foreground=self.story[self.num_story-1].dict['color'])
    if 'bg_color' in self.story[self.num_story-1].dict:
          self.txtarea.config(bg=self.story[self.num_story-1].dict['bg_color'])
    if 'bold' in self.story[self.num_story-1].dict:
          for bld in self.story[self.num_story-1].dict['bold']:
            if bld != ['end']:
              self.txtarea.tag_add('bold', bld[0], bld[1])
              bold_font = Font(self.txtarea, self.txtarea.cget("font"))
              bold_font.configure(weight="bold")
              self.txtarea.tag_configure("bold", font=bold_font)
    if 'italic' in self.story[self.num_story-1].dict:
          for bld in self.story[self.num_story-1].dict['italic']:
            if bld != ['end']:
              self.txtarea.tag_add('italic', bld[0], bld[1])
              italic_font = Font(self.txtarea, self.txtarea.cget("font"))
              italic_font.configure(slant="italic")
              self.txtarea.tag_configure("italic", font=italic_font)
    if 'underline' in self.story[self.num_story-1].dict:
          for bld in self.story[self.num_story-1].dict['underline']:
            if bld != ['end']:
              self.txtarea.tag_add('underline', bld[0], bld[1])
              underline_font = Font(self.txtarea, self.txtarea.cget("font"))
              underline_font.configure(underline=1)
              self.txtarea.tag_configure("underline", font=underline_font)
    if 'overstrike' in self.story[self.num_story-1].dict:
          for bld in self.story[self.num_story-1].dict['overstrike']:
            if bld != ['end']:
              self.txtarea.tag_add('overstrike', bld[0], bld[1])
              overstrike_font = Font(self.txtarea, self.txtarea.cget("font"))
              overstrike_font.configure(overstrike=1)
              self.txtarea.tag_configure("overstrike", font=overstrike_font)

  def redo(self,*args):
    #self.undo_redo(undo=False)


    if self.num_story < 10:
        self.num_story += 1
    else:
        pass

    infile = self.story[self.num_story-1].dict["text"]
    self.txtarea.delete("1.0",END)
    for line in infile:
          self.txtarea.insert(END,line)
    self.settitle()
    self.txtarea.tag_delete(self.txtarea.tag_names)
    if 'colortags' in self.story[self.num_story-1].dict:
          for clr in self.story[self.num_story-1].dict['colortags']:
            if clr != ['end']:
              self.txtarea.tag_add('color', clr[0], clr[1])
          self.txtarea.tag_configure('color', foreground=self.story[self.num_story-1].dict['color'])
    if 'bg_color' in self.story[self.num_story-1].dict:
          self.txtarea.config(bg=self.story[self.num_story-1].dict['bg_color'])
    if 'bold' in self.story[self.num_story-1].dict:
          for bld in self.story[self.num_story-1].dict['bold']:
            if bld != ['end']:
              self.txtarea.tag_add('bold', bld[0], bld[1])
              bold_font = Font(self.txtarea, self.txtarea.cget("font"))
              bold_font.configure(weight="bold")
              self.txtarea.tag_configure("bold", font=bold_font)
    if 'italic' in self.story[self.num_story-1].dict:
          for bld in self.story[self.num_story-1].dict['italic']:
            if bld != ['end']:
              self.txtarea.tag_add('italic', bld[0], bld[1])
              italic_font = Font(self.txtarea, self.txtarea.cget("font"))
              italic_font.configure(slant="italic")
              self.txtarea.tag_configure("italic", font=italic_font)
    if 'underline' in self.story[self.num_story-1].dict:
          for bld in self.story[self.num_story-1].dict['underline']:
            if bld != ['end']:
              self.txtarea.tag_add('underline', bld[0], bld[1])
              underline_font = Font(self.txtarea, self.txtarea.cget("font"))
              underline_font.configure(underline=1)
              self.txtarea.tag_configure("underline", font=underline_font)
    if 'overstrike' in self.story[self.num_story-1].dict:
          for bld in self.story[self.num_story-1].dict['overstrike']:
            if bld != ['end']:
              self.txtarea.tag_add('overstrike', bld[0], bld[1])
              overstrike_font = Font(self.txtarea, self.txtarea.cget("font"))
              overstrike_font.configure(overstrike=1)
              self.txtarea.tag_configure("overstrike", font=overstrike_font)


  def undo_redo(self,*args, undo = True): #Функция возврата, повтора
    if undo == True: #воврат
      if self.num_story > 1:
        self.num_story -= 1
      else:
        pass
    else: #повтор
      if self.num_story < 10:
        self.num_story += 1
      else:
        pass

    infile = self.story[self.num_story-1].dict["text"]
    self.txtarea.delete("1.0",END)
    for line in infile:
          self.txtarea.insert(END,line)
    self.settitle()
    if 'colortags' in self.story[self.num_story-1].dict:
          for clr in self.story[self.num_story-1].dict['colortags']:
            if clr != ['end']:
              self.txtarea.tag_add('color', clr[0], clr[1])
          self.txtarea.tag_configure('color', foreground=self.story[self.num_story-1].dict['color'])
    if 'bg_color' in self.story[self.num_story-1].dict:
          self.txtarea.config(bg=self.story[self.num_story-1].dict['bg_color'])
    if 'bold' in self.story[self.num_story-1].dict:
          for bld in self.story[self.num_story-1].dict['bold']:
            if bld != ['end']:
              self.txtarea.tag_add('bold', bld[0], bld[1])
              bold_font = Font(self.txtarea, self.txtarea.cget("font"))
              bold_font.configure(weight="bold")
              self.txtarea.tag_configure("bold", font=bold_font)
    if 'italic' in self.story[self.num_story-1].dict:
          for bld in self.story[self.num_story-1].dict['italic']:
            if bld != ['end']:
              self.txtarea.tag_add('italic', bld[0], bld[1])
              italic_font = Font(self.txtarea, self.txtarea.cget("font"))
              italic_font.configure(slant="italic")
              self.txtarea.tag_configure("italic", font=italic_font)
    if 'underline' in self.story[self.num_story-1].dict:
          for bld in self.story[self.num_story-1].dict['underline']:
            if bld != ['end']:
              self.txtarea.tag_add('underline', bld[0], bld[1])
              underline_font = Font(self.txtarea, self.txtarea.cget("font"))
              underline_font.configure(underline=1)
              self.txtarea.tag_configure("underline", font=underline_font)
    if 'overstrike' in self.story[self.num_story-1].dict:
          for bld in self.story[self.num_story-1].dict['overstrike']:
            if bld != ['end']:
              self.txtarea.tag_add('overstrike', bld[0], bld[1])
              overstrike_font = Font(self.txtarea, self.txtarea.cget("font"))
              overstrike_font.configure(overstrike=1)
              self.txtarea.tag_configure("overstrike", font=overstrike_font)
    #try:
      #идёт проверка если имя файла не найдено
    #   if self.filename:
    #     self.txtarea.delete("1.0",END)
    #     infile = open(self.filename,"r")
    #     for line in infile:
    #       self.txtarea.insert(END,line)
    #     infile.close()
    #     self.settitle()
    #   else:
    #     self.txtarea.delete("1.0",END)
    #     self.filename = None
    #     self.settitle()
    # except Exception as e:
    #   messagebox.showerror("Exception",e)


  def color(self):
    try:
        (rgb, hx) = tkinter.colorchooser.askcolor()
        self.txtarea.tag_add('color', 'sel.first', 'sel.last')
        if self.num_story < 10:
          h = self.story[-1]
          self.story.append(h)
          self.num_story +=1
        else:
          self.story.pop(0)
          h = self.story[-1]
          self.story.append(h)
        self.story[-1].dict['color'] = hx
        if 'colortags' in self.story[-1].dict:
          clrs = list(self.story[-1].dict['colortags'])
          clrs.remove(['end'])
          clrs.append((self.txtarea.index("sel.first"), self.txtarea.index("sel.last")))
          clrs.append(['end'])
          self.story[-1].dict['colortags'] = clrs
        else:
          clrs = []
          clrs.append((self.txtarea.index("sel.first"), self.txtarea.index("sel.last")))
          clrs.append(['end'])
          self.story[-1].dict['colortags'] = clrs
        self.txtarea.tag_configure('color', foreground=hx)
    except TclError:
        pass
  def bg_color(self):
    my_color = tkinter.colorchooser.askcolor()[1]
    if self.num_story < 10:
          h = self.story[-1]
          self.story.append(h)
          self.num_story +=1
    else:
          self.story.pop(0)
          h = self.story[-1]
          self.story.append(h)
    if my_color:
      self.txtarea.config(bg=my_color)
      self.story[-1].dict['bg_color'] = my_color
  def bold(self, *args):
    try:
        current_tags = self.txtarea.tag_names("sel.first")
        if self.num_story < 10:
          h = self.story[-1]
          self.story.append(h)
          self.num_story +=1
        else:
          self.story.pop(0)
          h = self.story[-1]
          self.story.append(h)
        if "bold" in current_tags:
          self.txtarea.tag_remove("bold", "sel.first", "sel.last")
          bl = list(self.story[-1].dict['bold'])
          bl.remove((self.txtarea.index("sel.first"), self.txtarea.index("sel.last")))
          self.story['bold'] = bl
        else:
          self.txtarea.tag_add("bold", "sel.first", "sel.last")
          bold_font = Font(self.txtarea, self.txtarea.cget("font"))
          bold_font.configure(weight="bold")
          self.txtarea.tag_configure("bold", font=bold_font)
          if 'bold' in self.story[-1].dict:
            bl = list(self.story[-1].dict['bold'])
            bl.remove(['end'])
            bl.append((self.txtarea.index("sel.first"), self.txtarea.index("sel.last")))
            bl.append(['end'])
            self.story[-1].dict['bold'] = bl
          else:
            bl = []
            bl.append((self.txtarea.index("sel.first"), self.txtarea.index("sel.last")))
            bl.append(['end'])
            self.story[-1].dict['bold'] = bl
    except TclError:
        pass
  def italic(self, *args):
    try:
        current_tags = self.txtarea.tag_names("sel.first")
        if self.num_story < 10:
          h = self.story[-1]
          self.story.append(h)
          self.num_story +=1
        else:
          self.story.pop(0)
          h = self.story[-1]
          self.story.append(h)
        if "italic" in current_tags:
          self.txtarea.tag_remove("italic", "sel.first", "sel.last")
          it = list(self.story[-1].dict['italic'])
          it.remove((self.txtarea.index("sel.first"), self.txtarea.index("sel.last")))
          self.story['italic'] = it
        else:
          self.txtarea.tag_add("italic", "sel.first", "sel.last")
          italic_font = Font(self.txtarea, self.txtarea.cget("font"))
          italic_font.configure(slant="italic")
          self.txtarea.tag_configure("italic", font=italic_font)
          if 'italic' in self.story[-1].dict:
            it = list(self.story['italic'])
            it.remove(['end'])
            it.append((self.txtarea.index("sel.first"), self.txtarea.index("sel.last")))
            it.append(['end'])
            self.story[-1].dict['italic'] = it
          else:
            it = []
            it.append((self.txtarea.index("sel.first"), self.txtarea.index("sel.last")))
            it.append(['end'])
            self.story[-1].dict['italic'] = it
    except TclError:
        pass
  def underline(self, *args):
    try:
        current_tags = self.txtarea.tag_names("sel.first")
        if self.num_story < 10:
          h = self.story[-1]
          self.story.append(h)
          self.num_story +=1
        else:
          self.story.pop(0)
          h = self.story[-1]
          self.story.append(h)
        if "underline" in current_tags:
          self.txtarea.tag_remove("underline", "sel.first", "sel.last")
          ul = list(self.story[-1].dict['underline'])
          ul.remove((self.txtarea.index("sel.first"), self.txtarea.index("sel.last")))
          self.story[-1].dict['underline'] = ul
        else:
          self.txtarea.tag_add("underline", "sel.first", "sel.last")
          underline_font = Font(self.txtarea, self.txtarea.cget("font"))
          underline_font.configure(underline=1)
          self.txtarea.tag_configure("underline", font=underline_font)
          if 'underline' in self.story[-1].dict:
            ul = list(self.story[-1].dict['underline'])
            ul.remove(['end'])
            ul.append((self.txtarea.index("sel.first"), self.txtarea.index("sel.last")))
            ul.append(['end'])
            self.story[-1].dict['underline'] = ul
          else:
            ul = []
            ul.append((self.txtarea.index("sel.first"), self.txtarea.index("sel.last")))
            ul.append(['end'])
            self.story[-1].dict['underline'] = ul
    except TclError:
        pass
  def overstrike(self, *args):
    try:
        current_tags = self.txtarea.tag_names("sel.first")
        if self.num_story < 10:
          h = self.story[-1]
          self.story.append(h)
          self.num_story +=1
        else:
          self.story.pop(0)
          h = self.story[-1]
          self.story.append(h)
        if "overstrike" in current_tags:
          self.txtarea.tag_remove("overstrike", "sel.first", "sel.last")
          os = list(self.story[-1].dict['overstrike'])
          os.remove((self.txtarea.index("sel.first"), self.txtarea.index("sel.last")))
          self.story[-1].dict['overstrike'] = os
        else:
          self.txtarea.tag_add("overstrike", "sel.first", "sel.last")
          overstrike_font = Font(self.txtarea, self.txtarea.cget("font"))
          overstrike_font.configure(overstrike=1)
          self.txtarea.tag_configure("overstrike", font=overstrike_font)
          if 'overstrike' in self.story[-1].dict:
            os = list(self.story[-1].dict['overstrike'])
            os.remove(['end'])
            os.append((self.txtarea.index("sel.first"), self.txtarea.index("sel.last")))
            os.append(['end'])
            self.story[-1].dict['overstrike'] = os
          else:
            os = []
            os.append((self.txtarea.index("sel.first"), self.txtarea.index("sel.last")))
            os.append(['end'])
            self.story[-1].dict['overstrike'] = os
    except TclError:
        pass
  def infoabout(self):  #Справка действие
    messagebox.showinfo("Наш текстовый редактор", "Мы написали текстовый редактор\nс помощью языка Python.")
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