import robot_components.boards as boards


def get_name():
    return "Keypad"


def get_methods():
    """
    Returns the methods of the library as a dict, whose
    key is the naming in Arduino and whose value is the
    corresponding method.
    Returns:
        A dict with the methods
    """
    methods = {}
    methods["getKey"] = ("char", "get_key", [], -1)
    return methods


def get_not_implemented():
    return []


class Keypad:

    def __init__(self, keymap, pin_rows, pin_columns,
                 size_rows, size_columns):
        """
        Constructor for Keypad class
        """
        self.board = None

    def set_board(self, board: boards.Board):
        """
        Sets the board that the robot is using
        """
        self.board = board

    def get_key(self):
        pass

    def make_keymap(self):
        pass

