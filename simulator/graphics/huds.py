import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk


class HUD:

    def __init__(self):
        """
        Constructor for HUD superclass
        """
        self.canvas: tk.Canvas = None
        self.drawing = None

    def set_canvas(self, canvas: tk.Canvas):
        """
        Sets the canvas where the data is going to be drawn at
        Arguments:
            canvas: the canvas
        """
        self.canvas = canvas
        self.canvas.delete('all')
        self.set_text()

    def reboot(self):
        self.canvas.delete('all')
        self.set_text()

    def set_text(self):
        """
        Shows the text of the data that the HUD is going to
        show
        """
        pass


class MobileHUD(HUD):

    def __init__(self):
        """
        Constructor for mobile robot's HUD
        """
        super().__init__()
        self.img_ff = Image.open('assets/full-speed.png')
        self.img_mf = Image.open('assets/mid-speed.png')
        self.img_sf = Image.open('assets/slow-speed.png')

    def set_text(self):
        """
        Sets the corresponding texts for the mobile robot
        """
        self.canvas.create_text(5, 25, text="Rueda izquierda:", font=(
            "Consolas", 13), anchor="w", fill="white")
        self.canvas.create_text(5, 50, text="Rueda derecha:", font=(
            "Consolas", 13), anchor="w", fill="white")
        self.canvas.create_text(5, 75, text="En pista:", font=(
            "Consolas", 13), anchor="w", fill="white")
        self.canvas.create_text(250, 25, text="Detecta obstáculo:", font=(
            "Consolas", 13), anchor="w", fill="white")
        self.canvas.create_text(250, 50, text="└Distancia:", font=(
            "Consolas", 13), anchor="w", fill="white")

    def set_wheel(self, vels):
        """
        Method that gets all the velocitys and calls display_wheels
        for each velocity, so it can represent the wheel's direction
        and velocity
        """
        self.canvas.delete('arr_img')
        i = 0
        self.imgs = []
        for vel in vels:
            self.__display_wheels(i, vel)
            i += 1

    def __display_wheels(self, i, vel):
        """
        Displays arrows in the direction that the wheels are moving
        and with a color that represents their velocity (blue fast,
        yellow medium, red slow).
        Arguments:
            i: the index of the wheel
            vel: the velocity of the wheel
        """
        w = int(self.img_ff.width * 0.5)
        h = int(self.img_ff.height * 0.5)
        self.ff = self.img_ff.resize((w, h), Image.ANTIALIAS)
        self.mf = self.img_mf.resize((w, h), Image.ANTIALIAS)
        self.sf = self.img_sf.resize((w, h), Image.ANTIALIAS)
        if abs(vel) < 100:
            if vel < 0:
                self.sf = self.sf.rotate(180, expand=True)
            self.imgs.append(ImageTk.PhotoImage(self.sf))
        elif abs(vel) > 200:
            if vel < 0:
                self.ff = self.ff.rotate(180, expand=True)
            self.imgs.append(ImageTk.PhotoImage(self.ff))
        else:
            if vel < 0:
                self.mf = self.mf.rotate(180, expand=True)
            self.imgs.append(ImageTk.PhotoImage(self.mf))
        y = 25 + (25 * i)
        self.canvas.create_image(200, y, image=self.imgs[i], tags="arr_img")

    def set_circuit(self, measurements):
        """
        Displays if the robot is on the circuit or outside it
        Arguments:
            measurements: a list with the measurements of the
            light sensors. True if on track, False if else
        """
        self.canvas.delete("cir")
        text = ""
        for i in range(0, len(measurements)):
            if i > 0:
                text += " | "
            if measurements[i]:
                text += "Si"
            else:
                text += "No"
        self.canvas.create_text(100, 75, text=text, font=(
            "Consolas", 13), anchor="w", fill="white", tags="cir")

    def set_detect_obstacle(self, dists):
        """
        Displays if the robot is detecting an obstacle, and the distance
        to it.
        Arguments:
            dists: a list with the distances
        """
        self.canvas.delete("obs")
        text = ""
        for i in range(0, len(dists)):
            dist_text = "-"
            if i > 0:
                text += " | "
            if dists[i] != -1:
                text += "Si"
                dist_text = str(dists[i] - 1)
            else:
                text += "No"
            self.canvas.create_text(360, 50 + (25 * i), text=dist_text, font=("Consolas", 13), anchor="w", tags="obs",
                                    fill="white")
        self.canvas.create_text(425, 25, text=text, font=(
            "Consolas", 13), anchor="w", tags="obs", fill="white")


