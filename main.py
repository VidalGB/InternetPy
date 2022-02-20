#	importaciones
import speedtest
import datetime
import webbrowser
from kivy.app import App
from kivymd.uix.dialog import MDDialog
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton
from kivymd.uix.list import OneLineAvatarIconListItem
from kivy.config import Config
from kivy.clock import Clock
from kivy.core.window import Window
from kivymd.utils import asynckivy
import csv
import math

#	tamaño de ventana
Window.size = (840, 470)

#	funciones de letura y escritura
def lectura(variable):
	with open ('datos/datos.csv') as archivo:
		contenido = csv.reader(archivo, delimiter = ';')
		for line in contenido:
			if line[0] == variable:
				return line[1]

def escritura(variable, escribir):
	guardado = []
	n = 0
	with open ('datos/datos.csv') as archivo:
		contenido = csv.reader(archivo, delimiter = ';')
		for line in contenido:
			if line[0] == variable:
				del line[1]
				del line[0]
			guardado.append(line)
		for elemento in guardado:
			if elemento == []:
				del guardado[n]
			n += 1
	with open ('datos/datos.csv', 'w', newline = '') as archivo:
		write = csv.writer(archivo, delimiter = ';')
		write.writerows(guardado)
		write.writerow([variable,escribir])
	archivo.close()

def lectura2(ID):
	idiomas = {"Español":1,"English":2, "Portugues":3}
	with open ('datos/textos.csv') as archivo:
		contenido = csv.reader(archivo, delimiter = ';')
		posicion = idiomas[lectura("lenguage")]
		for line in contenido:
			if line[0] == ID:
				return line[posicion]

#	clases
class ItemConfirm(OneLineAvatarIconListItem):
	text = f"{lectura2('idioma_i')}"
	if lectura("lenguage") == "English":
		active = True
	else:
		active = False

class ItemConfirm2(OneLineAvatarIconListItem):
	text = f"{lectura2('idioma_e')}"
	if lectura("lenguage") == "Español":
		active = True
	else:
		active = False

class ItemConfirm3(OneLineAvatarIconListItem):
	text = f"{lectura2('idioma_p')}"
	if lectura("lenguage") == "Portugues":
		active = True
	else:
		active = False

#	aplicacion
class Internet(MDApp):
#	funciones globales
	inicio = lectura("inicio")
	dialog_oscuro = None
	dialog_idioma = None
	ERROR = None
	lenguaje = lectura("lenguage")
	global idiomas
	idiomas = {"Español":1,"English":2, "Portugues":3}
	global Screen_M
	Screen_M = ScreenManager()
	List = ['logo_screen','inicio_screen','login_screen','info_screen','settings_screen','resultados_screen','datos_screen']

#	funciones de inicio
	def __init__(self, *args, **kwargs):
		MDApp.__init__(self, *args, **kwargs)
		self.title = "QuickWify"
		self.theme_cls.primary_palette = "Blue"
		self.theme_cls.accent_palette = "Teal"
		self.icon="datos/imagenes/logo.ico"
		self.theme_cls.theme_style = lectura("color")

	def on_start(self):
		Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
		Config.set('graphics', 'resizable', False)
		Config.write()
		Clock.schedule_once(self.animacion_screen, 3)

#	contruccion
	def build(self):
		Screen_M.add_widget(Builder.load_file("datos/screen/logo_screen.kv"))
		Screen_M.add_widget(Builder.load_file("datos/screen/inicio_screen.kv"))
		Screen_M.add_widget(Builder.load_file("datos/screen/login_screen.kv"))
		Screen_M.add_widget(Builder.load_file("datos/screen/info_screen.kv"))
		Screen_M.add_widget(Builder.load_file("datos/screen/settings_screen.kv"))
		Screen_M.add_widget(Builder.load_file("datos/screen/resultados_screen.kv"))
		Screen_M.add_widget(Builder.load_file("datos/screen/datos_screen.kv"))
		Screen_M.add_widget(Builder.load_file("datos/screen/error_screen.kv"))
		escritura("progreso", "0")
		menu_items = [{"viewclass": "OneLineListItem", "text": f"{self.mostrar('b_ajustes', True)}", "height": 40, "on_release": lambda x=f"{self.mostrar('b_ajustes', True)}": self.cambio_screen("settings_screen")},{"viewclass": "OneLineListItem","text": f"{self.mostrar('b_info', True)}","height": 45,"on_release": lambda x=f"{self.mostrar('b_info', True)}": self.cambio_screen("info_screen")}]
		self.menu = MDDropdownMenu(items=menu_items,width_mult=2.3,)
		return Screen_M

