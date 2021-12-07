import os
import pyglet
import glooey


def is_openal_exist():
    cmd = "whereis libopenal.so.1"
    return_message = os.popen(cmd).readline()
    if len(return_message) >= 32:
        return True
    else:
        return False


class TextForm(glooey.Form):
    custom_alignment = 'bottom left'
    custom_left_padding = 81
    custom_bottom_padding = 58

    class Label(glooey.EditableLabel):
        custom_font_name = 'Lato Regular'
        custom_font_size = 13
        custom_color = '#b9ad86'
        custom_horz_padding = 5
        custom_width_hint = 432

    class Base(glooey.Background):
        custom_center = pyglet.resource.texture('res/text_frame/form_center.png')
        custom_left = pyglet.resource.image('res/text_frame/form_left.png')
        custom_right = pyglet.resource.image('res/text_frame/form_right.png')


class WesnothLabel(glooey.Label):
    custom_font_name = 'Lato Regular'
    custom_font_size = 24
    custom_color = '#b9ad86'
    custom_alignment = 'top'
    custom_bottom_padding = 9


class WesnothButton(glooey.Button):
    Foreground = WesnothLabel
    Background = glooey.Image
    custom_base_image = pyglet.resource.image('res/dialog/base.png')
    custom_over_image = pyglet.resource.image('res/dialog/over.png')
    custom_down_image = pyglet.resource.image('res/dialog/down.png')


class WesnothDialog(glooey.YesNoDialog):

    class Decoration(glooey.Background):
        custom_center = pyglet.resource.texture('res/dialog/center.png')
        custom_top = pyglet.resource.texture('res/dialog/top.png')
        custom_bottom = pyglet.resource.texture('res/dialog/bottom.png')
        custom_left = pyglet.resource.texture('res/dialog/left.png')
        custom_right = pyglet.resource.texture('res/dialog/right.png')
        custom_top_left = pyglet.resource.image('res/dialog/top_left.png')
        custom_top_right = pyglet.resource.image('res/dialog/top_right.png')
        custom_bottom_left = pyglet.resource.image('res/dialog/bottom_left.png')
        custom_bottom_right = pyglet.resource.image('res/dialog/bottom_right.png')

    class Box(glooey.Grid):
        def __init__(self):
            super().__init__()

        custom_right_padding = 14
        custom_top_padding = 14
        custom_left_padding = 17
        custom_bottom_padding = 10
        custom_cell_padding = 13

    class Buttons(glooey.HBox):
        def __init__(self):
            super().__init__()

        custom_cell_padding = 50
        custom_alignment = 'right'

    class Content(WesnothLabel):
        custom_text = '您缺少 openal 库，\n请点击“install”\n或在命令行运行下面的代码\n以安装openal。\n安装完成后，请重启此程序'

    class YesButton(WesnothButton):
        custom_text = 'Install'

        def on_mouse_press(self, x, y, button, modifiers):
            os.system("gnome-terminal --title=install-openal -- bash -c 'sudo apt install libopenal1; exec bash'")
            pyglet.app.exit()

    class NoButton(WesnothButton):
        custom_text = 'Cancel'

        def on_mouse_press(self, x, y, button, modifiers):
            pyglet.app.exit()


def run_install_window():
    window = pyglet.window.Window(width=600, height=500)
    pyglet.resource.path.append('res/fonts')
    pyglet.resource.reindex()
    pyglet.resource.add_font('Lato-Regular.ttf')
    form = TextForm(text="sudo apt install libopenal1")
    gui = glooey.Gui(window)
    dialog = WesnothDialog()
    gui.add(dialog)
    gui.add(form)
    pyglet.app.run()
