from cocos.director import director
from menu import create_menu
from settings import Settings


setting = Settings()

director.init(caption="连连看", width=setting.level_info[setting.level]["column"] * (setting.square_size+2) + 30,
              height=setting.level_info[setting.level]["row"] * (setting.square_size+2) + 60, resizable=True)
menu_scene = create_menu()
director.run(menu_scene)


