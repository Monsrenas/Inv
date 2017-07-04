
from tkinter import  *
from tkinter.ttk import *
from misclases import  *
import _mysql

root = Tk()


def hello():
	seccion.nueva("Entrada de Insumos",0,0)
	wx = Entry(seccion.vtn)
	wx.pack()
	wxy = Entry(seccion.vtn)
	wxy.pack()

def factura():
	seccion.nueva("Facturacion",1,0)


def cierra():
	seccion.cerrar()


seccion=ventana(root)

menubar = Menu(root)
codigos=editcodigo(seccion)

inventario=movInventario(seccion)



# create a pulldown menu, and add it to the menu bar
facturamenu = Menu(menubar, tearoff=0)

facturamenu.add_command(label="Factura", command=factura)
facturamenu.add_command(label="Devolución", command=cierra)
facturamenu.add_separator()
facturamenu.add_command(label="Cobro de Credito", command=root.quit)
menubar.add_cascade(label="Facturación", menu=facturamenu)

invetariomenu = Menu(menubar, tearoff=0)
invetariomenu.add_command(label="Entrada", command=inventario.edita)
invetariomenu.add_command(label="Salida", command=inventario.edita)
invetariomenu.add_separator()
invetariomenu.add_command(label="Registrar Producto", command=codigos.codProductos)
invetariomenu.add_separator()
invetariomenu.add_command(label="Pago de Debito", command=root.quit)
menubar.add_cascade(label="Inventario", menu=invetariomenu)

# create more pulldown menus
produccionmenu = Menu(menubar, tearoff=0)
produccionmenu.add_command(label="Abrir Orden", command=hello)
produccionmenu.add_command(label="Cerrar Orden", command=hello)
menubar.add_cascade(label="Producción", menu=produccionmenu)

distribucionmenu = Menu(menubar, tearoff=0)
distribucionmenu.add_command(label="Despacho", command=hello)
distribucionmenu.add_command(label="Ejecuciòn", command=hello)
menubar.add_cascade(label="Distribuciòn", menu=distribucionmenu)

gastosmenu = Menu(menubar, tearoff=0)
gastosmenu.add_command(label="Generar Partida Mensual", command=hello)
gastosmenu.add_separator()
gastosmenu.add_command(label="Editar Elementos de Gasto", command=hello)
gastosmenu.add_command(label="Editar Factores", command=hello)
menubar.add_cascade(label="Gastos", menu=gastosmenu)

informesmenu = Menu(menubar, tearoff=0)
informesmenu.add_command(label="Costo de Producciòn", command=hello)
informesmenu.add_command(label="Gasto de Administraciòn", command=hello)
informesmenu.add_command(label="Utilidad", command=hello)
informesmenu.add_command(label="Cantidad de Materia Prima", command=hello)
menubar.add_cascade(label="Informes", menu=informesmenu)

nomencladormenu = Menu(menubar, tearoff=0)
nomencladormenu.add_command(label="Clientes", command=hello)
nomencladormenu.add_command(label="Trabajadores", command=hello)
nomencladormenu.add_command(label="Unidades de Medida	", command=hello)
nomencladormenu.add_command(label="Tipos de Gasto", command=hello)
menubar.add_cascade(label="≡", menu=nomencladormenu )


# display the menu

root.title("Sistema de Inventario")	
root.config(menu=menubar)
root.geometry("800x650")
root.mainloop() 

