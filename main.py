from cocos.director import director
from menu import create_menu


director.init(caption="连连看菜单", width=520, height=360, resizable=True)
menu_scene = create_menu()
director.run(menu_scene)