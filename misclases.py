from tkinter import  *
from tkinter.ttk import *
from decimal import *
import time

import _mysql

class listado:

	def __init__ (self, mroot, x, y, ancho):
		self.vtn=mroot
		self.x=x
		self.y=y
		self.ancho=ancho
		#tipoletra=font.Font(size=12, weight="bold")

		self.txt=StringVar()
		self.txt.set("prueba")
		self.campos=Label(self.vtn, textvariable="prueba")
													# font=tipoletra,
		self.campos.pack()
		self.campos.place(x=self.x, y=self.y-10)

		self.list = Listbox(self.vtn, width=self.ancho)
		self.list.pack()
		self.list.place(x=self.x, y=self.y+10)

		self.info = [{}]  # Lista de diccionarios con la informacion a guardar en la base de datos

	def elementos(self):
		return(len(self.info))

	def registros(self):		
		return self.info

	def agregar (self, info, vista):
		self.info.append(info)		  #agrega un diccionario a la lista con los nombres de los campos y los datos correspondientes
		self.list.insert(END, vista)  #agrega elemento visiblen en el LlistBox 	
		print("Agrego")

	def etiqueta (self, texto):
		self.txt.set(texto)

class ventana:

	def __init__ (self, principal):
		self.principal=principal
		self.vtn = LabelFrame(principal)

	def  nueva (self, texto, x, y):
		 self.vtn.destroy() 
		 self.vtn
		 self.vtn = LabelFrame(self.principal,  text=texto, borderwidth=2, relief="raised")
		 self.vtn.pack(fill="both", expand="yes")

	def cerrar(self):
		self.vtn.destroy()
		self.vtn.destroy()
# test stuff

class dbase:

	def __init__ (self, host, usuario, pasww, base ):
			self.host=host
			self.user=usuario
			self.pasw=pasww
			self.base=base

	def existe (self, tabla, ocurrencia):
		
		db = _mysql.connect(self.host, self.user,self.pasw,self.base)
		consulta="SELECT * FROM "+tabla+" WHERE "+ocurrencia
		
		db.query(consulta)
		c=db.use_result()
		fila = c.fetch_row(how=1)
		reco= c.num_rows()
		db.close

		a=(reco!=0)
		return a

	def registros (self, tabla, condicion, campos):
		

		
		db = _mysql.connect(self.host, self.user,self.pasw,self.base)
		#SELECT col_name FROM tbl_name WHERE col_name > 0
		loscampos=""
		if len(campos)==0:
			loscampos="*"
		else:
			for x in range(0,len(campos)):
				loscampos=loscampos+campos[x]
				if x<len(campos)-1:
					loscampos=loscampos+","
		
		consulta="SELECT "+loscampos+" FROM "+tabla+" WHERE "+condicion
		db.query(consulta)
		c=db.use_result()
		fila = c.fetch_row(how=1)
					
		listado=[]	#para almacenar el resultado de la consulta en un diccionario
		while fila:
			registro={} 
			for x in range(0,len(campos)):
					
				#listado[mllave[2:-1]]=mcampo[2:-1]

				registro[campos[x]]=str(fila[0][campos[x]])	#Crea un diccionaro con los registros de esta fila

				cadtmp=registro[campos[x]]

				if cadtmp.find("b'")==0:
					registro[campos[x]]=str(registro[campos[x]])[2:-1]

			listado.append(registro)  #Agrega el diccionario a la lista
			fila = c.fetch_row(how=1) #Avanza a la proxima fila

		db.close
		return listado


	def agregar(self, tabla, lisdicc):
			db = _mysql.connect(self.host, self.user,self.pasw,self.base)

			# Ejemplo: INSERT INTO Customers (CustomerName, ContactName, Address, City, PostalCode, Country) 
			#                         VALUES ('Cardinal', 'Tom B. Erichsen', 'Skagen 21', 'Stavanger', '4006', 'Norway');

			for x in range(0,len(lisdicc)):   #Iterando lista para crear consulta para  alta de elemento inexistente
				consulta="INSERT INTO "+ tabla+ " ("
				campos=lisdicc[x].keys()
				xvalores="VALUES ("
				xcampos=""
				for campo in campos:
					xcampos=xcampos+str(campo)+"," 
					nomcamp=lisdicc[x][campo]
					xvalores=xvalores+"'"+lisdicc[x][campo]+"',"
				consulta=consulta+str(xcampos[0:len(xcampos)-1])+") "+str(xvalores[0:len(xvalores)-1])+")"
				db.query(consulta)
			db.close

	def actualizar(self, tabla, lisdicc, llave):
		
		db = _mysql.connect(self.host, self.user,self.pasw,self.base)
		#ContactName = 'Alfred Schmidt', City= 'Frankfurt'
		#WHERE CustomerID = 1;

		for x in range(0,len(lisdicc)):
			consulta="UPDATE "+tabla+" SET "
			campos=lisdicc[x].keys()
			xclave=""
			xcampos=""
			for campo in campos:
				xcampos=xcampos+str(campo)+"= '"+lisdicc[x][campo]+"',"
			for clave in llave:
				xclave=xclave+str(clave)+"="+lisdicc[x][clave]+" and "
			consulta=consulta+str(xcampos[0:len(xcampos)-1])+" WHERE "+str(xclave[0:len(xclave)-5])
			db.query(consulta)
		db.close


	def valores(self, tabla, campo, llave):   #Genera un diccionario util para ComboBox
		db = _mysql.connect(self.host, self.user,self.pasw,self.base)
		consulta="SELECT "+campo+", "+llave+" FROM "+tabla

		db.query(consulta)
		c=db.use_result() 
		reco= c.num_rows()
		fila = c.fetch_row(how=1)

		
		mcampo=""
		listado={}	#para almacenar el resultado de la consulta
		while fila:
			mcampo=str((fila[0][campo]))
			mllave=str(fila[0][llave])

			listado[mllave[2:-1]]=mcampo[2:-1]
			fila = c.fetch_row(how=1)
		db.close
		return listado

	def dicclist(self, dicc,op): #Genera una lista (array) para uso en ComBox
		if op==0:
			arreglo=dicc.keys()
		else:
			arreglo=dicc.values()		

		elemens=[]
		for vms in arreglo:
  			elemens.append(vms)
		return elemens


