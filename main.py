from tkinter import *
import tkinter.filedialog as fd
from ElectricityCluster import *
from Electricity import *
from VectorField import *


class PaintApp:
    Cluster = ElectricityCluster()
    VecFil = VectorField()
    drawing_tool = "inside"
    left_button = "up"
    x_position, y_position = None, None

    x1_line_pt, y1_line_pt, x2_line_pt, y2_line_pt = None, None, None, None

    @staticmethod
    def quit_app():
        root.quit()

    def __init__(self, Root):
        self.drawing_area = Canvas(Root, width=500, height=500, bg="white")
        self.drawing_area.pack()

        self.drawing_area.bind("<Motion>", self.motion)
        self.drawing_area.bind("<ButtonPress-1>", self.left_button_down)
        self.drawing_area.bind("<ButtonRelease-1>", self.left_button_up)

        the_menu = Menu(Root)
        file_menu = Menu(the_menu, tearoff=0)
        tool_menu = Menu(the_menu, tearoff=0)
        elect_menu = Menu(the_menu, tearoff=0)
        coil_menu = Menu(the_menu, tearoff=0)
        elect_menu.add_command(label="Inside", command=self.set_inside_drawing_tool)
        elect_menu.add_command(label="Outside", command=self.set_outside_drawing_tool)
        tool_menu.add_command(label="Remove", command=self.remove_drawing_tool)
        tool_menu.add_command(label="Move", command=self.move_drawing_tool)
        file_menu.add_command(label="Save", command=self.save)
        file_menu.add_command(label="load", command=self.load)
        file_menu.add_command(label="Quit", command=self.quit_app)
        coil_menu.add_command(label="Inside", command=self.set_inside_coil)
        coil_menu.add_command(label="OutSide", command=self.set_outside_coil)
        the_menu.add_cascade(label="Options", menu=file_menu)
        the_menu.add_cascade(label="Tools", menu=tool_menu)
        the_menu.add_cascade(label="Electricity", menu=elect_menu)
        the_menu.add_cascade(label="Coil", menu=coil_menu)
        Root.config(menu=the_menu)

    def save(self):
        save_file = fd.asksaveasfile(title="Сохранить файл",
                                     defaultextension=".txt",
                                     filetypes=(("Текстовый файл", "*.txt"),))
        if not save_file:
            return
        save_file.write(self.Cluster.get_JSON())
        save_file.close()

    def load(self):
        load_file = fd.askopenfilename(title="Выбрать файл",
                                       defaultextension=".txt",
                                       filetypes=(("Текстовый файл", "*.txt"),))
        with open(load_file) as file:
            load_collection = json.loads(file.read())
        for elem in load_collection:
            elect = Electricity(x=int(elem[0]), y=int(elem[1]), clockwise=int(elem[2]), is_elec=int(elem[3]))
            self.Cluster.add_electricity(elect)
            self.build_Vector_field()

    def set_inside_drawing_tool(self):
        self.drawing_tool = "inside_elec"

    def set_outside_drawing_tool(self):
        self.drawing_tool = "outside-elec"

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
        self.x1_line_pt = event.x
        self.y1_line_pt = event.y

    def left_button_up(self, event=None):
        self.left_button = "up"
        self.x_position = None
        self.y_position = None

        self.x2_line_pt = event.x
        self.y2_line_pt = event.y

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
        self.x_position = event.x
        self.y_position = event.y

    def inside_elec_draw(self):
        if None not in (self.x1_line_pt, self.x2_line_pt, self.y1_line_pt, self.y2_line_pt):
            diameter = 15
            center_x = min(self.x1_line_pt, self.x2_line_pt) + diameter
            center_y = min(self.y1_line_pt, self.y2_line_pt) + diameter
            new_elect = Electricity(x=center_x, y=center_y, clockwise=1, is_elec=1)
            self.Cluster.add_electricity(new_elect)
            self.build_Vector_field()

    def inside_coil_draw(self):
        if None not in (self.x1_line_pt, self.x2_line_pt, self.y1_line_pt, self.y2_line_pt):
            diameter = 15
            center_x = min(self.x1_line_pt, self.x2_line_pt) + diameter
            center_y = min(self.y1_line_pt, self.y2_line_pt) + diameter
            new_elect = Electricity(x=center_x, y=center_y, clockwise=1, is_elec=0)
            self.Cluster.add_electricity(new_elect)
            self.build_Vector_field()

    def outside_coil_draw(self):
        if None not in (self.x1_line_pt, self.x2_line_pt, self.y1_line_pt, self.y2_line_pt):
            diameter = 15
            center_x = min(self.x1_line_pt, self.x2_line_pt) + diameter
            center_y = min(self.y1_line_pt, self.y2_line_pt) + diameter
            new_elect = Electricity(x=center_x, y=center_y, clockwise=0, is_elec=0)
            self.Cluster.add_electricity(new_elect)
            self.build_Vector_field()

    def outside_elec_draw(self):
        if None not in (self.x1_line_pt, self.x2_line_pt, self.y1_line_pt, self.y2_line_pt):
            diameter = 15
            center_x = min(self.x1_line_pt, self.x2_line_pt) + diameter
            center_y = min(self.y1_line_pt, self.y2_line_pt) + diameter
            new_elect = Electricity(x=center_x, y=center_y, clockwise=0, is_elec=1)
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

        for vector in self.VecFil.get_VectorField():
            x = vector.get_X()
            y = vector.get_Y()
            length = 0
            angle = 0
            len2 = 0
            flag = 1
            for elect in self.Cluster.get_cluster():
                temp_len = elect.get_vector_length(vector_x=x, vector_y=y)

                temp_angle = elect.get_vector_angle(vector_x=x, vector_y=y)

                if flag == 1:
                    length = temp_len
                    angle = temp_angle
                    len2 = length
                    flag = 0
                else:
                    num = math.pi - angle + temp_angle
                    cos = math.cos(num)
                    sin = math.sin(num)
                    len2 = temp_len * temp_len + length * length - 2 * temp_len * length * cos
                    len2 = math.sqrt(len2)
                    angle = math.asin(sin * temp_len / len2) + temp_angle


            vector.set_length(len2)
            vector.set_angle(angle)
            vector.draw(self.drawing_area)


root = Tk()
paint_app = PaintApp(root)
root.mainloop()
