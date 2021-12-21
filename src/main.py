import sys
import os
from cocos.director import director
from menu import create_menu
from check_openal import is_openal_exist, run_install_window
from settings import setting
import pyglet
import logging


def run():
    def run_game():
        director.init(caption="Crazy Link", style=pyglet.window.Window.WINDOW_STYLE_DEFAULT,
                  width=setting.level_info[setting.level]["column"] * (setting.square_size + 2) + 30,
                  height=setting.level_info[setting.level]["row"] * (setting.square_size + 2) + 65, resizable=True, vsync=True)

        logger.info(f"game start on {sys.platform}")
        logger.info(f"audio driver : {pyglet.media.get_audio_driver()}")  # 此代码理论上仅打印声音驱动名称，但可以使初次播放声音速度明显提升

        director.window.set_icon(setting.logo)
        menu_scene = create_menu()
        director.run(menu_scene)

    try:
        run_game()
    except Exception:
        logger.error("game is failed", exc_info = True)


def init_log():
    logger = logging.getLogger('main')
    logger.setLevel(level=logging.INFO)

    log_path = "./crazy_link"
    if not os.path.exists(log_path):
        os.mkdir(os.path.join(os.getcwd(), "crazy_link"))

    handler = logging.FileHandler("./crazy_link/logs.txt")
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)

    logger.addHandler(handler)
    logger.addHandler(console)

    return logger



logger = init_log()


if __name__ == "__main__":

    def get_display_info():
        display = pyglet.canvas.get_display()
        screen = display.get_default_screen()
        logger.info(f"display : {display} ; default screen : {screen}")
        logger.info(f"current screen mode : {screen.get_mode()}")


    get_display_info()

    if sys.platform == 'linux':
        if not is_openal_exist():
            logger.info("openal is nonexistent")
            run_install_window()
        else:
            logger.info("openal exist")
            run()
    elif sys.platform == 'win32':
        logger.info("openal exist")
        run()
