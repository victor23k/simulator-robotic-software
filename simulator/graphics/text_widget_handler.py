from logging import LogRecord, Handler
from typing import override
import tkinter

class TextWidgetHandler(Handler):
    def __init__(self, widget: tkinter.Text) -> None:
        """Initialize handler with an already created tkinter Text Widget."""

        super().__init__()
        self.widget: tkinter.Text = widget

    @override
    def emit(self, record: LogRecord) -> None:
        """Emit a record to the tkinter Text Widget."""

        self.widget.config(state=tkinter.NORMAL)
        self.widget.insert(tkinter.END, record.getMessage() + "\n",
                           record.levelname.lower())
        self.widget.see("end")
        self.widget.config(state=tkinter.DISABLED)
