from tkinter import *
import requests
from datetime import datetime
from tkcalendar import DateEntry
import json
from datetime import timedelta 
from GUI.NuevoContenedor import NuevoContenedor
from GUI.classScrollFrame import ScrollableFrame

class Contenedor():
	def __init__(self,frame,menuPrincipal):
		self.frame=Frame(frame)
		self.menuPrincipal=menuPrincipal
		self.frameMenu=Frame(frame)
		self.listaContenedores=self.dameContenedores()

		self.newContenedor=NuevoContenedor(self.frame)


	def dameContenedores(self):
		API_ENDPOINT="http://localhost:5000/contenedor"
		try:
			r = requests.get(url = API_ENDPOINT)
			data = r.json() 
			lista=data['mensaje']
			return lista
		except:
			return 0
			
			

	def crearMenuContenedor(self):
		btn_nuevo_contenedor=Button(self.frameMenu,bg="#6E5F0E",text="Nuevo \n contenedor",
			fg="white",font=("courier",18,"bold italic"),
			command=lambda:self.aparecerNuevoContenedor())
		btn_nuevo_contenedor.pack()

		btn_atras=Button(self.frameMenu,bg="#6E5F0E",text="Atras",
			fg="white",font=("courier",18,"bold italic"),
			command=lambda:self.atras())
		btn_atras.pack()	
		return self.frameMenu	

	def aparecerNuevoContenedor(self):
		self.newContenedor=NuevoContenedor(self.frame)
		frameNuevoC=self.newContenedor.esqueletoNuevoContenedor()
		frameNuevoC.grid(row=0,column=1,sticky="nsew")
		

	

	def atras(self):
		self.frameMenu.grid_forget()
		self.menuPrincipal.grid(row=0,column=0,sticky="ns")	

	def crearFrameContenedores(self):
		self.frameScroll=ScrollableFrame(self.frame)
		self.frameScroll.grid(column=1,row=0,sticky="nsew")

		for item in self.listaContenedores:
			self.crearEsqueletoLocalFrame(item,self.frameScroll.scrollable_frame)

		return self.frame		

	def crearEsqueletoLocalFrame(self,contenedor,frameScroll):
		now = datetime.now()	
		fechaCreacion=datetime.strptime(contenedor['caduca'], "%d/%m/%Y %H:%M:%S")
		caducidad=fechaCreacion+timedelta(days=2) 

		frameView=Frame(frameScroll,relief=SUNKEN,bd=3)
		frameView.pack(padx=5,pady=5)
		#Calculo cuanto falta a partir de ahora para llegar a la caducidad
		boton=Button(frameView,text=contenedor['nombre'],
			font=("Serif",22),bg="#CBC2CF",bd=2,relief=SUNKEN)
		boton.grid(row=0,column=0,padx=1,pady=1,sticky="nsew")

		lbl_cantidad=Label(frameView,text=contenedor['cantidad'],
			font=("Serif",22),bg="#EEECE1",bd=2,relief=SUNKEN)
		lbl_cantidad.grid(row=0,column=1,padx=1,pady=1,sticky="nsew")

		lbl_unidad=Label(frameView,text=contenedor['unidad'],
			font=("Serif",22),bg="#EEECE1",bd=2,relief=SUNKEN)
		lbl_unidad.grid(row=0,column=2,padx=1,pady=1,sticky="nsew")

		lbl_tiempo_de_vida=Label(frameView,text="Tiempo de vida:",
			font=("courier",22),bg="#EEECE1",bd=2)
		lbl_tiempo_de_vida.grid(row=1,column=0,padx=1,pady=1,sticky="nsew")

		if(now>caducidad):
			resultado="Caduco"
			btn_eliminar=Button(frameView,text="X",bg="red",fg="white",
				command=lambda:self.borrarContenedor(contenedor))
			btn_eliminar.grid(row=1,column=2)
		else:
			resultado=str(caducidad-now)
		

		lbl_caducidad=Label(frameView,text=resultado[:15],
			font=("Serif",18,"bold italic"),bg="#EEECE1",bd=2)
		lbl_caducidad.grid(row=1,column=1,padx=1,pady=1,sticky="nsew")


	def borrarContenedor(self,contenedor):
		API_ENDPOINT = "http://localhost:5000/contenedor/"+str(contenedor['_id'])
		r = requests.delete(url = API_ENDPOINT) 
		print(r.json())
		if r.json()['status']:
			print("contenedor eliminado con exito")		