class ActuatorHUD(HUD):

    def __init__(self):
        """
        Constructor for linear actuator's HUD
        """
        super().__init__()
        self.img_ff = Image.open('assets/full-speed.png')
        self.img_mf = Image.open('assets/mid-speed.png')
        self.img_sf = Image.open('assets/slow-speed.png')

    def set_text(self):
        """
        Sets the corresponding texts for the linear actuator
        """
        self.canvas.create_text(5, 25, text="Dirección de movimiento:", font=(
            "Consolas", 13), anchor="w", fill="white")
        self.canvas.create_text(5, 50, text="Botón izquierdo:", font=(
            "Consolas", 13), anchor="w", fill="white")
        self.canvas.create_text(5, 75, text="Botón derecho:", font=(
            "Consolas", 13), anchor="w", fill="white")

    def set_pressed(self, but_states):
        """
        Parses the button sates to data to show on the HUD
        """
        self.canvas.delete('but_text')
        for i in range(0, len(but_states)):
            text = "No pulsado"
            if but_states[i]:
                text = "Pulsado"
            self.canvas.create_text(150 + 20 * ((i + 1) % 2), 50 + 25 * i, text=text, font=("Consolas", 13), anchor="w",
                                    fill="white", tags="but_text")

    def set_direction(self, vel):
        """
        Draws the direction arrows with the information
        of the velocity
        """
        self.canvas.delete('arr_img')
        w = int(self.img_ff.width * 0.5)
        h = int(self.img_ff.height * 0.5)
        self.ff = self.img_ff.resize((w, h), Image.ANTIALIAS)
        self.mf = self.img_mf.resize((w, h), Image.ANTIALIAS)
        self.sf = self.img_sf.resize((w, h), Image.ANTIALIAS)
        if abs(vel) < 100:
            if vel < 0:
                self.sf = self.sf.rotate(90, expand=True)
            else:
                self.sf = self.sf.rotate(-90, expand=True)
            self.img = ImageTk.PhotoImage(self.sf)
        elif abs(vel) > 200:
            if vel < 0:
                self.ff = self.ff.rotate(90, expand=True)
            else:
                self.ff = self.ff.rotate(-90, expand=True)
            self.img = ImageTk.PhotoImage(self.ff)
        else:
            if vel < 0:
                self.mf = self.mf.rotate(90, expand=True)
            else:
                self.mf = self.mf.rotate(-90, expand=True)
            self.img = ImageTk.PhotoImage(self.mf)
        self.canvas.create_image(250, 25, image=self.img, tags="arr_img")


