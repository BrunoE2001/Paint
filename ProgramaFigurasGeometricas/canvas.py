import tkinter as tk
import pyautogui
from tkinter import *
from tkinter import Canvas
from PIL import ImageDraw, Image, ImageTk
from tkinter.colorchooser import askcolor

class App(tk.Frame):
    
    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'black'
    
    def __init__(self, master):
        super().__init__(master)
        self.pack()
        master.title("GEOMETRIC FIGURES")
        master.iconphoto(False, tk.PhotoImage(file='img/icono.png'))
        self.setWindowSize()
        self.createcanvas()
        self.options()
        self.menu_Figures()
        self.menu_Lateral()

    def setWindowSize(self):
        canvas.geometry("600x600")
        canvas.update_idletasks()
        self.width = canvas.winfo_width()
        frm_width = canvas.winfo_rootx() - canvas.winfo_x()
        win_width = self.width + 2 * frm_width
        self.height = canvas.winfo_height()
        titlebar_height = canvas.winfo_rooty() - canvas.winfo_y()
        win_height = self.height + titlebar_height + frm_width
        self.x = canvas.winfo_screenwidth() // 2 - win_width // 2
        self.y = canvas.winfo_screenheight() // 2 - win_height // 2
        canvas.geometry('{}x{}+{}+{}'.format(self.width, self.height, self.x, self.y))
        canvas.deiconify()

    def createcanvas(self):
        self.cs = Canvas(width=canvas.winfo_screenwidth(), height=canvas.winfo_screenheight() , bg="#fff")
        self.cs.pack()

        # PIL create an empty image and draw object to draw on
        # memory only, not visible
        self.image1 = Image.new("RGB", (canvas.winfo_screenwidth(), canvas.winfo_screenheight()), "#fff")

    def menu_Figures(self):
        self.menubar.add_cascade(label="Circle", command=self.figureCircle)
        self.menubar.add_cascade(label="rectangle", command=self.figureRectangle)
        self.menubar.add_cascade(label="Line", command=self.figureLine)
        self.menubar.add_cascade(label="Polygon", command=lambda: self.cs.create_polygon([150,75,225,0,300,75,225,150], fill="#eeeeff"))
        self.menubar.add_cascade(label="Arc", command=self.figureArc)
        
    def menu_Lateral(self):
        self.paint_tools = Frame(self.master, width=150, height=self.master.winfo_screenheight(), relief=RIDGE,borderwidth=2)
        self.paint_tools.place(x=0,y=0)

        self.pen_logo = ImageTk.PhotoImage(Image.open('pen.png'))
        self.p = Label(self.paint_tools, text="pen",borderwidth=0,font=('verdana',10,'bold'))
        self.p.place(x=5,y=11)
        self.pen_button = Button(self.paint_tools,padx=6,image=self.pen_logo,borderwidth=2,command=self.use_pen)
        self.pen_button.place(x=90,y=10)

        self.brush_logo = ImageTk.PhotoImage(Image.open('brush.png'))
        self.b = Label(self.paint_tools,borderwidth=0,text='brush',font=('verdana',10,'bold'))
        self.b.place(x=5,y=40)
        self.brush_button = Button(self.paint_tools,image = self.brush_logo,borderwidth=2,command=self.use_brush) 
        self.brush_button.place(x=90,y=40)

        self.color_logo = ImageTk.PhotoImage(Image.open('color.png'))
        self.cl = Label(self.paint_tools, text='color',font=('verdana',10,'bold'))
        self.cl.place(x=5,y=70)
        self.color_button = Button(self.paint_tools,image = self.color_logo,borderwidth=2,command=self.choose_color)
        self.color_button.place(x=90,y=70)

        self.eraser_logo = ImageTk.PhotoImage(Image.open('eraser.png'))
        self.e = Label(self.paint_tools, text='eraser',font=('verdana',10,'bold'))
        self.e.place(x=5,y=100)
        self.eraser_button = Button(self.paint_tools,image = self.eraser_logo,borderwidth=2,command=self.use_eraser)
        self.eraser_button.place(x=90,y=100)

        self.pen_size = Label(self.paint_tools,text="Pen Size",font=('verdana',10,'bold'))
        self.pen_size.place(x=20,y=250)
        self.choose_size_button = Scale(self.paint_tools, from_=1, to=10, orient=VERTICAL)
        self.choose_size_button.place(x=38,y=150)
        
        self.setup()

    def figureCircle(self):
        self.optionsDraw()

        self.tipos_figuras = [self.cs.create_oval, self.cs.create_oval]
        self.dibujo = None

    def figureRectangle(self):
        self.optionsDraw()

        self.tipos_figuras = [self.cs.create_rectangle, self.cs.create_rectangle]
        self.dibujo = None

    def figureLine(self):
        self.optionsDraw()

        self.tipos_figuras = [self.cs.create_line, self.cs.create_line]
        self.dibujo = None

    def figurePolygon(self):
        self.optionsDraw()

        self.tipos_figuras = [self.cs.create_polygon, self.cs.create_polygon]
        self.dibujo = None

    def figureArc(self):
        self.optionsDraw()

        self.tipos_figuras = [self.cs.create_arc, self.cs.create_arc]
        self.dibujo = None

    def optionsDraw(self):
        self.cs.bind('<ButtonPress-1>', self.start_drawing)
        self.cs.bind('<B1-Motion>', self.draw)
        self.cs.bind('<Double-1>', self.clear)
        self.cs.bind('<ButtonPress-3>', self.move)

    def start_drawing(self, evento):
        self.figura = self.tipos_figuras[0]
        self.tipos_figuras = self.tipos_figuras[1:] + self.tipos_figuras[:1]
        self.inicio = evento
        self.dibujo = None

    def draw(self, evento):
        cs = evento.widget
        if self.dibujo:
            self.cs.delete(self.dibujo)
        id_figura = self.figura(self.inicio.x, self.inicio.y, evento.x, evento.y, fill="#7CFC00")
        self.dibujo = id_figura

        draw = ImageDraw.Draw(self.image1) #Draw on image1

        draw.ellipse([self.inicio.x, self.inicio.y, evento.x, evento.y],fill="#eeeeff")
        draw.polygon([150,75,225,0,300,75,225,150],fill="#eeeeff",outline = "blue")

    def clear(self, evento):
        evento.widget.delete('all')

    def move(self, evento):
        if self.dibujo:
            self.cs = evento.widget
            diferencia_x = evento.x - self.inicio.x
            diferencia_y = evento.y - self.inicio.y

            self.cs.move(self.dibujo, diferencia_x, diferencia_y)

            self.inicio = evento


    def options(self):
        self.menubar = Menu(canvas)
        filemenu = Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="New", command=None)
        filemenu.add_command(label="Open", command=None)
        filemenu.add_command(label="Save", command=self.save)
        filemenu.add_command(label="Save as...", command=self.save)
        filemenu.add_command(label="Close", command=None)

        filemenu.add_separator()

        filemenu.add_command(label="Exit", command=canvas.quit)
        self.menubar.add_cascade(label="File", menu=filemenu)
        editmenu = Menu(self.menubar, tearoff=0)

        editmenu.add_command(label="Cut", command=None)
        editmenu.add_command(label="Copy", command=None)
        editmenu.add_command(label="Paste", command=None)
        editmenu.add_command(label="Delete", command=None)
        editmenu.add_command(label="Select All", command=None)
        self.menubar.add_cascade(label="Edit", menu=editmenu)

        helpmenu = Menu(self.menubar, tearoff=0)
        helpmenu.add_command(label="About...", command=None)
        helpmenu.add_command(label="Theme", command=self.theme)
        self.menubar.add_cascade(label="Help", menu=helpmenu)

        canvas.config(menu=self.menubar)

    def save(self):
        # Tkinter canvas object can only be saved as a postscipt file
        # which is actually a postscript printer language text file
        self.cs.postscript(file="my_drawing.ps", colormode='color')
        # PIL image can be saved as .png .jpg .gif or .bmp file
        filename = "my_canvas.jpg"
        self.image1.save(filename)
        #os.startfile(filename)

        imagen = pyautogui.screenshot(region=(self.x, self.y, self.width, self.height))
        imagen.save('captura.png')
        imagen.show()

    def theme(self):
        filewin = Toplevel(canvas)
        Button(filewin, text="Dark", width=30, command=lambda: self.cs.configure(bg="#000")).pack()
        Button(filewin, text="Lihg", width=30, command=lambda: self.cs.configure(bg="#fff")).pack()
        
    '''
    Este nuevo codigo
    '''
    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = self.choose_size_button.get()
        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.active_button = self.pen_button
        self.cs.bind('<B1-Motion>', self.paint)
        self.cs.bind('<ButtonRelease-1>', self.reset)

    def use_pen(self):
        self.activate_button(self.pen_button)

    def use_brush(self):
        self.activate_button(self.brush_button)

    def choose_color(self):
        self.eraser_on = False
        self.color = askcolor(color=self.color)[1]

    def use_eraser(self):
        self.activate_button(self.eraser_button, eraser_mode=True)

    def activate_button(self, some_button, eraser_mode=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode

    def paint(self, event):
        self.line_width = self.choose_size_button.get()
        paint_color = 'white' if self.eraser_on else self.color
        if self.old_x and self.old_y:
            self.cs.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=paint_color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x, self.old_y = None, None

canvas = tk.Tk()
myapp = App(canvas)
myapp.mainloop()