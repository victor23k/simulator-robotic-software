class Element:

    def __init__(self):
        """
        Constructor for Element
        """
        self.value = 0

    def get_value(self, pin=-1):
        """
        Gets the value (digital or analog) of the element
        Arguments:
            pin: the pin to read (only needed in case the
            element uses 2 or more pins)
        Returns:
            The value of the element
        """
        return self.value

    def set_value(self, pin, value):
        """
        Writes a value into an element
        Arguments:
            pin: the pin to write (only needed in case the
            element uses 2 or more pins)
            value: the value to write
        """
        self.value = value

    def get_pulse(self, pin, value):
        """
        Reads a pulse value from a pin
        Arguments:
            pin: the pin to read from
            value: the value to read
        Returns:
            The read value or None if none read
        """
        return None


class Servo(Element):

    def __init__(self):
        """
        Constructor for servo class.
        The servo will be rotational.
        """
        self.pin = -1
        self.min = 544  # default arduino value
        self.max = 2400  # default arduino value
        self.value = 90  # stopped (180 and 0 full speed)

    def set_value(self, pin, value):
        """
        Writes speed to servo.
        Arguments:
            angle: the value to write [0-180]
        Returns:
            True if updated, False if else
        """
        if 0 <= value <= 180:
            super().set_value(pin, value)
            return True
        return False

    def get_pin_type(self):
        """
        Returns connection type needed for the pin
        """
        return "digital"


class Button(Element):

    def __init__(self):
        """
        Constructor for button
        """
        self.pin = -1
        self.value = 1

    def set_value(self, pin, value):
        if value == 1 or value == 0:
            super().set_value(pin, value)
            return True
        return False

    def get_pin_type(self):
        """
        Returns connection type needed for the pin
        """
        return "digital"


class Joystick(Element):

    def __init__(self):
        """
        Constructor for joystick
        """
        self.pinx = -1
        self.piny = -1
        self.pinb = -1
        self.dx = 500
        self.dy = 500
        self.value = 1

    def get_value(self, pin):
        """
        Gets the analog value of the selected pin
        Arguments:
            pin: the pin to read
        Returns:
            The value of the pin
        """
        if pin == self.pinx:
            return self.dx
        elif pin == self.piny:
            return self.dy
        elif pin == self.pinb:
            return self.value
        else:
            return None

    def set_value(self, pin, value):
        if 0 <= value <= 1023:
            if pin == self.pinx:
                self.dx = value
            elif pin == self.piny:
                self.dy = value
            elif pin == self.pinb:
                self.value = value
            else:
                return False
            return True
        return False

    def get_button_pin_type(self):
        """
        Returns connection type needed for the button pin
        """
        return "digital"

    def get_x_pin_type(self):
        """
        Returns connection type needed for the x pin
        """
        return "analog"

    def get_y_pin_type(self):
        """
        Returns connection type needed for the y pin
        """
        return "analog"


class LightSensor(Element):

    def __init__(self):
        """
        Constructor for Light sensor
        """
        self.pin = -1
        self.value = 0

    def set_value(self, pin, value):
        if value == 1 or value == 0:
            super().set_value(pin, value)
            return True
        return False

    def get_pin_type(self):
        """
        Returns connection type needed for the pin
        """
        return "digital"


class UltrasoundSensor(Element):

    def __init__(self):
        """
        Constructor for Ultrasound sensor
        """
        self.pin_trig = -1
        self.pin_echo = -1
        self.value = 0
        self.dist = -1

    def set_value(self, pin, value):
        if pin == self.pin_trig:
            if value == 1 or value == 0:
                super().set_value(pin, value)
                return True
        return False

    def get_pulse(self, pin, value):
        if pin == self.pin_echo:
            return self.dist
        return None

    def get_echo_pin_type(self):
        """
        Returns the type of the connection needed for the echo
        pin
        """
        return "digital"

    def get_trig_pin_type(self):
        """
        Returns the type of the connection needed for the trig
        pin
        """
        return "digital"


class ResistanceArduino(Element):
    def __init__(self):
        """
        Constructor for resistance
        A resistance has two pins and a value
        """
        self.pin1 = -1
        self.pin2 = -1
        self.value = 10

    def get_pin1_type(self):
        """
        Returns connection type needed for the pin1
        """
        return "both"

    def get_pin2_type(self):
        """
        Returns connection type needed for the pin2
        """
        return "both"

    def set_value(self, value):
        self.value = value


class ButtonArduino(Element):
    def __init__(self):
        """
        Constructor for button
        A button has four pins and a state
        """
        self.pin1 = -1
        self.pin2 = -1
        self.pin3 = -1
        self.pin4 = -1
        self.state = True

    def get_pin1_type(self):
        """
        Returns connection type needed for the pin1
        """
        return "both"

    def get_pin2_type(self):
        """
        Returns connection type needed for the pin2
        """
        return "both"

    def get_pin3_type(self):
        """
        Returns connection type needed for the pin3
        """
        return "both"

    def get_pin4_type(self):
        """
        Returns connection type needed for the pin4
        """
        return "both"

    def open(self):
        """Open the button"""
        self.state = False

    def close(self):
        """Close the button"""
        self.state = True


