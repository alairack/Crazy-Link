from settings import display_setting, setting
import pyglet
import glooey
import logging


logger = logging.getLogger("main.menu")


class ConfigLabel(glooey.Label):
    custom_font_name = 'Lato Regular'
    custom_font_size = 15
    custom_color = '#b9ad86'
    custom_alignment = 'center'
    custom_bold = True


class OkButton(glooey.Button):
    custom_alignment = "bottom"
    custom_text = "OK"
    custom_bottom_padding = 40

    def __init__(self):
        super().__init__()
        self.push_handlers(on_click=self.complete_config)

    def complete_config(self, w):
        display_setting.export_config("w")
        display_setting.config_file.close()
        display_setting.current_window_location = self.get_window().get_location()
        self.get_window().close()
        setting.run(display_setting.current_window_location)

    class Foreground(ConfigLabel):
        def __init__(self):
            super().__init__()


class ConfigValue(glooey.Button):
    def __init__(self, value_list, dict_key):
        super().__init__()
        self.value_list = value_list
        self.dict_key = dict_key
        self.current_select = display_setting.select_value[dict_key]
        self.foreground = self.get_foreground()
        self.foreground.set_text(f"<{self.value_list[self.current_select]}>")

    def on_click(self, w):                   # w为按钮事件必传参数
        self.current_select = self.current_select + 1
        if self.current_select >= len(self.value_list):
            self.current_select = 0

        self.foreground.set_text(f"<{self.value_list[self.current_select]}>")
        display_setting.select_value[self.dict_key] = self.current_select            # 将修改后的值存在display_setting中的字典内

    class Foreground(ConfigLabel):
        def __init__(self):
            super().__init__()


def create_option(grid, label_row, label_col, description_text, button_value_list, default_value, button_row, button_col):
    label = ConfigLabel(description_text)
    grid.add(label_row, label_col, label)
    button = ConfigValue(button_value_list, default_value)
    grid.add(button_row, button_col, button)
    return button


def create_button(grid):
    msaa_button = create_option(grid, 0, 0, "MSAA", display_setting.config_dict["msaa"], "msaa", 0, 1)
    show_fps_button = create_option(grid, 0, 2, "显示fps", display_setting.config_dict["show_fps"], "show_fps", 0, 3)
    vsync_button = create_option(grid, 1, 0, 'vsync', display_setting.config_dict["vsync"], "vsync", 1, 1)
    fullscreen_button = create_option(grid, 1, 2, "全屏", display_setting.config_dict["fullscreen"], "fullscreen", 1, 3)


def create_setting_window(width, height, window_location):
    window = pyglet.window.Window(width=width, height=height)
    display_setting.current_window = window
    window.set_location(window_location[0], window_location[1])
    gui = glooey.Gui(window)
    grid = glooey.Grid(3, 4)
    gui.add(grid)
    create_button(grid)
    button_ok = OkButton()
    gui.add(button_ok)
    pyglet.app.run()
    return window




