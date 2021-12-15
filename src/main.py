import sys
from cocos.director import director
from menu import create_menu
from check_openal import is_openal_exist, run_install_window
from settings import setting, log
import pyglet
import traceback

log.log_file.write(f"\n\n{log.get_current_time()}   Crazy_Link runs on {sys.platform}\n")
log.log_file.write(f"audio driver: {pyglet.media.get_audio_driver()}\n")     # 此代码理论上仅打印声音驱动名称，但可以使初次播放声音速度明显提升


def run_game():
    director.init(caption="Crazy Link", style=pyglet.window.Window.WINDOW_STYLE_DEFAULT,
                  width=setting.level_info[setting.level]["column"] * (setting.square_size + 2) + 30,
                  height=setting.level_info[setting.level]["row"] * (setting.square_size + 2) + 65, resizable=True, vsync=True)
    director.window.set_icon(setting.logo)
    menu_scene = create_menu()
    log.log_file.write(f"\n{log.get_current_time()}   create menu scene successfully\n")
    director.run(menu_scene)


if __name__ == "__main__":
    try:
        if sys.platform == 'linux':
            if not is_openal_exist():
                log.log_file.write("\n Warning: Openal is non-existent \n")
                run_install_window()
            else:
                run_game()
        elif sys.platform == 'win32':
            run_game()
    except Exception as e:
        traceback.print_exc()
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback, limit=None, file=log.log_file)