class PotentiometerArduino(Element):
    def __init__(self):
        """
        Constructor for potentiometer
        A potentiometer has three pins and a value
        """
        self.pin1 = -1
        self.pin2 = -1
        self.pin3 = -1
        self.value = 100

    def get_pin1_type(self):
        """
        Returns connection type needed for the pin1
        """
        return "both"

    def get_pin2_type(self):
        """
        Returns connection type needed for the pin2
        """
        return "both"

    def get_pin3_type(self):
        """
        Returns connection type needed for the pin3
        """
        return "both"

    def set_value(self, value):
        """The value must be between 0 and 100"""
        if 0 <= value <= 100:
            self.value = value


class LedArduino(Element):
    def __init__(self):
        """
        Constructor for LED
        A LED has two pins, a state and a color
        - Color: 1 for red, 2 for yellow and 3 for green
            In future expansions, more colors could be added
        """
        self.pin1 = -1
        self.pin2 = -1
        self.state = False
        self.color = 1

    def get_pin1_type(self):
        """
        Returns connection type needed for the pin1
        """
        return "both"

    def get_pin2_type(self):
        """
        Returns connection type needed for the pin2
        """
        return "both"

    def set_on(self):
        """Turns on the LED"""
        self.state = True

    def set_off(self):
        """Turns off the LED"""
        self.state = False

    def set_color(self, color):
        """For now there are only three colors"""
        if color == 1 or color == 2 or color == 3:
            self.color = color


class BuzzerArduino(Element):
    def __init__(self):
        """
        Constructor for buzzer
        A buzzer has three pins and a state
        """
        self.pin1 = -1
        self.pin2 = -1
        self.pin3 = -1
        self.state = False

    def get_pin1_type(self):
        """
        Returns connection type needed for the pin1
        """
        return "both"

    def get_pin2_type(self):
        """
        Returns connection type needed for the pin2
        """
        return "both"

    def get_pin3_type(self):
        """
        Returns connection type needed for the pin3
        """
        return "both"

    def set_on(self):
        """Turns on the buzzer"""
        self.state = True

    def set_off(self):
        """Turns off the buzzer"""
        self.state = False


class RGBArduino(Element):
    def __init__(self):
        """
        Constructor for LED RGB
        A LED RGB has four pins and a value
        """
        self.pin1 = -1
        self.pin2 = -1
        self.pin3 = -1
        self.pin4 = -1
        self.value = 1

    def get_pin1_type(self):
        """
        Returns connection type needed for the pin1
        """
        return "digital"

    def get_pin2_type(self):
        """
        Returns connection type needed for the pin2
        """
        return "digital"

    def get_pin3_type(self):
        """
        Returns connection type needed for the pin3
        """
        return "digital"

    def get_pin4_type(self):
        """
        Returns connection type needed for the pin4
        """
        return "both"

    def set_value(self, value):
        """Sets the value of the LED to a certain value"""
        self.value = value


class LightSensorArduino(Element):
    def __init__(self):
        """
        Constructor for Light Sensor
        A Light sensor has three pins and a sensor
        """
        self.pin1 = -1
        self.pin2 = -1
        self.pin3 = -1
        self.sensor = False

    def get_pin1_type(self):
        """
        Returns connection type needed for the pin1
        """
        return "digital"

    def get_pin2_type(self):
        """
        Returns connection type needed for the pin2
        """
        return "digital"

    def get_pin3_type(self):
        """
        Returns connection type needed for the pin3
        """
        return "analog"

    def set_sensor_on(self):
        """Turns the sensor on"""
        self.sensor = True

    def set_sensor_off(self):
        """Turns the sensor off"""
        self.sensor = False


class PIRSensorArduino(Element):
    def __init__(self):
        """
        Constructor for PIR Sensor
        A PIR sensor has three pins and a sensor
        """
        self.pin1 = -1
        self.pin2 = -1
        self.pin3 = -1
        self.sensor = False

    def get_pin1_type(self):
        """
        Returns connection type needed for the pin1
        """
        return "digital"

    def get_pin2_type(self):
        """
        Returns connection type needed for the pin2
        """
        return "digital"

    def get_pin3_type(self):
        """
        Returns connection type needed for the pin3
        """
        return "digital"

    def set_sensor_on(self):
        """Turns the sensor on"""
        self.sensor = True

    def set_sensor_off(self):
        """Turns the sensor off"""
        self.sensor = False


