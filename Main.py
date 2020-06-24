from tkinter import *
import requests
from datetime import datetime
from tkcalendar import DateEntry
import json
from datetime import timedelta 
from GUI.NuevoContenedor import NuevoContenedor
from GUI.classScrollFrame import ScrollableFrame
from GUI.Cliente.Clientes import Cliente
from GUI.Contenedor.Contenedor import Contenedor
from GUI.Pedidos.Pedido import Pedido


class Main():
	def __init__(self,root):
		self.frame=Frame(root)
		#self.frame.config(width=880,height=620)
		self.frame.pack(fill="both", expand=1)
		self.visible=False		

		self.frameMenu=Frame(self.frame)
		self.frameMenu.grid(column=0,row=0)

		self.frameTerreno=Frame(self.frame)
		self.frameTerreno.grid(column=1,row=0)
		
		contenedor=Contenedor(self.frameTerreno,self.frameMenu)
		pedidos=Pedido(self.frameTerreno,self.frameMenu)
		cliente=Cliente(self.frameTerreno,self.frameMenu,pedidos)
		
		self.frameContenedores=contenedor.crearFrameContenedores()
		self.menuContenedor=contenedor.crearMenuContenedor()

		self.frameClientes=cliente.crearFrameClientes()
		self.menuClientes=cliente.crearMenuCliente()

		self.framePedidos=pedidos.frameMainPedidos()
		self.menuPedidos=pedidos.menuPedidos()
		




	def crearEsqueleto(self):
		
		return self.frameContenedores
		

	def crearMenuPrincipal(self):
		self.btn_conte=Button(self.frameMenu,bg="#6E5F0E",text="Contenedores",
			fg="white",font=("courier",18,"bold italic"),
			command=lambda:self.aparecerMenuContenedores())
		self.btn_conte.grid(row=0,sticky="nsew",pady=5)

		self.btn_clientes=Button(self.frameMenu,bg="#6E5F0E",text="Clientes",
			fg="white",font=("courier",18,"bold italic"),
			command=lambda:self.aparecerMenuClientes())
		self.btn_clientes.grid(row=1,sticky="nsew",pady=5)
		
		self.btn_pedidos=Button(self.frameMenu,bg="#6E5F0E",text="Ver \n Pedidos",
			fg="white",font=("courier",18,"bold italic")
			,command=lambda:self.aparecerMenuPedidos())
		self.btn_pedidos.grid(row=2,sticky="nsew",pady=5)

		return self.frameMenu

	def neutralizarMenus(self):
		self.frameMenu.grid_forget()
		self.menuClientes.grid_forget()
		self.menuPedidos.grid_forget()
		self.menuContenedor.grid_forget()

	def neutralizarTerreno(self):
		self.frameContenedores.grid_forget()
		self.frameClientes.grid_forget()
		self.framePedidos.grid_forget()	
		
	def aparecerMenuClientes(self):
		self.neutralizarMenus()
		self.neutralizarTerreno()
		self.frameClientes.grid(row=0,column=1,sticky="nsew")
		self.menuClientes.grid(row=0,column=0)


	def aparecerMenuContenedores(self):
		self.neutralizarMenus()
		self.neutralizarTerreno()
		self.menuContenedor.grid(row=0,column=0)
		self.frameContenedores.grid(row=0,column=1)


	def aparecerMenuPedidos(self):
		self.neutralizarMenus()
		self.neutralizarTerreno()
		self.menuPedidos.grid(row=0,column=0)
		self.framePedidos.grid(row=0,column=1,sticky="nsew")	


	



