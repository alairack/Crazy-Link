from cocos.director import director
from menu import create_menu
from settings import Settings
import ctypes

if __name__ == "__main__":
    setting = Settings()
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("dlan.lianliankan.lianliankan.0.1")
    director.init(caption="Crazy Link", width=setting.level_info[setting.level]["column"] * (setting.square_size+2) + 30,
                  height=setting.level_info[setting.level]["row"] * (setting.square_size+2) + 65, resizable=True)

    director.window.set_icon(setting.logo)
    menu_scene = create_menu()
    director.run(menu_scene)