class VibrationSensorArduino(Element):
    def __init__(self):
        """
        Constructor for Vibration Sensor
        A Vibration sensor has three pins and a sensor
        """
        self.pin1 = -1
        self.pin2 = -1
        self.pin3 = -1
        self.sensor = True

    def get_pin1_type(self):
        """
        Returns connection type needed for the pin1
        """
        return "digital"

    def get_pin2_type(self):
        """
        Returns connection type needed for the pin2
        """
        return "digital"

    def get_pin3_type(self):
        """
        Returns connection type needed for the pin3
        """
        return "digital"

    def set_sensor_on(self):
        """Turns the sensor on"""
        self.sensor = True

    def set_sensor_off(self):
        """Turns the sensor off"""
        self.sensor = False


class InfraredSensorArduino(Element):
    def __init__(self):
        """
        Constructor for Infrared Sensor
        An Infrared sensor has three pins and a sensor
        """
        self.pin1 = -1
        self.pin2 = -1
        self.pin3 = -1
        self.sensor = True

    def get_pin1_type(self):
        """
        Returns connection type needed for the pin1
        """
        return "digital"

    def get_pin2_type(self):
        """
        Returns connection type needed for the pin2
        """
        return "digital"

    def get_pin3_type(self):
        """
        Returns connection type needed for the pin3
        """
        return "digital"

    def set_sensor_on(self):
        """Turns the sensor on"""
        self.sensor = True

    def set_sensor_off(self):
        """Turns the sensor off"""
        self.sensor = False


class UltrasoundSensorArduino(Element):
    def __init__(self):
        """
        Constructor for Ultrasound Sensor
        An Ultrasound sensor has four pins and a sensor
        """
        self.pin1 = -1
        self.pin2 = -1
        self.pin3 = -1
        self.pin4 = -1
        self.sensor = True

    def get_pin1_type(self):
        """
        Returns connection type needed for the pin1
        """
        return "digital"

    def get_pin2_type(self):
        """
        Returns connection type needed for the pin2
        """
        return "digital"

    def get_pin3_type(self):
        """
        Returns connection type needed for the pin3
        """
        return "digital"

    def get_pin4_type(self):
        """
        Returns connection type needed for the pin4
        """
        return "digital"

    def set_sensor_on(self):
        """Turns the sensor on"""
        self.sensor = True

    def set_sensor_off(self):
        """Turns the sensor off"""
        self.sensor = False


class KeyBoardArduino(Element):
    def __init__(self):
        """
        Constructor for keyboard
        A keyboard has eight pins
        """
        self.pin1 = -1
        self.pin2 = -1
        self.pin3 = -1
        self.pin4 = -1
        self.pin5 = -1
        self.pin6 = -1
        self.pin7 = -1
        self.pin8 = -1

    def get_pin1_type(self):
        """
        Returns connection type needed for the pin1
        """
        return "digital"

    def get_pin2_type(self):
        """
        Returns connection type needed for the pin2
        """
        return "digital"

    def get_pin3_type(self):
        """
        Returns connection type needed for the pin3
        """
        return "digital"

    def get_pin4_type(self):
        """
        Returns connection type needed for the pin4
        """
        return "digital"

    def get_pin5_type(self):
        """
        Returns connection type needed for the pin5
        """
        return "digital"

    def get_pin6_type(self):
        """
        Returns connection type needed for the pin6
        """
        return "digital"

    def get_pin7_type(self):
        """
        Returns connection type needed for the pin7
        """
        return "digital"

    def get_pin8_type(self):
        """
        Returns connection type needed for the pin8
        """
        return "digital"


class ScreenArduino(Element):
    def __init__(self):
        """
        Constructor for Screen
        A screen has four pins
        """
        self.pin1 = -1
        self.pin2 = -1
        self.pin3 = -1
        self.pin4 = -1

    def get_pin1_type(self):
        """
        Returns connection type needed for the pin1
        """
        return "digital"

    def get_pin2_type(self):
        """
        Returns connection type needed for the pin2
        """
        return "digital"

    def get_pin3_type(self):
        """
        Returns connection type needed for the pin3
        """
        return "digital"

    def get_pin4_type(self):
        """
        Returns connection type needed for the pin4
        """
        return "digital"


class ServomotorArduino(Element):
    def __init__(self):
        """
        Constructor for servomotor
        A servomotor has three pins and a state
        """
        self.pin1 = -1
        self.pin2 = -1
        self.pin3 = -1
        self.state = False

    def get_pin1_type(self):
        """
        Returns connection type needed for the pin1
        """
        return "digital"

    def get_pin2_type(self):
        """
        Returns connection type needed for the pin2
        """
        return "digital"

    def get_pin3_type(self):
        """
        Returns connection type needed for the pin3
        """
        return "digital"

    def set_on(self):
        """Turns on the servomotor"""
        self.state = True

    def set_off(self):
        """Turns off the servomotor"""
        self.state = False