class ArduinoBoardHUD(HUD):

    def __init__(self):
        """
        Constructor for arduino board's HUD
        """
        super().__init__()
        self.img_resistance = Image.open('assets/resistance.png')
        self.img_button = Image.open('assets/button.png')
        self.img_potentiometer = Image.open('assets/potentiometer.png')
        self.img_led = Image.open('assets/led.png')
        self.img_buzzer = Image.open('assets/buzzer.png')
        self.img_led_rgb = Image.open('assets/ledRGB.png')
        self.img_light_sensor = Image.open('assets/lightSensor.png')
        self.img_pir_sensor = Image.open('assets/PIRSensor.png')
        self.img_vibration_sensor = Image.open('assets/vibrationSensor.png')
        self.img_infrared_sensor = Image.open('assets/infraredSensor.png')
        self.img_ultrasonic_sensor = Image.open('assets/ultrasonicSensor.png')
        self.img_keyboard = Image.open('assets/keyboard.png')
        self.img_screen = Image.open('assets/screen.png')
        self.img_servomotor = Image.open('assets/servomotor180.png')

    def set_canvas(self, canvas: tk.Canvas):
        """
        Sets the canvas where the data is going to be drawn at
        Arguments:
            canvas: the canvas
        """
        self.canvas = canvas
        self.canvas.delete('all')
        self.set_text()
        self.create_photo_resistance()
        self.create_photo_button()
        self.create_photo_potentiometer()
        self.create_photo_led()
        self.create_photo_buzzer()
        self.create_photo_led_rgb()
        self.create_photo_light_sensor()
        self.create_photo_pir_sensor()
        self.create_photo_vibration_sensor()
        self.create_photo_infrared_sensor()
        self.create_photo_ultrasonic_sensor()
        self.create_photo_keyboard()
        self.create_photo_screen()
        self.create_photo_servomotor()

    def put_resistance(self):
        self.drawing = "resistance"

    def put_button(self):
        self.drawing = "button"

    def put_potentiometer(self):
        self.drawing = "potentiometer"

    def put_led(self):
        self.drawing = "led"

    def put_buzzer(self):
        self.drawing = "buzzer"

    def put_led_rgb(self):
        self.drawing = "ledRGB"

    def put_light_sensor(self):
        self.drawing = "lightSensor"

    def put_pir_sensor(self):
        self.drawing = "PIRSensor"

    def put_vibration_sensor(self):
        self.drawing = "vibrationSensor"

    def put_infrared_sensor(self):
        self.drawing = "infraredSensor"

    def put_ultrasonic_sensor(self):
        self.drawing = "ultrasonicSensor"

    def put_keyboard(self):
        self.drawing = "keyboard"

    def put_screen(self):
        self.drawing = "screen"

    def put_servomotor(self):
        self.drawing = "servomotor180"

    def create_photo_resistance(self):
        self.resistance = self.img_resistance.resize((15, 50), Image.ANTIALIAS)
        self.photo_resistance = ImageTk.PhotoImage(self.resistance)
        self.button_resistance = tk.Button(self.canvas, width=20, height=90,
                                           image=self.photo_resistance,
                                           command=self.put_resistance)
        self.button_resistance.config(background='#006468', activebackground='#006468')
        self.canvas.create_window(15, 50, window=self.button_resistance)

    def create_photo_button(self):
        self.button = self.img_button.resize((40, 45), Image.ANTIALIAS)
        self.photo_button = ImageTk.PhotoImage(self.button)
        self.button_button = tk.Button(self.canvas, width=47, height=90,
                                       image=self.photo_button,
                                       command=self.put_button)
        self.button_button.config(background='#006468', activebackground='#006468')
        self.canvas.create_window(55, 50, window=self.button_button)

    def create_photo_potentiometer(self):
        self.potentiometer = self.img_potentiometer.resize((40, 50), Image.ANTIALIAS)
        self.photo_potentiometer = ImageTk.PhotoImage(self.potentiometer)
        self.button_potentiometer = tk.Button(self.canvas, width=45, height=90,
                                              image=self.photo_potentiometer,
                                              command=self.put_potentiometer)
        self.button_potentiometer.config(background='#006468', activebackground='#006468')
        self.canvas.create_window(108, 50, window=self.button_potentiometer)

    def create_photo_led(self):
        self.led = self.img_led.resize((15, 50), Image.ANTIALIAS)
        self.photo_led = ImageTk.PhotoImage(self.led)
        self.button_led = tk.Button(self.canvas, width=22, height=90,
                                    image=self.photo_led,
                                    command=self.put_led)
        self.button_led.config(background='#006468', activebackground='#006468')
        self.canvas.create_window(149, 50, window=self.button_led)

    def create_photo_buzzer(self):
        self.buzzer = self.img_buzzer.resize((40, 40), Image.ANTIALIAS)
        self.photo_buzzer = ImageTk.PhotoImage(self.buzzer)
        self.button_buzzer = tk.Button(self.canvas, width=48, height=90,
                                       image=self.photo_buzzer,
                                       command=self.put_buzzer)
        self.button_buzzer.config(background='#006468', activebackground='#006468')
        self.canvas.create_window(191, 50, window=self.button_buzzer)

    def create_photo_led_rgb(self):
        self.rgb = self.img_led_rgb.resize((25, 50), Image.ANTIALIAS)
        self.photo_rgb = ImageTk.PhotoImage(self.rgb)
        self.button_rgb = tk.Button(self.canvas, width=31, height=90,
                                    image=self.photo_rgb,
                                    command=self.put_led_rgb)
        self.button_rgb.config(background='#006468', activebackground='#006468')
        self.canvas.create_window(237, 50, window=self.button_rgb)

    def create_photo_light_sensor(self):
        self.light_sensor = self.img_light_sensor.resize((30, 50), Image.ANTIALIAS)
        self.photo_light_sensor = ImageTk.PhotoImage(self.light_sensor)
        self.button_light_sensor = tk.Button(self.canvas, width=35, height=90,
                                             image=self.photo_light_sensor,
                                             command=self.put_light_sensor)
        self.button_light_sensor.config(background='#006468', activebackground='#006468')
        self.canvas.create_window(277, 50, window=self.button_light_sensor)

    def create_photo_pir_sensor(self):
        self.pir = self.img_pir_sensor.resize((35, 40), Image.ANTIALIAS)
        self.photo_pir = ImageTk.PhotoImage(self.pir)
        self.button_pir = tk.Button(self.canvas, width=45, height=90,
                                    image=self.photo_pir,
                                    command=self.put_pir_sensor)
        self.button_pir.config(background='#006468', activebackground='#006468')
        self.canvas.create_window(324, 50, window=self.button_pir)

    def create_photo_vibration_sensor(self):
        self.vibration_sensor = self.img_vibration_sensor.resize((30, 50), Image.ANTIALIAS)
        self.photo_vibration_sensor = ImageTk.PhotoImage(self.vibration_sensor)
        self.button_vibration_sensor = tk.Button(self.canvas, width=40, height=90,
                                                 image=self.photo_vibration_sensor,
                                                 command=self.put_vibration_sensor)
        self.button_vibration_sensor.config(background='#006468', activebackground='#006468')
        self.canvas.create_window(374, 50, window=self.button_vibration_sensor)

    def create_photo_infrared_sensor(self):
        self.infrared_sensor = self.img_infrared_sensor.resize((35, 60), Image.ANTIALIAS)
        self.photo_infrared_sensor = ImageTk.PhotoImage(self.infrared_sensor)
        self.button_infrared_sensor = tk.Button(self.canvas, width=45, height=90,
                                                image=self.photo_infrared_sensor,
                                                command=self.put_infrared_sensor)
        self.button_infrared_sensor.config(background='#006468', activebackground='#006468')
        self.canvas.create_window(423, 50, window=self.button_infrared_sensor)

    def create_photo_ultrasonic_sensor(self):
        self.ultrasonic_sensor = self.img_ultrasonic_sensor.resize((55, 40), Image.ANTIALIAS)
        self.photo_ultrasonic_sensor = ImageTk.PhotoImage(self.ultrasonic_sensor)
        self.button_ultrasonic_sensor = tk.Button(self.canvas, width=65, height=90,
                                                  image=self.photo_ultrasonic_sensor,
                                                  command=self.put_ultrasonic_sensor)
        self.button_ultrasonic_sensor.config(background='#006468', activebackground='#006468')
        self.canvas.create_window(485, 50, window=self.button_ultrasonic_sensor)

    def create_photo_keyboard(self):
        self.keyboard = self.img_keyboard.resize((55, 60), Image.ANTIALIAS)
        self.photo_keyboard = ImageTk.PhotoImage(self.keyboard)
        self.button_keyboard = tk.Button(self.canvas, width=60, height=90,
                                         image=self.photo_keyboard,
                                         command=self.put_keyboard)
        self.button_keyboard.config(background='#006468', activebackground='#006468')
        self.canvas.create_window(555, 50, window=self.button_keyboard)

    def create_photo_screen(self):
        self.screen = self.img_screen.resize((60, 40), Image.ANTIALIAS)
        self.photo_screen = ImageTk.PhotoImage(self.screen)
        self.button_screen = tk.Button(self.canvas, width=66, height=90,
                                       image=self.photo_screen,
                                       command=self.put_screen)
        self.button_screen.config(background='#006468', activebackground='#006468')
        self.canvas.create_window(625, 50, window=self.button_screen)

    def create_photo_servomotor(self):
        self.servomotor = self.img_servomotor.resize((35, 50), Image.ANTIALIAS)
        self.photo_servomotor = ImageTk.PhotoImage(self.servomotor)
        self.button_servomotor = tk.Button(self.canvas, width=45, height=90,
                                           image=self.photo_servomotor,
                                           command=self.put_servomotor)
        self.button_servomotor.config(background='#006468', activebackground='#006468')
        self.canvas.create_window(687, 50, window=self.button_servomotor)
