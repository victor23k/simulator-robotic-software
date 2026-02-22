import simulator.graphics.layers as layers

layer: layers.Layer = None
view = None

def wait_ms(ms: int):
    global view

    view.controller.wait(ms)


def refresh():
    global layer
    global view

    layer.move(view.keys_used, view.move_WASD)
    view.update_idletasks()
