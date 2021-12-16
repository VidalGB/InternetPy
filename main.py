from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.button import MDRectangleFlatButton

Apariencia = '''
<ScreenManager>:
Sinicio:

<Sinicio>:
	MDFloatLayout:
		orientation: "vertical"
		MDToolbar:
			title: "InternetSpeed"
			elevation: 15
			pos_hint: {"top": 1}
			left_action_items: [["format-list-bulleted"]]

'''

class Sinicio(Screen):
	pass

class Sinfo(Screen):
	pass

class Sajustes(Screen):
	pass


class Internet(MDApp):
	def __init__(self, *args, **kwargs):
		MDApp.__init__(self, *args, **kwargs)
		self.theme_cls.primary_palette = "Blue"
		self.theme_cls.accent_palette = "Teal"

	def build(self):
		self.Screen_M = ScreenManager()
		self.Screen_M.add_widget(Sinicio(name='inicio'))
		self.Screen_M.add_widget(Sinfo(name='informacion'))
		self.Screen_M.add_widget(Sajustes(name='ajustes'))
		return Builder.load_string(Apariencia)

if __name__ == '__main__':
	Internet().run()