class editcodigo:  #clase para la adicion y edicion de codigos de Productos
	def __init__(self,  seccion):
		self.scc=seccion	
		self.mtext=StringVar()
		self.txtdesc=StringVar()
		self.txtum=StringVar()
		self.txtelm=StringVar()
		self.txtval=StringVar()
		self.txtprec1=StringVar()
		self.txtprec2=StringVar()
		self.txtprec3=StringVar()
		self.tipol=["Insumo","Producto"]

		self.bd=dbase("127.0.0.1","root","ferrer","papas")
		self.vum=self.bd.valores("_umedida","codigo","descripcion") #Diccionario con la informacion del ComboBox
		self.uml=self.bd.dicclist(self.vum,0) #Lista de opciones que apareceran en el ComboBox
	
	def Limpiar(self):
		self.mtext.set("")
		self.txtdesc.set("")
		self.txtelm.set("")
		self.txtval.set("")
		self.txtprec1.set("")
		self.txtprec2.set("")
		self.txtprec3.set("")
		self.um.current(0)
				
		self.cod.focus_set()	

	def procesaForma(self, mlista):
		cadena=mlista[0]["valor"]
		if cadena=="":
			cadena="0"
		mlista[0]["valor"]=cadena.replace(",", ".")
		mlista[0]["codigo"]=mlista[0]["codigo"][0:13]
		cadena=mlista[0]["codigo"]
		mlista[0]["codigo"]=cadena.strip()
		tmpcad="codigo='"+mlista[0]["codigo"]+"'"

		if len(mlista[0]["codigo"])!=0 and len(mlista[0]["elementos"])!=0 and float(mlista[0]["valor"])>0 :
			tmpcad="codigo='"+mlista[0]["codigo"]+"'"
			if self.bd.existe("inventario",tmpcad):
				self.bd.actualizar("inventario", mlista, ["codigo"])
			else:	
				self.bd.agregar("inventario", mlista)
			self.Limpiar()	

			
	def existeCodigo(self):

		if len(self.cod.get())==0:
			self.cod.focus_set()
		else:
			self.mtext.set(str(self.cod.get()[0:13]))

			mlista=self.bd.registros ("inventario", "codigo='"+self.cod.get()+"'", ["codigo","descripcion","umedida","elementos","cantidad","enalmacen","valor","precio1","precio2","precio3","importe","insumo"])
			self.desc.focus_set()
			if len(mlista)!=0:
				tmpdic=self.bd.dicclist(self.vum,1)

				self.txtdesc.set(mlista[0]["descripcion"])
				self.txtelm.set(mlista[0]["elementos"])
				self.txtval.set(mlista[0]["valor"])
				self.txtprec1.set(mlista[0]["precio1"])
				self.txtprec2.set(mlista[0]["precio2"])
				self.txtprec3.set(mlista[0]["precio3"])
				self.um.current(tmpdic.index(mlista[0]["umedida"]))
				self.tipo.current(mlista[0]["insumo"])
				

	def codProductos(self):
		
		self.scc.nueva("Registro de código de producto",0,0)

		etqcod=Label(self.scc.vtn, text="Código")
		etqcod.pack()
		etqcod.place(x=20, y=20)
		self.cod = Entry(self.scc.vtn, textvariable=self.mtext)  
		self.cod.bind("<FocusOut>", lambda verifica:	self.existeCodigo())
		self.cod.bind("<Return>", lambda verifica: self.existeCodigo())		
		self.cod.pack()
		self.cod.place(x=80, y=20)
		
		etqdesc=Label(self.scc.vtn, text="Descripción")
		etqdesc.pack()
		etqdesc.place(x=230, y=20)
		self.desc = Entry(self.scc.vtn, width=70, textvariable=self.txtdesc)
		self.desc.pack()
		self.desc.place(x=310, y=20)

		etqum=Label(self.scc.vtn, text="Unidad de medida")
		etqum.pack()
		etqum.place(x=20, y=50)
		self.um = Combobox(self.scc.vtn, values=self.uml, state="readonly")
		self.um.set(self.uml[0])
		self.um.configure(width=8)
		self.um.pack()
		self.um.place(x=130, y=50)

		etqelm=Label(self.scc.vtn, text="Elementos")
		etqelm.pack()
		etqelm.place(x=230, y=50)
		self.elm = Entry(self.scc.vtn, width=8, textvariable=self.txtelm)
		self.elm.pack()
		self.elm.place(x=295, y=50)

		etqtipo=Label(self.scc.vtn, text="Tipo")
		etqtipo.pack()
		etqtipo.place(x=370, y=50)
		self.tipo = Combobox(self.scc.vtn, values=self.tipol, state="readonly")
		self.tipo.set(self.tipol[0])
		self.tipo.configure(width=8)
		self.tipo.pack()
		self.tipo.place(x=420, y=50)

		etqval=Label(self.scc.vtn, text="Costo")
		etqval.pack()
		etqval.place(x=570, y=50)
		self.val = Entry(self.scc.vtn, textvariable=self.txtval)
		self.val.pack()
		self.val.place(x=610, y=50)

		etqprec1=Label(self.scc.vtn, text="Precio 1")
		etqprec1.pack()
		etqprec1.place(x=20, y=80)
		self.prec1 = Entry(self.scc.vtn, textvariable=self.txtprec1)
		self.prec1.pack()
		self.prec1.place(x=80, y=80)

		etqprec2=Label(self.scc.vtn, text="Precio 2")
		etqprec2.pack()
		etqprec2.place(x=295, y=80)
		self.prec2 = Entry(self.scc.vtn, textvariable=self.txtprec2)
		self.prec2.pack()
		self.prec2.place(x=355, y=80)

		etqprec3=Label(self.scc.vtn, text="Precio 3")
		etqprec3.pack()
		etqprec3.place(x=570, y=80)
		self.prec3 = Entry(self.scc.vtn, textvariable=self.txtprec3)
		self.prec3.pack()
		self.prec3.place(x=630, y=80)
		
		btnGuarda = Button(self.scc.vtn, text="Guardar", command=lambda:self.procesaForma(mlista =[{"codigo":self.cod.get(), "descripcion":self.desc.get(), "umedida":self.vum[self.um.get()],"elementos":self.elm.get(), "cantidad":"0", "enalmacen":"0", "valor":self.val.get(), "precio1":self.prec1.get(), "precio2":self.prec2.get(), "precio3":self.prec3.get(), "importe":"0", "insumo":str(self.tipo.current())}]))
		btnGuarda.pack()
		btnGuarda.place(x=370, y=160)

		btnNuevo = Button(self.scc.vtn, text="Limpiar", command=lambda:self.Limpiar())
		btnNuevo.pack()
		btnNuevo.place(x=220, y=160)

		self.Limpiar()
		self.cod.focus_set()

