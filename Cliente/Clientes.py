from tkinter import *
import requests
from GUI.classScrollFrame import ScrollableFrame
from datetime import datetime,timedelta



class Cliente():
	def __init__(self,frame,menuPrincipal,pedidos):
		
		self.framePrimario=Frame(frame)
		self.framePrimario.config(bg="orange")
		self.frameNuevoCliente=Frame(frame)
		self.menuPrincipal=menuPrincipal
		self.frameMenu=Frame(frame)
		self.nombre=StringVar()
		self.latitud=DoubleVar()
		self.longitud=DoubleVar()
		self.nuevoCliente=self.esqueletoNuevoCliente()
		self.pedidos=pedidos


	def esqueletoNuevoCliente(self):
		
		lbl_nombre=Label(self.frameNuevoCliente,text="Nombre del cliente",font=("Courier",22))
		lbl_nombre.grid(column=0,row=0)

		enty_nombre=Entry(self.frameNuevoCliente,textvariable=self.nombre,font=("Serif",20,"bold italic"))
		enty_nombre.grid(column=0,row=1)

		lbl_latitud=Label(self.frameNuevoCliente,text="Latitud",font=("Courier",22))
		lbl_latitud.grid(column=0,row=2,pady=15)

		entry_latitud=Entry(self.frameNuevoCliente,textvariable=self.latitud,font=("Serif",20,"bold italic"))
		entry_latitud.grid(column=0,row=3)

		lbl_longitud=Label(self.frameNuevoCliente,text="Longitud",font=("Courier",22))
		lbl_longitud.grid(column=0,row=4)

		entry_longitud=Entry(self.frameNuevoCliente,textvariable=self.longitud,font=("Serif",20,"bold italic"))
		entry_longitud.grid(column=0,row=5)

		btn_listo=Button(self.frameNuevoCliente,text="Subir",bg="#30671B",fg="white",
			command=lambda:self.subirCliente())
		btn_listo.grid(column=0,row=6,padx=5,pady=5)

		return self.frameNuevoCliente

	def crearFrameClientes(self):
		self.frameScroll=ScrollableFrame(self.framePrimario)
		
		self.frameScroll.grid(column=1,row=0,sticky="nsew")
		lista=self.obtenerListaClientes()

		frameTitulos=Frame(self.frameScroll.scrollable_frame)
		lbl_nombre_cliente=Label(frameTitulos,text="Nombre",bd=3,relief=SUNKEN)
		lbl_nombre_cliente.grid(column=0,row=0,sticky="nsew")

		promedio_consumo_tit=Label(frameTitulos,text="Promedio de consumo\ndiario",
			bd=3,relief=SUNKEN)
		promedio_consumo_tit.grid(column=1,row=0,sticky="nsew")

		necesita_aguacate=Label(frameTitulos,text="Necesita \naguacate?",
			bd=3,relief=SUNKEN)
		necesita_aguacate.grid(column=2,row=0,sticky="nsew")
		frameTitulos.pack()
		for item in lista:
			self.crearFila(item,self.frameScroll.scrollable_frame)
			

		return self.framePrimario	
	

	def crearFila(self,item,scrollFrame):
		frameFila=Frame(scrollFrame,bd=3,relief=SUNKEN)
		frameFila.config(bg="#0D1070")
		#frameFila.pack()
		frameFila.pack(fill = X,padx=5,pady=5)#, expand = True)

		btn_name=Button(frameFila,text=item['nombre'],
			command=lambda:self.hacerPedido(item))
		btn_name.config(font=("Courier",24,"bold italic"),bd=3,relief=SUNKEN,
			bg="#A06E2E",fg="white")
		btn_name.grid(row=0,pady=5,padx=5,sticky="nsew")

		consumo_promedio=str(self.obtenerConsumoCliente(item))

		lbl_promedio_consumo=Label(frameFila,text=consumo_promedio[:2]+" Kg's")
		lbl_promedio_consumo.config(font=("Courier",22,"bold italic"),bd=3,relief=SUNKEN,
			bg="#A06E2E",fg="white")
		lbl_promedio_consumo.grid(row=0,column=1,pady=5,padx=5,sticky="nsew")

		ultimoPedido=self.pedidos.obtenerUltimoPedido(item)
		if(ultimoPedido!=0):
			
			now = datetime.now()
			limit=ultimoPedido+timedelta(days=1)
			diferencia=limit-now
			segundos=diferencia.seconds
			resPorcentual=(segundos*100)/86400
			resultadoFinal=100-resPorcentual
			#Pinta el fondo de la probabilidad (Verde,amarillo,rojo)
			lbl_probabilidad_venta=self.colorProbabilidad(frameFila,resultadoFinal)
			lbl_probabilidad_venta.grid(row=0,column=2,pady=5,padx=5,sticky="nsew")


	

	def colorProbabilidad(self,frameFila,resultadoFinal):
			lbl_probabilidad_venta=Label(frameFila)
			if(resultadoFinal>70):
				lbl_probabilidad_venta.config(text=str(resultadoFinal)[:4]+" %")
				lbl_probabilidad_venta.config(font=("Courier",24,"bold italic"),bd=3,relief=SUNKEN,
					bg="#1C710E",fg="white")
			elif(resultadoFinal>30):
				lbl_probabilidad_venta.config(text=str(resultadoFinal)[:4]+" %")
				lbl_probabilidad_venta.config(font=("Courier",24,"bold italic"),bd=3,relief=SUNKEN,
					bg="#AEA919",fg="white")

			else:
				lbl_probabilidad_venta.config(text=str(resultadoFinal)[:4]+" %")
				lbl_probabilidad_venta.config(font=("Courier",24,"bold italic"),bd=3,relief=SUNKEN,
					bg="#CD291E",fg="white")

			return lbl_probabilidad_venta			

	def hacerPedido(self,cliente):
		print("Cliente seleccionado: ",cliente['nombre'])
		self.pedidos.nombre=cliente['nombre']
		self.pedidos.clienteID=cliente['_id']

		frame=self.pedidos.generarNuevoPedido()
		frame.grid(row=0,column=1,sticky="nsew")
		self.framePrimario.grid_forget()




	def crearMenuCliente(self):
		btn_nuevo_cliente=Button(self.frameMenu,bg="#6E5B0E",text="Nuevo \n cliente",
			fg="white",font=("courier",18,"bold italic"),
			command=lambda:self.generarFrameNuevoCliente())
		btn_nuevo_cliente.pack()

		btn_atras=Button(self.frameMenu,bg="#6E5B0E",text="Atras",
			fg="white",font=("courier",18,"bold italic"),
			command=lambda:self.atras())
		btn_atras.pack()	

		return self.frameMenu


	def subirCliente(self):
		API_ENDPOINT = "http://localhost:5000/clientes"
		data = {
		'latitud':self.latitud.get(),
		'longitud':self.longitud.get(), 
		'nombre':self.nombre.get()
	
		} 
		r = requests.post(url = API_ENDPOINT, data = data) 
		#print(r.text)
		#json_data = json.loads(r.text)
		
		documentos=r.json()['documentos']	
		if r.json()['status']:
			self.framePrimario.grid(row=0,column=1)
			self.frameNuevoCliente.grid_forget()

	def obtenerListaClientes(self):
		API_ENDPOINT = "http://localhost:5000/clientes"
		r = requests.get(url = API_ENDPOINT)

		data = r.json() 	
		return data['clientes']

	def atras(self):
		self.frameMenu.grid_forget()
		self.menuPrincipal.grid(row=0,column=0,sticky="ns")		

	def generarFrameNuevoCliente(self):
		self.frameNuevoCliente.grid(row=0,column=1)
		self.framePrimario.grid_forget()
	
	def obtenerConsumoCliente(self,item):
		API_ENDPOINT = "http://localhost:5000/pedido/"+str(item['_id'])
		r = requests.get(url = API_ENDPOINT) 
		data = r.json()
		lista=r.json()['result']
		i=0
		sumaTotal=0
		for pedido in lista:
			entrada=pedido['cantidad']
			sumaTotal=sumaTotal+entrada
			i=i+1

		if i==0:
			return 0
		else:
			return	sumaTotal/i



