import graphics.layers as layers
import output.console as console
import output.console_gamification as console_gamification
import compiler.commands as commands
import graphics.screen_updater as screen_updater
from datetime import datetime


class RobotsController:

    def __init__(self, view):
        self.view = view
        self.console: console.Console = None
        self.robot_layer: layers.Layer = None
        self.consoleGamification = console_gamification.ConsoleGamification()
        self.arduino = commands.ArduinoCompiler(self, view.get_code())
        self.executing = False
        self.board = False
        self.new = True

    def execute(self, option_gamification):
        if not self.board:
            screen_updater.layer = self.robot_layer
            screen_updater.view = self.view
            self.view.abort_after()
            self.robot_layer.execute()
            self.console.clear()
            if self.arduino.check():
                if self.arduino.setup():
                    self.executing = True
                    self.drawing_loop()
        else:
            if self.arduino.check():
                self.probe_robot(option_gamification)

    def drawing_loop(self):
        screen_updater.refresh()
        if not self.view.keys_used:
            self.arduino.loop()
        self.view.identifier = self.view.after(10, self.drawing_loop)

    def stop(self):
        self.executing = False
        self.robot_layer.stop()
        self.view.abort_after()

    def zoom_in(self):
        self.robot_layer.zoom_in()
        self.view.change_zoom_label(self.robot_layer.drawing.zoom_percentage())

    def zoom_out(self):
        self.robot_layer.zoom_out()
        self.view.change_zoom_label(self.robot_layer.drawing.zoom_percentage())

    def configure_layer(self, drawing_canvas, hud_canvas):
        self.robot_layer.set_canvas(drawing_canvas, hud_canvas)
        self.view.change_zoom_label(self.robot_layer.drawing.zoom_percentage())

    def configure_console(self, text_component):
        self.console = console.Console(text_component)

    def change_robot(self, option):
        """
        Here you write the parts of the GUI that you want to show when a robot is chosen
        :param option: Selected robot (mobile: 0, 1, 2, linear, 3, Arduino: 4)
        :return: None
        """
        if self.robot_layer is not None:
            self.stop()
        # Mobile Robot, 2 infrared
        if option == 0:
            self.view.show_circuit_selector(True)
            self.view.show_gamification_option_selector(False)
            self.view.show_joystick(False)
            self.view.show_button_keys_movement(True)
            self.view.show_buttons_gamification(False)
            self.view.show_key_drawing(False)
            self.robot_layer = layers.MobileRobotLayer(2)
            self.board = False
        # Mobile Robot, 3 infrared
        elif option == 1:
            self.view.show_circuit_selector(True)
            self.view.show_gamification_option_selector(False)
            self.view.show_joystick(False)
            self.view.show_button_keys_movement(True)
            self.view.show_buttons_gamification(False)
            self.view.show_key_drawing(False)
            self.robot_layer = layers.MobileRobotLayer(3)
            self.board = False
        # Mobile Robot,  4 infrared
        elif option == 2:
            self.view.show_circuit_selector(True)
            self.view.show_gamification_option_selector(False)
            self.view.show_joystick(False)
            self.view.show_button_keys_movement(True)
            self.view.show_buttons_gamification(False)
            self.view.show_key_drawing(False)
            self.robot_layer = layers.MobileRobotLayer(4)
            self.board = False
        # Linear Actuator
        elif option == 3:
            self.view.show_circuit_selector(False)
            self.view.show_gamification_option_selector(False)
            self.view.show_joystick(True)
            self.view.show_button_keys_movement(True)
            self.view.show_buttons_gamification(False)
            self.view.show_key_drawing(False)
            self.robot_layer = layers.LinearActuatorLayer()
            self.board = False
        # Option for the Arduino Board
        elif option == 4:
            self.view.show_circuit_selector(False)
            self.view.show_gamification_option_selector(True)
            self.view.show_joystick(False)
            self.view.show_button_keys_movement(False)
            self.view.show_buttons_gamification(True)
            self.view.show_key_drawing(False)
            self.robot_layer = layers.ArduinoBoardLayer()
            self.board = True

    def change_circuit(self, option):
        if self.robot_layer is not None:
            self.stop()
        if isinstance(self.robot_layer, layers.MobileRobotLayer):
            self.robot_layer.set_circuit(option)

    def send_input(self, text):
        self.console.input(text)

    def update_joystick(self, elem, value):
        if elem == "dx":
            self.robot_layer.robot.joystick.dx = value
        elif elem == "dy":
            self.robot_layer.robot.joystick.dy = value
        elif elem == "button":
            self.robot_layer.robot.joystick.value = value

    def filter_console(self, options):
        messages = []
        if options['info']:
            messages.append('info')
        if options['warning']:
            messages.append('warning')
        if options['error']:
            messages.append('error')
        self.console.filter_messages(messages)

    def get_pin_data(self):
        return self.robot_layer.robot.get_data()

    def save_pin_data(self, pin_data):
        robot = self.robot_layer.robot
        self.__detach_pins(robot, pin_data)
        self.__set_pins(robot, pin_data)
        if 'servo_left' in pin_data:
            robot.detach_servo_left()
            robot.set_servo_left(robot.parse_pin(pin_data['servo_left']))
        if 'servo_right' in pin_data:
            robot.detach_servo_right()
            robot.set_servo_right(robot.parse_pin(pin_data['servo_right']))
        if 'light_mleft' in pin_data:
            robot.detach_light_mleft()
            robot.set_light_mleft(robot.parse_pin(pin_data['light_mleft']))
        if 'light_left' in pin_data:
            robot.detach_light_left()
            robot.set_light_left(robot.parse_pin(pin_data['light_left']))
        if 'light_right' in pin_data:
            robot.detach_light_right()
            robot.set_light_right(robot.parse_pin(pin_data['light_right']))
        if 'light_mright' in pin_data:
            robot.detach_light_mright()
            robot.set_light_mright(robot.parse_pin(pin_data['light_mright']))
        if 'sound_trig' in pin_data:
            robot.detach_sound_trig()
            robot.set_sound_trig(robot.parse_pin(pin_data['sound_trig']))
        if 'sound_echo' in pin_data:
            robot.detach_sound_echo()
            robot.set_sound_echo(robot.parse_pin(pin_data['sound_echo']))
        if 'button_left' in pin_data:
            robot.detach_button_left()
            robot.set_button_left(robot.parse_pin(pin_data['button_left']))
        if 'button_right' in pin_data:
            robot.detach_button_right()
            robot.set_button_right(robot.parse_pin(pin_data['button_right']))
        if 'servo' in pin_data:
            robot.detach_servo()
            robot.set_servo(robot.parse_pin(pin_data['servo']))
        if 'button_joystick' in pin_data:
            robot.detach_joystick_button()
            robot.set_joystick_button(
                robot.parse_pin(pin_data['button_joystick']))
        if 'joystick_x' in pin_data:
            robot.detach_joystick_x()
            robot.set_joystick_x(robot.parse_pin(pin_data['joystick_x']))
        if 'joystick_y' in pin_data:
            robot.detach_joystick_y()
            robot.set_joystick_y(robot.parse_pin(pin_data['joystick_y']))

    def __detach_pins(self, robot, pin_data):
        """
        Detaches all the pins present in the data from the robot
        Arguments:
            robot: the instance of the robot being modified
            pin_data: the pin data to change
        """
        if 'servo_left' in pin_data:
            robot.detach_servo_left()
        if 'servo_right' in pin_data:
            robot.detach_servo_right()
        if 'light_mleft' in pin_data:
            robot.detach_light_mleft()
        if 'light_left' in pin_data:
            robot.detach_light_left()
        if 'light_right' in pin_data:
            robot.detach_light_right()
        if 'light_mright' in pin_data:
            robot.detach_light_mright()
        if 'sound_trig' in pin_data:
            robot.detach_sound_trig()
        if 'sound_echo' in pin_data:
            robot.detach_sound_echo()
        if 'button_left' in pin_data:
            robot.detach_button_left()
        if 'button_right' in pin_data:
            robot.detach_button_right()
        if 'servo' in pin_data:
            robot.detach_servo()
        if 'button_joystick' in pin_data:
            robot.detach_joystick_button()
        if 'joystick_x' in pin_data:
            robot.detach_joystick_x()
        if 'joystick_y' in pin_data:
            robot.detach_joystick_y()

    def __set_pins(self, robot, pin_data):
        """
        Sets attaches the corresponding robot pins
        Arguments:
            robot: the instance of the robot being modified
            pin_data: the pin data to change
        """
        if 'servo_left' in pin_data:
            robot.set_servo_left(pin_data['servo_left'])
        if 'servo_right' in pin_data:
            robot.set_servo_right(pin_data['servo_right'])
        if 'light_mleft' in pin_data:
            robot.set_light_mleft(pin_data['light_mleft'])
        if 'light_left' in pin_data:
            robot.set_light_left(pin_data['light_left'])
        if 'light_right' in pin_data:
            robot.set_light_right(pin_data['light_right'])
        if 'light_mright' in pin_data:
            robot.set_light_mright(pin_data['light_mright'])
        if 'sound_trig' in pin_data:
            robot.set_sound_trig(pin_data['sound_trig'])
        if 'sound_echo' in pin_data:
            robot.set_sound_echo(pin_data['sound_echo'])
        if 'button_left' in pin_data:
            robot.set_button_left(pin_data['button_left'])
        if 'button_right' in pin_data:
            robot.set_button_right(pin_data['button_right'])
        if 'servo' in pin_data:
            robot.set_servo(pin_data['servo'])
        if 'button_joystick' in pin_data:
            robot.set_joystick_button(pin_data['button_joystick'])
        if 'joystick_x' in pin_data:
            robot.set_joystick_x(pin_data['joystick_x'])
        if 'joystick_y' in pin_data:
            robot.set_joystick_y(pin_data['joystick_y'])

    def get_code(self):
        return self.view.get_code()

    def exit(self):
        self.console.logger.close_log()

    def show_tutorial(self):
        self.robot_layer.show_tutorial()

    def show_results(self):
        self.robot_layer.show_results()

    def show_help(self, option_gamification):
        self.robot_layer.show_help(option_gamification)

    def delete_elements(self):
        self.robot_layer.delete_elements()

    def probe_robot(self, option_gamification):
        self.new = False
        code, circuit = self.robot_layer.probe(option_gamification, self.get_code(),
                               self.robot_layer.get_robot_challenge(option_gamification).get_code())
        self.console.logger.write_log('info', "El usuario ha comprobado el desafío " + str(option_gamification+1))
        mensaje = "El usuario tiene los siguientes componentes: "
        for component in self.robot_layer.drawing.components:
            mensaje += component['element'].name
            mensaje += " "
        self.console.logger.write_log('info', mensaje)
        if code and circuit:
            log = "El usuario ha completado el desafío correctamente.\nLa puntuación del usuario es de " \
                  + str(self.robot_layer.drawing.points) + "\n\n"
            self.record_results(True, option_gamification)
        else:
            log = "El usuario ha comprobado el desafío.\n"
            if not code:
                log += "\tEl código introducido no es correcto (-1 punto)\n"
            if not circuit:
                log += "\tEl circuito creado no es correcto (-1 punto)\n"
            log += "\tPuntuación actual: " + str(self.robot_layer.drawing.points) + "\n\n"
        self.consoleGamification.write_encrypted(log, option_gamification+1)

    def record_results(self, correct, challenge):
        if not self.new:
            points = self.robot_layer.drawing.points
            date = datetime.now().strftime("%d-%m-%Y")
            if challenge == 0:
                return

            if correct:
                log = date + " - El usuario ha completado el desafío " + str(challenge) + " con una nota de: " \
                      + str(points) + "\n"
            else:
                log = date + " - El usuario ha abandonado el desafío " + str(challenge) + " cuando su nota era: " \
                      + str(points) + "\n"
            self.consoleGamification.write(log)