#	selector de idioma
	def idioma_configuracion_dialog(self):
		if not self.dialog_idioma:
			self.dialog_idioma = MDDialog(title= f"{self.mostrar('idioma_dialog', True)}",type="confirmation",items=[ItemConfirm(),ItemConfirm2(),ItemConfirm3(),],buttons=[MDFlatButton(text="Ok",theme_text_color="Custom",text_color=self.theme_cls.primary_color,on_release = self.cerrar,),],)
		self.dialog_idioma.open()

	def lec_idioma(self, instance_check, idioma):
		escritura("lenguage", idioma)
		instance_check.active = True
		check_list = instance_check.get_widgets(instance_check.group)
		for check in check_list:
			if check != instance_check:
				check.active = False

	def cerrar(self, obj):
		self.dialog_idioma.dismiss()
		if self.lenguaje != lectura("lenguage"):
			self.lenguaje = lectura("lenguage")
			self.inicio_actualizar()
			self.cambio_screen("inicio_screen")
			self.settings_actualizar()
			self.datos_actualizar()
			self.info_actualizar()
			self.error_actualizar()

#	modo oscuro
	def modo_oscuro_dialog(self):
		if not self.dialog_oscuro:
			if self.theme_cls.theme_style == "Light":
				self.dialog_oscuro = MDDialog(text = f"{self.mostrar('modo_oscuro', True)}",radius=[20, 7, 20, 7],buttons =[MDFlatButton(text= f"{self.mostrar('b1_modo_oscuro', True)}", theme_text_color = "Custom", text_color = self.theme_cls.primary_color, on_release = self.modo_oscuro_on),],)
			else:
				self.dialog_oscuro = MDDialog(text = f"{self.mostrar('modo_oscuro', True)}",radius=[20, 7, 20, 7],buttons =[MDFlatButton(text = f"{self.mostrar('b2_modo_oscuro', True)}", theme_text_color = "Custom", text_color = self.theme_cls.primary_color, on_release = self.modo_oscuro_off),],)
		self.dialog_oscuro.open()

	def modo_oscuro_off(self, obj):
		self.theme_cls.theme_style = "Light"
		escritura("color", "Light")
		self.dialog_oscuro.dismiss()
		self.dialog_oscuro = MDDialog(text = f"{self.mostrar('modo_oscuro', True)}",radius=[20, 7, 20, 7],buttons =[MDFlatButton(text= f"{self.mostrar('b1_modo_oscuro', True)}", theme_text_color = "Custom", text_color = self.theme_cls.primary_color, on_release = self.modo_oscuro_on),],)

	def modo_oscuro_on(self, obj):
		self.theme_cls.theme_style = "Dark"
		escritura("color", "Dark")
		self.dialog_oscuro.dismiss()
		self.dialog_oscuro = MDDialog(text = f"{self.mostrar('modo_oscuro', True)}",radius=[20, 7, 20, 7],buttons =[MDFlatButton(text = f"{self.mostrar('b2_modo_oscuro', True)}", theme_text_color = "Custom", text_color = self.theme_cls.primary_color, on_release = self.modo_oscuro_off),],)

#	test wifi
	def Test(self):
		try:
			wifi = speedtest.Speedtest()
			time = datetime.datetime.now().strftime("%D · %H:%M")
			escritura("fecha", time)
			download = round((round(wifi.download()) / 1048576), 2)
			escritura("descarga", download)
			upload = round((round(wifi.upload()) / 1048576), 2)
			escritura("subida", upload)
			ping = wifi.results.ping
			escritura("ping", ping)
		except:
			return True

#	menu
	def abrir(self, button):
		self.menu.caller = button
		self.menu.open()

#	cambio de pantalla

	def animacion_screen(self, dt):
		if self.inicio == "True":
			Screen_M.current = "datos_screen"
		else:
			Screen_M.current = "inicio_screen"

	def cambio_screen(self, screen):
		Screen_M.current = screen
		if screen == "settings_screen" or screen == "info_screen":
			self.menu.dismiss()

