import sys
from cocos.director import director
from menu import create_menu
from settings import Settings
from check_openal import is_openal_exist, run_install_window


def run_game():
    setting = Settings()
    director.init(caption="Crazy Link", width=setting.level_info[setting.level]["column"] * (setting.square_size+2) + 30,
                  height=setting.level_info[setting.level]["row"] * (setting.square_size+2) + 65, resizable=True)
    director.window.set_icon(setting.logo)
    menu_scene = create_menu()
    director.run(menu_scene)


if __name__ == "__main__":
    if sys.platform == 'linux':
        if not is_openal_exist():
            run_install_window()
        else:
            run_game()
    elif sys.platform == 'win32':
        run_game()



