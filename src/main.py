import sys
from cocos.director import director
from menu import create_menu
from check_openal import is_openal_exist, run_install_window
from settings import setting
import pyglet

pyglet.media.get_audio_driver()           # 此代码理论上仅打印声音驱动名称，但可以使初次播放声音速度明显提升


def run_game():
    director.init(caption="Crazy Link", style=pyglet.window.Window.WINDOW_STYLE_DEFAULT, resizable=True)
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