#	boton de guardado de datos
	def guardar(self):
		List = ['a','b','c','d','e','f','g','h','i','j','k','l','m','o','p','q','r','s','t','u','v','w','x','y','z','°','|','¬','!','"',"'",'#','$','%','&','/','(',')','=','?','¡','¿',',',';','.',':','-','_','@','<','>','{','}','[',']','^','`','´','¨','+','*','~']
		Screen_M.get_screen('datos_screen').ids.subida.error = False
		Screen_M.get_screen('datos_screen').ids.bajada.error = False
		texto_s = Screen_M.get_screen('datos_screen').ids.subida.text
		subida = list(texto_s)
		texto_b = Screen_M.get_screen('datos_screen').ids.bajada.text
		bajada = list(texto_b)
		if len(subida) >= 6 or len(subida) == 0:
			Screen_M.get_screen('datos_screen').ids.subida.error = True
		for letra in subida:
			for elementos in List:
				if letra == elementos:
					Screen_M.get_screen('datos_screen').ids.subida.error = True
		if len(bajada) >= 6 or len(bajada) == 0:
			Screen_M.get_screen('datos_screen').ids.bajada.error = True
		for letra in bajada:
			for elementos in List:
				if letra == elementos:
					Screen_M.get_screen('datos_screen').ids.bajada.error = True
		if Screen_M.get_screen('datos_screen').ids.bajada.error == False and Screen_M.get_screen('datos_screen').ids.subida.error == False:
			escritura("datos_subida", texto_s)
			escritura("datos_descarga", texto_b)
			if self.inicio == "True":
				self.cambio_screen("inicio_screen")
				escritura("inicio", "False")
			else:
				self.cambio_screen("settings_screen")

