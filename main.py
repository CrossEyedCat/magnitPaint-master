from tkinter import *
import tkinter.filedialog as fd
from tkinter import simpledialog
from ElectricityCluster import *
from Electricity import *
from VectorField import *
from tkinter.messagebox import showerror
import tkinter.messagebox as mb
SCALE = 1

def from_rgb(rgb):
    # translates an rgb tuple of int to a tkinter friendly color code
    return "#%02x%02x%02x" % rgb

class ResizingCanvas(Canvas):
    def __init__(self, parent, **kwargs):
        Canvas.__init__(self, parent, **kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self, event):
        self.width = event.width
        self.height = event.height
        # resize the canvas 
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        #self.scale("all",0,0,wscale,hscale)

    def scale_plus(self):
        global SCALE
        SCALE *= 1.1
        print(SCALE)
        self.scale("all", 0, 0, 1.1, 1.1)

    def scale_minus(self):
        global SCALE
        SCALE /= 1.1
        print(SCALE)
        self.scale("all", 0, 0, 1/1.1, 1/1.1)

    def scale_normal(self):
        self.scale("all", 0, 0, SCALE, SCALE)


class PaintApp:
    Cluster = ElectricityCluster()
    drawing_tool = "inside"
    left_button = "up"
    x_position, y_position = None, None
    current_strength = 1
    x1_line_pt, y1_line_pt, x2_line_pt, y2_line_pt = None, None, None, None

    @staticmethod
    def quit_app():
        root.quit()

    def __init__(self, Root):
        self.VecFil = VectorField()
        self.VecFil.set_window_size(root.winfo_screenwidth(), root.winfo_screenheight())
        self.drawing_area = ResizingCanvas(Root, width=500, height=500, bg="white",
            scrollregion=(0, 0, root.winfo_screenwidth(), root.winfo_screenheight()))

        self.hbar = Scrollbar(Root, orient=HORIZONTAL)
        self.hbar.pack(side=BOTTOM, fill=X)
        self.hbar.config(command=self.drawing_area.xview)
        self.vbar = Scrollbar(Root, orient=VERTICAL)
        self.vbar.pack(side=RIGHT, fill=Y)
        self.vbar.config(command=self.drawing_area.yview)
        self.drawing_area.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
        self.drawing_area.pack(side=LEFT, expand=True, fill=BOTH)

        self.drawing_area.bind("<Motion>", self.motion)
        self.drawing_area.bind("<ButtonPress-1>", self.left_button_down)
        self.drawing_area.bind("<ButtonRelease-1>", self.left_button_up)
        self.drawing_area.bind("<ButtonPress-3>", self.right_button_vector_info)
        def keys(event):
            if event.keycode == 402653245 and event.state == 4:
                self.drawing_area.scale_plus()
            if event.keycode == 452984863 and event.state == 4:
                self.drawing_area.scale_minus()
        root.bind("<Control-KeyPress>", keys)

        the_menu = Menu(Root)
        Root.config(menu=the_menu)

        file_menu = Menu(the_menu, tearoff=0)
        file_menu.add_command(label="Save", command=self.save)
        file_menu.add_command(label="load", command=self.load)
        file_menu.add_command(label="Quit", command=self.quit_app)
        the_menu.add_cascade(label="Options", menu=file_menu)

        tool_menu = Menu(the_menu, tearoff=0)
        tool_menu.add_command(label="Remove", command=self.remove_drawing_tool)
        tool_menu.add_command(label="Move", command=self.move_drawing_tool)
        the_menu.add_cascade(label="Tools", menu=tool_menu)

        elect_menu = Menu(the_menu, tearoff=0)
        elect_menu.add_command(label="Inside", command=self.set_inside_drawing_tool)
        elect_menu.add_command(label="Outside", command=self.set_outside_drawing_tool)
        the_menu.add_cascade(label="Electricity", menu=elect_menu)

        coil_menu = Menu(the_menu, tearoff=0)
        coil_menu.add_command(label="Inside", command=self.set_inside_coil)
        coil_menu.add_command(label="OutSide", command=self.set_outside_coil)
        the_menu.add_cascade(label="Coil", menu=coil_menu)

        scale_menu = Menu(the_menu, tearoff=0)
        scale_menu.add_command(label="+", command=self.drawing_area.scale_plus)
        scale_menu.add_command(label="-", command=self.drawing_area.scale_minus)
        the_menu.add_cascade(label="Scale", menu=scale_menu)

        def strength_input():
            user_input = simpledialog.askstring("Введите силу тока", "Значение - дробное число")
            if user_input != "":
                try:
                    self.current_strength = float(user_input)
                except:
                    showerror("Ошибка ввода", "Сила тока должна быть числом")
        strength_menu = Menu(the_menu, tearoff=0)
        strength_menu.add_command(label = "Сила Тока", command=strength_input)
        the_menu.add_cascade(label="Параметры", menu=strength_menu)


    def save(self):
        save_file = fd.asksaveasfile(title="Сохранить файл",
                                     defaultextension=".txt",
                                     filetypes=(("Текстовый файл", "*.txt"),))
        if not save_file:
            return
        save_file.write(self.Cluster.get_JSON())
        save_file.close()

    def right_button_vector_info(self, event=None):
        for v in self.VecFil.get_VectorField():
            x1= event.x-event.x%10
            y1= event.y-event.y%10
            if x1==v.get_X() and y1==v.get_Y():
                num =v.get_length()
                if num==1: num =0
                msg= str(num) + "*μ0*10^-5 Тс"
                mb.showinfo("Информация", msg)
    def load(self):
        load_file = fd.askopenfilename(title="Выбрать файл",
                                       defaultextension=".txt",
                                       filetypes=(("Текстовый файл", "*.txt"),))
        with open(load_file) as file:
            load_collection = json.loads(file.read())
        self.Cluster.clear()
        for elem in load_collection:
            elect = Electricity(x=int(elem[0]), y=int(elem[1]), clockwise=int(elem[2]), is_elec=int(elem[3]), current_strength=int(elem[4]))
            self.Cluster.add_electricity(elect)
            self.build_Vector_field()

    def set_inside_drawing_tool(self):
        self.drawing_tool = "inside_elec"

    def set_outside_drawing_tool(self):
        self.drawing_tool = "outside_elec"

    def remove_drawing_tool(self):
        self.drawing_tool = "remove"

    def move_drawing_tool(self):
        self.drawing_tool = "move"

    def set_inside_coil(self):
        self.drawing_tool = "inside_coil"

    def set_outside_coil(self):
        self.drawing_tool = "outside_coil"

    def left_button_down(self, event=None):
        self.left_button = "down"
        self.x1_line_pt = (event.x + self.hbar.get()[0]*root.winfo_screenwidth()) // SCALE
        self.y1_line_pt = (event.y + self.vbar.get()[0]*root.winfo_screenheight()) // SCALE

    def left_button_up(self, event=None):
        self.left_button = "up"
        self.x_position = None
        self.y_position = None

        self.x2_line_pt = (event.x + self.hbar.get()[0]*root.winfo_screenwidth()) // SCALE
        self.y2_line_pt = (event.y + self.vbar.get()[0]*root.winfo_screenheight()) // SCALE

        if self.drawing_tool == "inside_elec":
            self.inside_elec_draw()
        if self.drawing_tool == "inside_coil":
            self.inside_coil_draw()
        if self.drawing_tool == "outside_elec":
            self.outside_elec_draw()
        if self.drawing_tool == "outside_coil":
            self.outside_coil_draw()
        if self.drawing_tool == "remove":
            self.remove_draw()
        if self.drawing_tool == "move":
            self.move_draw()

    def motion(self, event=None):
        self.x_position = (event.x + self.hbar.get()[0]*root.winfo_screenwidth()) // SCALE
        self.y_position = (event.y + self.vbar.get()[0]*root.winfo_screenheight()) // SCALE

    def inside_elec_draw(self):
        if None not in (self.x1_line_pt, self.x2_line_pt, self.y1_line_pt, self.y2_line_pt):
            diameter = 15
            center_x = min(self.x1_line_pt, self.x2_line_pt) + diameter
            center_y = min(self.y1_line_pt, self.y2_line_pt) + diameter
            new_elect = Electricity(x=center_x, y=center_y, clockwise=1, is_elec=1, current_strength=self.current_strength)
            self.Cluster.add_electricity(new_elect)
            self.build_Vector_field()

    def inside_coil_draw(self):
        if None not in (self.x1_line_pt, self.x2_line_pt, self.y1_line_pt, self.y2_line_pt):
            diameter = 15
            center_x = min(self.x1_line_pt, self.x2_line_pt) + diameter
            center_y = min(self.y1_line_pt, self.y2_line_pt) + diameter
            new_elect = Electricity(x=center_x, y=center_y, clockwise=1, is_elec=0, current_strength=self.current_strength)
            self.Cluster.add_electricity(new_elect)
            self.build_Vector_field()

    def outside_coil_draw(self):
        if None not in (self.x1_line_pt, self.x2_line_pt, self.y1_line_pt, self.y2_line_pt):
            diameter = 15
            center_x = min(self.x1_line_pt, self.x2_line_pt) + diameter
            center_y = min(self.y1_line_pt, self.y2_line_pt) + diameter
            new_elect = Electricity(x=center_x, y=center_y, clockwise=0, is_elec=0, current_strength=self.current_strength)
            self.Cluster.add_electricity(new_elect)
            self.build_Vector_field()

    def outside_elec_draw(self):
        if None not in (self.x1_line_pt, self.x2_line_pt, self.y1_line_pt, self.y2_line_pt):
            diameter = 15
            center_x = min(self.x1_line_pt, self.x2_line_pt) + diameter
            center_y = min(self.y1_line_pt, self.y2_line_pt) + diameter
            new_elect = Electricity(x=center_x, y=center_y, clockwise=0, is_elec=1, current_strength=self.current_strength)
            self.Cluster.add_electricity(new_elect)
            self.build_Vector_field()

    def remove_draw(self):
        for elect in self.Cluster.get_cluster():
            if (elect.get_x() - self.x2_line_pt) ** 2 + (elect.get_y() - self.y2_line_pt) ** 2 <= 900:
                self.Cluster.get_cluster().remove(elect)
                self.build_Vector_field()

    def move_draw(self):
        for elect in self.Cluster.get_cluster():
            if (elect.get_x() - self.x1_line_pt) ** 2 + (elect.get_y() - self.y1_line_pt) ** 2 <= 900:
                elect.set_x(self.x2_line_pt)
                elect.set_y(self.y2_line_pt)
                self.build_Vector_field()

    def build_Vector_field(self):
        self.drawing_area.delete("all")
        for elect in self.Cluster.get_cluster():
            x = elect.get_x()
            y = elect.get_y()
            if elect.get_clockwise() == 0 and elect.iselec() == 1:
                self.drawing_area.create_oval(x - 15, y - 15, x + 15,
                                              y + 15, fill="blue", outline="black", width=1)
                self.drawing_area.create_oval(x - 7.5, y - 7.5,
                                              x + 7.5, y + 7.5,
                                              fill="black", width=1)
            elif elect.get_clockwise() == 1 and elect.iselec() == 1:
                self.drawing_area.create_oval(x - 15, y - 15, x + 15,
                                              y + 15, fill="red", outline="black", width=1)
                self.drawing_area.create_line(x, y - 7.5,
                                              x, y + 7.5,
                                              fill="black",
                                              width=4)
                self.drawing_area.create_line(x - 7.5, y,
                                              x + 7.5, y,
                                              fill="black",
                                              width=4)
            elif elect.get_clockwise() == 0 and elect.iselec() == 0:
                self.drawing_area.create_oval(x - 15, y - 15, x + 15,
                                              y + 15, fill="purple", outline="black", width=1)
                self.drawing_area.create_oval(x - 7.5, y - 7.5,
                                              x + 7.5, y + 7.5,
                                              fill="black", width=1)
            elif elect.get_clockwise() == 1 and elect.iselec() == 0:
                self.drawing_area.create_oval(x - 15, y - 15, x + 15,
                                              y + 15, fill="yellow", outline="black", width=1)
                self.drawing_area.create_line(x, y - 7.5,
                                              x, y + 7.5,
                                              fill="black",
                                              width=4)
                self.drawing_area.create_line(x - 7.5, y,
                                              x + 7.5, y,
                                              fill="black",
                                              width=4)
        max_len = 0
        min_len = 99999999999999
        for vector in self.VecFil.get_VectorField():
            x = vector.get_X()
            y = vector.get_Y()
            length = 0
            angle = 0
            len2 = 0
            flag = 1
            for elect in self.Cluster.get_cluster():
                temp_len = elect.get_vector_length(x, y)
                temp_angle = elect.get_vector_angle(vector_x=x, vector_y=y)
                if flag == 1:
                    length = temp_len
                    angle = temp_angle
                    len2 = length
                    flag = 0
                else:
                    num = math.pi - angle + temp_angle
                    cos = math.cos(num)
                    sin = math.sin(math.pi-num)
                    len2 = temp_len * temp_len + length * length - 2 * temp_len * length * cos
                    len2 = math.sqrt(len2)
                    angle = math.asin(sin * temp_len / len2) + temp_angle if len2 != 0 else 0.1
                    length = len2
            if max_len < len2:
                max_len = len2
            if min_len > len2:
                min_len = len2
            vector.set_length(len2)
            vector.set_angle(angle)
        part = (max_len - min_len) / 256

        for vector in self.VecFil.get_VectorField():
            if part:
                color = int((vector.length - min_len) / part)+30
                if color < 0: color = 0
                if color > 255: color = 255
                vector.set_color(from_rgb((color, 0, 255 - color)))
            vector.draw(self.drawing_area)
        self.drawing_area.scale_normal()


root = Tk()
root.geometry("1000x700")

paint_app = PaintApp(root)
root.mainloop()