class movInventario:

	def __init__(self, seccion):
		self.scc=seccion

		self.txtprovee=StringVar()
		self.txtfactu=StringVar()
		self.txtcomercial=StringVar()
		self.txtcomercial.set("Cooperativa ambateña de papas")
		self.txttlfono=StringVar()
		self.txttlfono.set("0685342547")
		self.txtconsecu=StringVar()
		self.txtconsecu.set("00000000000")
		self.txtfecha=StringVar()
		self.txtfecha.set(time.strftime("%d/%m/%y"))
		self.txtcodigo=StringVar()
		self.txtdesc=StringVar()
		self.txtval=StringVar()
		self.txtcant=StringVar()
		self.txtimporte=StringVar()
		self.txtfpago=StringVar()
		self.txtdocpago=StringVar()
		self.txtfechpago=StringVar()
		self.txtfechpago.set(time.strftime("%d/%m/%y"))
		self.txtum=StringVar()
		self.it=0

		self.bd=dbase("127.0.0.1","root","ferrer","papas")
		self.vfpago=self.bd.valores("_formapago","codigo","descripcion") #Diccionario con la informacion del ComboBox
		self.fpagol=self.bd.dicclist(self.vfpago,0) #Lista de opciones que apareceran en el ComboBox

	def Limpiar(self, nivel):

		if nivel==0:
			self.txtprovee.set("")
			self.txtfactu.set("")
			self.txtcomercial.set("")
			self.txttlfono.set("")
			self.txtconsecu.set("")
			self.txtfecha.set("")
			self.txtimporte.set("0.00")
			self.txtfpago.set("")
			self.txtdocpago.set("")
			self.txtfechpago.set("")
			self.txtum.set("")

		self.txtcodigo.set("")
		self.txtdesc.set("")
		self.txtval.set("")
		self.txtcant.set("")
				
		self.codigo.focus_set()	

	def buscacliente(self):
		self.txtprovee.set(self.cod.get().replace(" ",""))
		if len(self.cod.get())==0:
			self.cod.focus_set()
		else:
			self.txtprovee.set(str(self.cod.get()[0:13]))

			mlista=self.bd.registros ("_clientes", "codigo='"+self.cod.get()+"'", ["codigo","descripcion","celular","telefono"])
			if len(mlista)!=0:
				self.txtcomercial.set(mlista[0]["descripcion"])
				self.txttlfono.set(mlista[0]["telefono"]+"    "+mlista[0]["celular"])

				mlista=self.bd.registros ("_consecutivos", "codigo='RE'", ["codigo","numero"])
				self.txtconsecu.set(str(mlista[0]["numero"]).zfill(13))
				self.cod.config(state='disabled')  
				self.factu.config(state='enabled')
				self.codigo.config(state='enabled')
				self.factu.focus_set()
			else:
				self.cod.focus_set()


	def buscaproducto(self):
		self.txtcodigo.set(self.codigo.get().replace(" ",""))
		print ("La longitud de Codigo es:")
		print (len(self.codigo.get()))
		if len(self.codigo.get())==0:
			#self.codigo.focus_set()
			pass
		else:
			self.txtcodigo.set(str(self.codigo.get()[0:13]))

			mlista=self.bd.registros ("inventario", "codigo='"+self.codigo.get()+"'", ["descripcion","valor","umedida"])
			if len(mlista)!=0:
				self.txtdesc.set(mlista[0]["descripcion"])
				self.txtval.set(mlista[0]["valor"])

				

				mlista=self.bd.registros ("_umedida", "codigo='"+mlista[0]["umedida"]+"'", ["codigo","descripcion"])
				self.txtum.set(str(mlista[0]["descripcion"]))
				self.cant.focus_set()
			else:
				print("PASAAAAA")
				self.codigo.focus_set()

	def modimporte(self):
		auxc=str(self.cant.get().replace(" ",""))
		auxn=0
		if len(auxc)>0:
			c=float(str(self.txtval.get()))
			p=float(str(self.cant.get()))
			self.txtimporte.set(str(c*p))
		else:
			self.txtcant.set("0")
			self.txtval.set("0")
		
	def ejecutar(self):
		if self.contenedor.elementos()>0:
			mlist=self.contenedor.registros()

			print(self.vfpago)
			for ele in mlista:

			#	self.um.current(tmpdic.index(mlista[0]["umedida"]))

				mlista[ele]["formapago"]=self.vfpago

			#	self.fpagol=self.bd.dicclist(self.vfpago,0)
			#   elemento = elemento * elemento
    		# print(elemento) # Una simple verificación

			#print(mlist)
					#self.bd.agregar("inventario", mlista)


	def agrega(self, dicc, linea):
		if float(str(self.txtval.get()))>0:
			self.contenedor.agregar(dicc,linea)
			self.Limpiar(1)

	def fecha(self,cadena):
		if len(cadena)>9:
			cadena=cadena[0:9]
		if len(cadena)==2:
			cadena=cadena[0:2]+"/"+cadena[2:9]
			if int(cadena[0:2])>31:
				cadena="31"+"/"+cadena[3:10]
			
		if len(cadena)==5:
			cadena=cadena[0:5]+"/"+cadena[5:9]
			if int(cadena[3:5])>12:
				cadena=cadena[0:3]+"12"+"/"+cadena[6:len(cadena)]
		if len(cadena)>5:
			if cadena[2]!="/" or cadena[5]!="/":
				cadena=""
		return cadena

	def mascara(self):
		self.txtfechpago.set( self.fecha(self.fechpago.get()) )
		self.fechpago.icursor(END)		

	def edita(self):

		self.scc.nueva("Informe de Recepción",0,0)

		self.contenedor=listado( self.scc.vtn, 10, 100, 120)
		self.contenedor.etiqueta("LISTADO de las Pruebas")
		

		etqprovee=Label(self.scc.vtn, text="Proveedor")
		etqprovee.pack()
		etqprovee.place(x=10, y=10)
		self.cod = Entry(self.scc.vtn, textvariable=self.txtprovee)  
		
		self.cod.bind("<Return>", lambda client: self.buscacliente())		
		self.cod.bind("<FocusOut>", lambda verifica: self.buscacliente())
		#self.cod.bind("<FocusOut>", lambda verifica: self.cod.focus_set())

		self.cod.pack()
		self.cod.place(x=70, y=10)

		etqfactu=Label(self.scc.vtn, text="Factura")
		etqfactu.pack()
		etqfactu.place(x=250, y=10)
		self.factu = Entry(self.scc.vtn, textvariable=self.txtfactu)  
		self.factu.pack()
		self.factu.place(x=300, y=10)
		self.factu.bind("<FocusOut>", lambda verifica: self.factu.config(state='disabled'))
		self.factu.bind("<Return>", lambda verifica: self.codigo.focus_set())

		etqconsecu=Label(self.scc.vtn, text="Informe de Recepción:")
		etqconsecu.pack()
		etqconsecu.place(x=480, y=10)
		consecu=Label(self.scc.vtn, textvariable=self.txtconsecu, foreground="red", font=('Ariel', 12))
		consecu.pack()
		consecu.place(x=620, y=7)

		etqcomercial=Label(self.scc.vtn, text="Nombre comercial:")
		etqcomercial.pack()
		etqcomercial.place(x=10, y=40)
		comercial=Label(self.scc.vtn, textvariable=self.txtcomercial, foreground="blue")
		comercial.pack()
		comercial.place(x=130, y=40)

		etqfecha=Label(self.scc.vtn, text="Fecha de emisiòn:")
		etqfecha.pack()
		etqfecha.place(x=480, y=40)
		fecha=Label(self.scc.vtn, textvariable=self.txtfecha)
		fecha.pack()
		fecha.place(x=600, y=40)

		etqtlfono=Label(self.scc.vtn, text="Teléfono:")
		etqtlfono.pack()
		etqtlfono.place(x=10, y=70)
		tlfono=Label(self.scc.vtn, textvariable=self.txttlfono, foreground="blue")
		tlfono.pack()
		tlfono.place(x=70, y=70)

		etqcodigo=Label(self.scc.vtn, text="Código")
		etqcodigo.pack()
		etqcodigo.place(x=10, y=305)
		self.codigo = Entry(self.scc.vtn, textvariable=self.txtcodigo, state='disabled')
		
		self.codigo.pack()
		self.codigo.bind("<Return>", lambda veriprodu: self.cant.focus_set())		
		self.codigo.bind("<FocusOut>", lambda veriprodu:self.buscaproducto())

		self.codigo.place(x=60, y=300)

		etqdesc=Label(self.scc.vtn, text="Descripción:")
		etqdesc.pack()
		etqdesc.place(x=220, y=300)
		desc=Label(self.scc.vtn, textvariable=self.txtdesc, foreground="blue")
		desc.pack()
		desc.place(x=300, y=300)
		self.txtdesc.set(".......................................")

		etqcant=Label(self.scc.vtn, text="Cantidad")
		etqcant.pack()
		etqcant.place(x=10, y=330)
		self.cant = Entry(self.scc.vtn, textvariable=self.txtcant)  
		self.cant.bind("<FocusOut>", lambda verifica: self.modimporte())
		self.cant.bind("<Return>", lambda verifica: self.cant.focus_set())

		self.cant.pack()
		self.cant.place(x=80, y=330)
		self.cant.configure(width=10)

		self.lum = Label(self.scc.vtn, textvariable=self.txtum)
		self.lum.pack()
		self.lum.place(x=200, y=330)
		self.txtum.set("Unidad de medida")

		etqval =Label(self.scc.vtn, text="Precio")
		etqval.pack()
		etqval.place(x=380, y=330)
		self.val = Label(self.scc.vtn, textvariable=self.txtval)
		self.val.pack()
		self.val.place(x=440, y=330)
		self.txtval.set("0.000")

		self.etqimporte =Label(self.scc.vtn, text="Importe")
		self.etqimporte.pack()
		self.etqimporte.place(x=550, y=330)
		self.txtimporte.set("0.000")
		self.importe = Label(self.scc.vtn, textvariable=self.txtimporte)
		self.importe.pack()
		self.importe.place(x=610, y=330)
		self.txtimporte.set("0.000")

		btnAgrega = Button(self.scc.vtn, text="Agregar", command=lambda: self.agrega(dicc={"ndocumento":str(self.txtconsecu.get()), "codigo":self.codigo.get(),"cliente":self.cod.get(),"fecha":self.txtfecha.get(),"cantidad":self.cant.get(),"valor":self.txtval.get(),"tipomov":"CO"}, linea=str("    "+self.codigo.get()).rjust(14, "0")+"    "+str(self.txtdesc.get())[0:100].ljust(100," ")+"    "+self.cant.get()+"    "))
		#, command=lambda:self.procesaForma(mlista =[{"codigo":self.cod.get(), "descripcion":self.desc.get(), "umedida":self.vum[self.um.get()],"elementos":self.elm.get(), "cantidad":"0", "enalmacen":"0", "valor":self.val.get(), "precio1":self.prec1.get(), "precio2":self.prec2.get(), "precio3":self.prec3.get(), "importe":"0", "insumo":str(self.tipo.current())}]
		btnAgrega.pack()
		btnAgrega.place(x=370, y=400)

		etqfpago=Label(self.scc.vtn, text="Forma de pago")
		etqfpago.pack()
		etqfpago.place(x=10, y=460)
		self.fpago = Combobox(self.scc.vtn, values=self.fpagol, state="readonly")
		self.fpago.set(self.fpagol[0])
		self.fpago.configure(width=8)
		self.fpago.pack()
		self.fpago.place(x=100, y=460)

		etqdocpago=Label(self.scc.vtn, text="Documento de pago")
		etqdocpago.pack()
		etqdocpago.place(x=210, y=460)
		self.docpago = Entry(self.scc.vtn, textvariable=self.txtdocpago)  
		#self.docpago.bind("<FocusOut>", lambda verifica: self.modimporte())
		#self.docpago.bind("<Return>", lambda verifica: self.modimporte())
		self.docpago.place(x=330, y=460)

		etqfechpago=Label(self.scc.vtn, text="Fecha límite de pago")
		etqfechpago.pack()
		etqfechpago.place(x=500, y=460)
		self.fechpago = Entry(self.scc.vtn, textvariable=self.txtfechpago)  
		self.fechpago.bind("<Key>", lambda verifica: self.mascara())
		#self.docpago.bind("<Return>", lambda verifica: self.modimporte())
		self.fechpago.place(x=620, y=460)

		btnEjecutar = Button(self.scc.vtn, text="Ejecutar", command= lambda: self.ejecutar())
		btnEjecutar.pack()
		btnEjecutar.place(x=370, y=520)

		btnImprimir = Button(self.scc.vtn, text="Imprimir")
		btnImprimir.pack()
		btnImprimir.place(x=470, y=520)


		self.cod.focus_set()