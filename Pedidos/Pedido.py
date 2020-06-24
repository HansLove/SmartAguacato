from tkinter import *
from datetime import datetime
import requests
from GUI.classScrollFrame import ScrollableFrame

class Pedido():
	def __init__(self,frame,menuPrincipal):
		self.frame=Frame(frame)
		self.frameMenu=Frame(frame,height=100)

		self.menuPrincipal=menuPrincipal
		self.frameCrearPedido=Frame(frame)
		self.amount=IntVar()
		self.precioUnidad=IntVar()
		self.nombre="Null"
		self.clienteID=""

	def frameMainPedidos(self):
		lista=self.obtenerPedidos()
		self.frameScroll=ScrollableFrame(self.frame)
		self.frameScroll.grid(column=1,row=0,sticky="nsew")

		i=1
		for item in lista:
			self.crearFilaPedido(item,self.frameScroll.scrollable_frame,i)
			i=i+1
			
		return self.frame
	
	def crearFilaPedido(self,item,frameScroll,numPedido):
		frameRow=Frame(frameScroll,bd=3,relief=SUNKEN)
		frameRow.config(bg="#0B3C0F")
		frameRow.grid( padx=5,pady=5,sticky="nsew")

		lbl_cliente=Label(frameRow,text=item['nombre'],
			font=("Serif",22,"bold italic"),bg="#0B3C0F",fg="white")
		lbl_cliente.grid(row=0,column=0,sticky="nsew",padx=3,pady=3)

		texto_cantidad=str(item['cantidad'])+" Kg's"
		lbl_cantidad=Label(frameRow,text=texto_cantidad,
			font=("Serif",22,"bold italic"),bg="#0B3C0F",fg="white")
		lbl_cantidad.grid(row=0,column=1,padx=3,pady=3)

		num_pedido=Label(frameRow,text="  "+str(numPedido),
			font=("Serif",22,"bold italic"),bg="#0B3C0F",fg="white")
		num_pedido.grid(row=0,column=2,sticky="nsew",padx=3,pady=3)

		texto="Precio por unidad: "+str(item['precioUnidad'])
		lbl_precioU=Label(frameRow,font=("Serif",20),
			text=texto,bg="#0B3C0F",fg="white")
		lbl_precioU.grid(row=1,column=0,columnspan=2,padx=3,pady=3)

		btn_eliminar=Button(frameRow,text="X",font=("serif",15,"bold italic"),
			bg="red",fg="white",command=lambda:self.borrarPedido(item))
		btn_eliminar.grid(row=2,column=2,sticky="se")
		try:
			lbl_fecha=Label(frameRow,text=item['date'][:19],
				font=("Serif",18,"bold italic"),bg="#0B3C0F",fg="white")
			lbl_fecha.grid(row=2,columnspan=1,sticky="nswe",padx=3,pady=3)
		except:
			print("Este pedido no contiene fecha")
		


	def menuPedidos(self):
		btn_nuevo_pedido=Button(self.frameMenu,bg="#6E5F0E",text="Nuevo \n pedido",
			fg="white",font=("courier",18,"bold italic"),
			command=lambda:self.aparecer())
		btn_nuevo_pedido.pack(side="top",fill="both")

		btn_atras=Button(self.frameMenu,bg="#6E5F0E",text="Atras",
			fg="white",font=("courier",18,"bold italic"),
			command=lambda:self.atras())
		btn_atras.pack(side="top",fill="both")	
		return self.frameMenu

	

	def generarNuevoPedido(self):
		lbl_cuanto_necesita=Label(self.frameCrearPedido,
			text="Cuantos Kg necesitas?",
			font=("Courier",20,"bold italic"))
		lbl_cuanto_necesita.grid(row=0,column=0,padx=6,pady=6,sticky="nswe")

		entry_amount=Entry(self.frameCrearPedido,textvariable=self.amount)
		entry_amount.grid(row=1,padx=6,pady=6,sticky="nswe")

		lbl_precio_unidad=Label(self.frameCrearPedido,
			text="Precio por Kg",
			font=("Courier",20,"bold italic"))
		lbl_precio_unidad.grid(row=2,column=0,padx=6,pady=6,sticky="nswe")

		entry_precio_unidad=Entry(self.frameCrearPedido,
			textvariable=self.precioUnidad)
		entry_precio_unidad.grid(row=3,sticky="nswe")

		btn_enviar_pedido=Button(self.frameCrearPedido,
			text="Crear pedido",
			font=("Courier",18,"bold italic"),
			fg="blue",bg="black",
			command=lambda:self.enviarPedido())
		btn_enviar_pedido.grid(row=4,padx=10,pady=10)


		return self.frameCrearPedido

	def enviarPedido(self):
		print("Nombre recibido al enviar el pedido: ",self.nombre)
		API_ENDPOINT = "http://localhost:5000/pedido"

		now = datetime.now()

		data = {
		'nombre':self.nombre,
		'clienteID':self.clienteID,
		'cantidad':self.amount.get(),
		'precioUnidad':self.precioUnidad.get(),
		'unidad':'Kg',
		'date':str(now.strftime("%d/%m/%Y %H:%M:%S"))

		} 
		r = requests.post(url = API_ENDPOINT, data = data) 
		
		
		if r.json()['status']:
			self.frameCrearPedido.grid_forget()
			self.frame.grid(row=0,column=1)
		else:
			print("Algo fallo al hacer un pedido")	

	def borrarPedido(self,item):
		API_ENDPOINT = "http://localhost:5000/pedido/"+str(item['_id'])
		r = requests.delete(url = API_ENDPOINT) 
		print(r.json())
		if r.json()['status']:
			print("Pedido eliminado con exito")	

	def obtenerPedidos(self):
		API_ENDPOINT = "http://localhost:5000/pedido"
		r = requests.get(url = API_ENDPOINT) 
		data = r.json()
		#print(r.json()['result']) 
		return	r.json()['result']
		
	def obtenerUltimoPedido(self,item):
		API_ENDPOINT = "http://localhost:5000/pedido/"+str(item['_id'])
		r = requests.get(url = API_ENDPOINT) 
		listaPedidos= r.json()['result']

		if len(listaPedidos)>0:
			
			fechaMayor=datetime.strptime('18/06/2018 14:51:08', "%d/%m/%Y %H:%M:%S")
			for pedido in listaPedidos:
				fechaEntrada=datetime.strptime(pedido['date'], "%d/%m/%Y %H:%M:%S")
				if fechaEntrada>fechaMayor:
					fechaMayor=fechaEntrada
					
			print("Fecha mayor: ",fechaMayor)
			return fechaMayor
		else:
			return 0
		

	def atras(self):
		self.menuPrincipal.grid(row=0,column=0)
		self.frameMenu.grid_forget()		