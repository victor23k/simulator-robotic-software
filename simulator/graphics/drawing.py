import tkinter as tk
import tkinter.ttk as ttk
from PIL import ImageTk, Image
import robot_components.robots as rbts
import subprocess
import os


class Drawing:

    def __init__(self):
        """
        Constructor for the drawing
        """
        self.canvas = None
        self.robot = None
        self.images = {}
        self.canvas_images = {}
        self.scale = 0.2
        self.hud_w = 0
        self.hud_h = 0
        self.component = 0
        self.components = []
        self.dx = 0
        self.dy = 0
        self.robots = []
        self.initialize_robots()
        self.wires = []
        self.buttons = []
        self.button = 0

    def set_canvas(self, canvas: tk.Canvas):
        """
        Sets the canvas in which the drawing is going to be done
        Arguments:
            canvas: the canvas
        """
        self.canvas = canvas

    def initialize_robots(self):
        robot1 = rbts.Challenge1Robot(self)
        self.robots.append(robot1)
        robot2 = rbts.Challenge2Robot(self)
        self.robots.append(robot2)
        robot3 = rbts.Challenge3Robot(self)
        self.robots.append(robot3)

    def set_robot(self, robot):
        self.robot = robot

    def empty_drawing(self):
        """
        Deletes all elements from the drawing
        """
        self.canvas.delete('all')
        self.canvas_images = {}

    def delete_zoomables(self):
        """
        Deletes all the elements that have to be zoomed
        """
        self.canvas.delete('actuator', 'button_left', 'button_right', 'block', 'arduinoBoard')
        self.canvas.delete('robot', 'circuit', 'obstacle', 'wire',
                           'light_1', 'light_2', 'light_3', 'light_4')
        self.canvas.delete('prueba')
        for component in self.components:
            self.canvas.delete(component["group"])
        for button in self.buttons:
            self.canvas.delete(button["group"])

    def draw_image(self, element, group):
        """
        Draws an image
        Arguments:
            element: a dict whose content is the x and y
            coordinates and the image (as Image instance)
            group: the tag where the image is going to
            be added to
        """
        image = self.__open_image(element["image"], group)
        return self.__add_to_canvas(element["x"], element["y"], image, group)

    def redraw_image(self, element, group):
        """
        Redraws an already existing image
        Arguments:
            element: a dict whose content is the x and y
            coordinates and the image (as Image instance)
            group: the tag where the image is going to
            be added to
        """
        self.canvas.delete(group)
        del self.canvas_images[group]
        image = self.__open_image(element["image"], group)
        self.__add_to_canvas(element["x"], element["y"], image, group)

    def move_image(self, group, x, y):
        """
        Moves a image (or group of) of the drawing
        Arguments:
            group: the tag of the image(s)
            x: the x differential
            y: the y differential
        """
        current_x = self.canvas_images[group]["x"]
        current_y = self.canvas_images[group]["y"]
        scale_x = int(x * self.scale)
        scale_y = int(y * self.scale)
        dx = scale_x - current_x
        dy = scale_y - current_y
        self.canvas_images[group]["x"] = scale_x
        self.canvas_images[group]["y"] = scale_y
        self.canvas.move(group, dx, dy)

    def rotate_image(self, element, angle, group):
        """
        Rotates a image by an angle
        Arguments:
            element: a dict whose elements are the x and
            y coordinates and the image (as str path)
            angle: the differential of the angle
            group: the group of the image(s)
        """
        self.canvas.delete(group)
        image = self.__open_image(element["image"], group)
        rotated_img = self.images[element["image"]
        ] = image.rotate(angle, expand=True)
        self.__add_to_canvas(element["x"], element["y"], rotated_img, group)

    def draw_rectangle(self, form: dict):
        """
        Draws a rectangle given some measurements
        Arguments:
            form: a dictionary whose elements are the x and
            y coordinates, the width and height of the
            rectangle and the color and group (tag of tkinter)
        """
        x = int(form["x"] * self.scale)
        y = int(form["y"] * self.scale) + self.hud_h
        width = int(form["width"] * self.scale)
        height = int(form["height"] * self.scale)
        color = form["color"]
        group = form["group"]
        self.canvas.create_rectangle(
            x, y, x + width, y + height, fill=color, tags=group)

    def draw_wire(self, x1, y1, x2, y2):
        self.wires.append(self.canvas.create_line(x1, y1, x2, y2, tags='wire'))

    def redraw_wire(self, wire):
        #TODO --> Cuando se redimensiona la pantalla se redibuja el cable (se borra bien, hay que volver a dibujarlo)
        print(8)

    def draw_arc(self, form: dict):
        """
        Draws an arc given some measurements
        Arguments:
            form: a dictionary whose elements are the x and y
            coordinates, the width and height of the bounding of
            the arc, the width of the arc, the angle of the arc
            and the group (tag of tkinter)
        """
        x = int(form["x"] * self.scale)
        y = int(form["y"] * self.scale) + self.hud_h
        width = int(form["width"] * self.scale)
        height = int(form["height"] * self.scale)
        track_width = int(form["track_width"] * self.scale)
        starting_angle = form["starting_angle"]
        angle = form["angle"]
        group = form["group"]
        self.canvas.create_arc(x, y, x + width, y + height, width=track_width, style="arc", start=starting_angle,
                               extent=angle, tags=group)

    def zoom_in(self):
        """
        Zooms in the scale and updates the drawing
        """
        if self.scale < 1:
            self.scale += 0.1
        self.scale = round(self.scale, 1)
        self.__update_size()

    def zoom_out(self):
        """
        Zooms out the scale and updates the drawing
        """
        if self.scale > 0.1:
            self.scale -= 0.1
        self.scale = round(self.scale, 1)
        self.__update_size()

    def zoom_percentage(self):
        """
        Returns the zoom percentage
        """
        return self.scale * 100

    def set_size(self, width, height):
        """
        Sets the size limits of the canvas
        Arguments:
            width: the width of the canvas
            height: the height of the canvas
        """
        self.width = width
        self.height = height
        self.__update_size()

    def __update_size(self):
        """
        Updates the size of the canvas according
        with the scale and the size of it
        """
        w = self.width * self.scale
        h = self.height * self.scale
        self.canvas.configure(scrollregion=(0, 0, w, h))

    def __add_to_canvas(self, x, y, image: Image, group):
        """
        Adds a image to the canvas
        Arguments:
            x: the x coordinate of the image
            y: the y coordinate of the image
            image: the image to add (as Image instance)
            group: the group (tag of tkinter)
        """
        width = int(image.width * self.scale)
        height = int(image.height * self.scale)
        res_img = image.resize((width, height), Image.ANTIALIAS)
        scale_x = x * self.scale
        scale_y = y * self.scale + self.hud_h
        self.canvas_images[group] = {
            "x": scale_x,
            "y": scale_y,
            "image": ImageTk.PhotoImage(res_img)
        }
        return self.canvas.create_image(
            scale_x, scale_y, image=self.canvas_images[group]["image"], tags=group)

    def __open_image(self, image_path, group):
        image = None
        if group not in self.images:
            image = self.__get_image(image_path, group)
        elif not self.images[group]["path"] == image_path:
            image = self.__get_image(image_path, group)
        else:
            image = self.images[group]["image"]
        return image

    def __get_image(self, image_path, group):
        image = Image.open(image_path)
        self.images[group] = {
            "image": image,
            "path": image_path
        }
        return image

    def draw_component(self, element, x, y):
        x_total = (x + self.dx) / self.scale
        y_total = (y + self.dy) / self.scale
        image = element.draw_self(x_total, y_total, self.component)
        self.draw_image(image, image["group"])
        self.components.append(image)
        self.component += 1
        self.draw_buttons(element, x_total, y_total)

    def draw_all_components(self):
        for component in self.components:
            self.draw_image(component, component["group"])


    def probe(self, option_gamification, user_code, robot_code, user_robot, robot):
        self.probe_window = tk.Toplevel()
        self.probe_window.geometry("800x450")
        self.probe_window.title("Resultado desafío " + str(option_gamification))
        self.probe_window.configure(background="#006468")

        #TODO --> Cambiar comprobaciones de código y robot
        """La comprobación del código podría ser que estén definidos los objetos en pines correctos
            (no necesariamente los mismos que el código de ejemplo), tengan las variables definidas
            correctamente aunque no exactamente con los mismos valores y el código esté igual sin espacios
            
            ¿El robot podría comprobar si los pins de cada elemento están unidos a lo que tienen que estar?
        """
        if not user_code.replace(" ", "").replace("\n", "").replace("\t", "") == \
               robot_code.replace(" ", "").replace("\n", "").replace("\t", ""):
            sol_code = tk.Label(self.probe_window, text="El código no es correcto",
                                font=("Arial", 15), background="#006468")
        else:
            sol_code = tk.Label(self.probe_window, text="Código OK", font=("Arial", 15), background="#006468")
        if not self.probe_robot(user_robot, robot):
            sol_robot = tk.Label(self.probe_window, text="El robot no es correcto",
                                 font=("Arial", 15), background="#006468")
        else:
            sol_robot = tk.Label(self.probe_window, text="Robot OK", font=("Arial", 15), background="#006468")

        sol_code.pack(padx=10, pady=20)
        sol_robot.pack(padx=10, pady=10)

    def show_tutorial(self, option_gamification):
        path = self.get_robot_challenge(option_gamification).get_tutorial()
        subprocess.Popen([os.path.abspath(path)], shell=True)

    def show_help(self, option_gamification):
        self.help_window = tk.Toplevel()
        self.help_window.geometry("600x620")
        self.help_window.title("Ayuda desafío " + str(option_gamification))
        self.help_window.configure(background="#006468")
        ayuda = tk.Label(self.help_window, text=self.get_robot_challenge(option_gamification).get_help(),
                         font=("Arial", 15), background="#006468")
        ayuda.pack(padx=10, pady=20)

    def get_robot_challenge(self, option_gamification):
        if option_gamification == 0:
            return self.robots[0]
        if option_gamification == 1:
            return self.robots[1]
        if option_gamification == 2:
            return self.robots[2]

    def probe_robot(self, user_robot, robot):
        if not len(user_robot.robot_elements) == len(robot.robot_elements):
            return False
        for i in range(len(robot.robot_elements)):
            if not isinstance(robot.robot_elements[i], type(user_robot.robot_elements[i])):
                return False
        return True

    def find_component(self, x, y):
        #TODO --> Esto no va a ser necesario cuando se consiga poner los botones en el canvas en los componentes
        x_total = x / self.scale
        y_total = y / self.scale
        distance_total = 1000
        component_selected = None
        for component in self.components:
            distance = ((x_total - component['x'])**2 + (y_total - component['y'])**2)**0.005
            if round(distance, 4) < 1.053 and round(distance, 4) < round(distance_total, 4):
                component_selected = component
                distance_total = distance
        distance = ((x_total - self.robot.board['x'])**2 + (y_total - self.robot.board['y'])**2)**0.005
        if round(distance, 4) < 1.057 and round(distance, 4) < round(distance_total, 4):
            component_selected = self.robot.board
        print(distance_total)
        return component_selected

    def attach(self, component1, component2, pin_component1, pin_component2):
        #TODO --> Cambiar esto cuando se consiga poner los botones en el canvas en los componentes
        #TODO --> si uno de los dos componentes es una placa arduino (no contemplado ahora mismo)
        component1.attach_element(pin_component1+1, component2, pin_component2+1)
        component2.attach_element(pin_component2+1, component1, pin_component1+1)
        self.attach_window.destroy()

    def attach_component(self, x, y):
        if self.hud.component_to_attach is None:
            """Si todavía no se ha seleccionado el primer componente, se selecciona"""
            self.hud.component_to_attach = self.drawing.find_component(x, y)
            self.prev_x = x
            self.prev_y = y
        else:
            """Si ya se ha seleccionado anteriormente un componente, se unen ambos"""
            component_to_attach2 = self.drawing.find_component(x, y)
            self.drawing.draw_wire(x, y, self.prev_x, self.prev_y)
            self.prev_x = x
            self.prev_y = y
            if component_to_attach2 is not None and component_to_attach2 is not self.hud.component_to_attach:
                self.drawing.attach_components(self.hud.component_to_attach, component_to_attach2, self.robot)
                self.hud.component_to_attach = None
                self.hud.draw_wire = False

    def draw_buttons(self, element, x, y):
        buttons = element.draw_buttons(x, y)
        for button in buttons:
            x_total = button['x']
            y_total = button['y']
            button1 = {
                "x": x_total,
                "y": y_total,
                "image": "assets/point.png",
                "group": "button" + str(self.button),
                "element": self,
                "n_pin": button['n_pin']
            }
            img = self.draw_image(button1, button1["group"])
            self.buttons.append(button1)
            self.button += 1
            if button['n_pin'] == 1:
                self.canvas.tag_bind(img, "<Button-1>", lambda event: self.select_pin1())
            elif button['n_pin'] == 2:
                self.canvas.tag_bind(img, "<Button-1>", lambda event: self.select_pin2())
            elif button['n_pin'] == 3:
                self.canvas.tag_bind(img, "<Button-1>", lambda event: self.select_pin3())
            elif button['n_pin'] == 4:
                self.canvas.tag_bind(img, "<Button-1>", lambda event: self.select_pin4())
            elif button['n_pin'] == 5:
                self.canvas.tag_bind(img, "<Button-1>", lambda event: self.select_pin5())
            elif button['n_pin'] == 6:
                self.canvas.tag_bind(img, "<Button-1>", lambda event: self.select_pin6())
            elif button['n_pin'] == 7:
                self.canvas.tag_bind(img, "<Button-1>", lambda event: self.select_pin7())
            elif button['n_pin'] == 8:
                self.canvas.tag_bind(img, "<Button-1>", lambda event: self.select_pin8())

    def draw_all_buttons(self):
        for button in self.buttons:
            self.draw_image(button, button["group"])

    def select_pin1(self):
        print(1)

    def select_pin2(self):
        print(2)

    def select_pin3(self):
        print(3)

    def select_pin4(self):
        print(4)

    def select_pin5(self):
        print(5)

    def select_pin6(self):
        print(6)

    def select_pin7(self):
        print(7)

    def select_pin8(self):
        print(8)
