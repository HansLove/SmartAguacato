import json 
from tkinter import *
from datetime import datetime
from tkcalendar import DateEntry
from datetime import timedelta 
import requests

class NuevoContenedor():
	def __init__(self,frame):
		self.frame=frame
		print("Creando nuevo contenedor")

	def esqueletoNuevoContenedor(self):
		aguacates=IntVar()
		self.frameLocal=Frame(self.frame)
		self.frameLocal.config(bg="#0E5506")
		
		lbl_ingresar=Label(self.frameLocal,text="Ingresar cantidad de aguacates",
			font=("Serif",20,"bold italic"),bg="#0E5506",fg="white")
		lbl_ingresar.pack(padx=10,pady=10)

		entry_aguacates=Entry(self.frameLocal,textvariable=aguacates,
			font=("Serif",20),justify="center")
		entry_aguacates.pack(padx=10,pady=10)


		grd_contenedor=Button(self.frameLocal,text="Guardar contenedor",
			bg="#87742C",fg="white",font=("Serif",20),
			command=lambda:self.nuevoContenedor(aguacates))
		grd_contenedor.pack(padx=10,pady=10)

		return self.frameLocal

	def nuevoContenedor(self,aguacates):
		now = datetime.now()

		# dd/mm/YY H:M:S
		dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
		API_ENDPOINT="http://localhost:5000/contenedor"

		data={
		"nombre":"Aguacate",
		"caduca":dt_string,
		"cantidad":aguacates.get(),
		"unidad":"Kg"
		}
		r = requests.post(url = API_ENDPOINT,data=data)

		print(r.json())

	def aparecerFrame(self,valor):
		if(valor):
			self.frameLocal.pack()
		else:
			self.frameLocal.pack_forget()