#	funciones de muestreo
	def mostrar(self, ID, clasificar):
		if clasificar:
			with open ('datos/textos.csv') as archivo:
				contenido = csv.reader(archivo, delimiter = ';')
				posicion = idiomas[self.lenguaje]
				for line in contenido:
					if line[0] == ID:
						return line[posicion]
		else:
			prin = lectura(f"{ID}")
			return prin

	def text_info(self):
		List = ["  QuickWify es una aplicación de escritorio creada con Python, \n  para poder medir las velocidades tanto de subida como de bajada de su internet.\n  QuickWify no guarda ni recopila ningún dato sobre sus usuarios.\n  Esta aplicación fue creada sin fines de lucro por @VidalGB. \n  Otros agradecimientos a los traductores y a la diseñadora/artista @rxaxven (Instagram)","  QuickWify is a desktop application created with Python,\n  to measure both the upload and download speed of your internet.\n  QuickWify does not save or collect any data about its users.\n  This application was created for non-profit by @VidalGB.\n  Other thanks to the translators and the designer/artist @rxaxven (Instagram)","  QuickWify é um aplicativo de desktop criado com Python,\n  para poder medir as velocidades de upload e download da sua internet.\n  QuickWify não salva nem coleta dados sobre seus usuários.\n  Este aplicativo foi criado sem fins lucrativos por @VidalGB.\n  Outros agradecimentos aos tradutores e ao designer/artista @rxaxven (Instagram)"]
		posicion = idiomas[self.lenguaje] -1
		return List[posicion]

	def login_actualizar(self):
		Screen_M.get_screen('login_screen').ids.Bar.title = f"{self.mostrar('p_medicion', True)}"
		Screen_M.get_screen('login_screen').ids.porsentaje.text = f"{self.mostrar('progreso', True)}: {self.mostrar('progreso', False)}%"
		Screen_M.get_screen('login_screen').ids.bar.value = int(lectura('progreso'))
		async def login_actualizar():
			for n in range(0,101,25):
				await asynckivy.sleep(1.5)
				escritura("progreso", f"{n}")
				text_porsentaje = Screen_M.get_screen('login_screen').ids.porsentaje
				text_porsentaje.text = f"{self.mostrar('progreso', True)}: {self.mostrar('progreso', False)}%"
				value_bar = Screen_M.get_screen('login_screen').ids.bar
				value_bar.value = int(lectura('progreso'))
				if n > 75:
					self.ERROR = self.Test()
				if self.ERROR:
					escritura("progreso", "0")
					self.cambio_screen("error_screen")
					value_bar.value = 0
					text_porsentaje.text = f"{self.mostrar('progreso', True)}: {self.mostrar('progreso', False)}%"
					self.ERROR = False
					break
				if n == 100:
					escritura("progreso", "0")
					await asynckivy.sleep(1)
					self.cambio_screen("resultados_screen")
					self.resultados_actualizar()
					value_bar.value = 0
					text_porsentaje.text = f"{self.mostrar('progreso', True)}: {self.mostrar('progreso', False)}%"
		asynckivy.start(login_actualizar())

	def resultados_actualizar(self):
		d_subida = int(lectura("datos_subida"))
		d_descarga = int(lectura("datos_descarga"))
		subida = round(float(lectura("subida")))
		descarga = round(float(lectura("descarga")))
		por_download = descarga * 100 / d_descarga
		por_upload = subida * 100 / d_subida
		if por_download <= 33 and por_download >= 0:
			Screen_M.get_screen('resultados_screen').ids.download.color = (1,0,0,1)
			Screen_M.get_screen('resultados_screen').ids.t_download.text_color = (1,0,0,1)
		elif por_download <= 66 and por_download > 33:
			Screen_M.get_screen('resultados_screen').ids.download.color = (0,0,1,1)
			Screen_M.get_screen('resultados_screen').ids.t_download.text_color = (0,0,1,1)
		elif por_download > 66:
			Screen_M.get_screen('resultados_screen').ids.download.color = (0,1,0,1)
			Screen_M.get_screen('resultados_screen').ids.t_download.text_color = (0,1,0,1)
		if por_upload <= 33 and por_upload >= 0:
			Screen_M.get_screen('resultados_screen').ids.upload.color = (1,0,0,1)
			Screen_M.get_screen('resultados_screen').ids.t_upload.text_color = (1,0,0,1)
		elif por_upload <= 66 and por_upload > 33:
			Screen_M.get_screen('resultados_screen').ids.upload.color = (0,0,1,1)
			Screen_M.get_screen('resultados_screen').ids.t_upload.text_color = (0,0,1,1)
		elif por_upload > 66:
			Screen_M.get_screen('resultados_screen').ids.upload.color = (0,1,0,1)
			Screen_M.get_screen('resultados_screen').ids.t_upload.text_color = (0,1,0,1)
		Screen_M.get_screen('resultados_screen').ids.upload.value = por_upload
		Screen_M.get_screen('resultados_screen').ids.download.value = por_download
		Screen_M.get_screen('resultados_screen').ids.t_upload.text = f"{self.mostrar('subida', False)} MB/s"
		Screen_M.get_screen('resultados_screen').ids.t_download.text = f"{self.mostrar('descarga', False)} MB/s"
		Screen_M.get_screen('resultados_screen').ids.t_ping.text = f"{self.mostrar('ping', False)} Ping"

	def inicio_actualizar(self):
		Screen_M.get_screen('inicio_screen').ids.t_tiempo.text = f"{self.mostrar('tiempo', True)}: {self.mostrar('fecha', False)}"
		Screen_M.get_screen('inicio_screen').ids.t_upload.text = f"{self.mostrar('subida', False)} MB/s"
		Screen_M.get_screen('inicio_screen').ids.t_download.text = f"{self.mostrar('descarga', False)} MB/s"
		Screen_M.get_screen('inicio_screen').ids.t_ping.text = f"{self.mostrar('ping', False)} Ping"
		menu_items = [{"viewclass": "OneLineListItem", "text": f"{self.mostrar('b_ajustes', True)}", "height": 40, "on_release": lambda x=f"{self.mostrar('b_ajustes', True)}": self.cambio_screen("settings_screen")},{"viewclass": "OneLineListItem","text": f"{self.mostrar('b_info', True)}","height": 45,"on_release": lambda x=f"{self.mostrar('b_info', True)}": self.cambio_screen("info_screen")}]
		self.menu = MDDropdownMenu(items=menu_items,width_mult=2.3,)

	def settings_actualizar(self):
		ItemConfirm.text = f"{self.mostrar('idioma_i', True)}"
		ItemConfirm2.text = f"{self.mostrar('idioma_e', True)}"
		ItemConfirm3.text = f"{self.mostrar('idioma_p', True)}"
		if self.lenguaje == "English":
			ItemConfirm.active = True
		else:
			ItemConfirm.active = False
		if self.lenguaje == "Español":
			ItemConfirm2.active = True
		else:
			ItemConfirm2.active = False
		if self.lenguaje == "Portugues":
			ItemConfirm3.active = True
		else:
			ItemConfirm3.active = False
		if self.theme_cls.theme_style == "Light":
			self.dialog_oscuro = MDDialog(text = f"{self.mostrar('modo_oscuro', True)}",radius=[20, 7, 20, 7],buttons =[MDFlatButton(text= f"{self.mostrar('b1_modo_oscuro', True)}", theme_text_color = "Custom", text_color = self.theme_cls.primary_color, on_release = self.modo_oscuro_on),],)
		else:
			self.dialog_oscuro = MDDialog(text = f"{self.mostrar('modo_oscuro', True)}",radius=[20, 7, 20, 7],buttons =[MDFlatButton(text = f"{self.mostrar('b2_modo_oscuro', True)}", theme_text_color = "Custom", text_color = self.theme_cls.primary_color, on_release = self.modo_oscuro_off),],)
		self.dialog_idioma = MDDialog(title= f"{self.mostrar('idioma_dialog', True)}",type="confirmation",items=[ItemConfirm(),ItemConfirm2(),ItemConfirm3(),],buttons=[MDFlatButton(text="Ok",theme_text_color="Custom",text_color=self.theme_cls.primary_color,on_release = self.cerrar,),],)
		Screen_M.get_screen('settings_screen').ids.oscuro.text = f"{self.mostrar('modo_oscuro', True)}"
		Screen_M.get_screen('settings_screen').ids.conf.text = f"{self.mostrar('b_datos', True)}"
		Screen_M.get_screen('settings_screen').ids.idioma.text = f"{self.mostrar('lenguaje', True)}"
		Screen_M.get_screen('settings_screen').ids.bar.title = f"{self.mostrar('p_ajustes', True)}"

	def datos_actualizar(self):
		Screen_M.get_screen('datos_screen').ids.bar.title = f"{self.mostrar('p_datos', True)}"
		Screen_M.get_screen('datos_screen').ids.texto.text = f"{self.mostrar('T_conf', True)}"
		Screen_M.get_screen('datos_screen').ids.subida.hint_text = f"{self.mostrar('cuadro_s', True)}"
		Screen_M.get_screen('datos_screen').ids.subida.helper_text = f"{self.mostrar('cuadro_s-a', True)}"
		Screen_M.get_screen('datos_screen').ids.bajada.hint_text = f"{self.mostrar('cuadro_b', True)}"
		Screen_M.get_screen('datos_screen').ids.bajada.helper_text = f"{self.mostrar('cuadro_b-a', True)}"
		Screen_M.get_screen('datos_screen').ids.button.text = f"{self.mostrar('B_conf', True)}"

	def info_actualizar(self):
		Screen_M.get_screen('info_screen').ids.bar.title = f"{self.mostrar('b_info', True)}"
		Screen_M.get_screen('info_screen').ids.text.text = self.text_info()
		Screen_M.get_screen('info_screen').ids.codigo.text = f"{self.mostrar('b_codigo', True)}"
		Screen_M.get_screen('info_screen').ids.contacto.text = f"{self.mostrar('b_contacto', True)}"

	def error_actualizar(self):
		Screen_M.get_screen('error_screen').ids.t_error.text = f"{self.mostrar('t_error', True)}"

#	Botones Info
	def button_info(self, contacto):
		if not contacto:
			webbrowser.open("https://github.com/VidalGB/InternetPy", new=2, autoraise=True)
		else:
			webbrowser.open("https://mail.google.com/mail/u/1/#inbox?compose=GTvVlcSHvnnrkvHzbwwdSPWmlFnjcKtRqFsQLTlCCVVWDMwmLbnjKcGhmHfTWScpnMGZVjvBxhVSD", new=2, autoraise=True)

#	inicio
if __name__ == '__main__':
	Internet().run()