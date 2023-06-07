from datetime import datetime, timedelta
from tkinter import ttk
from tkinter import *

from tabla import tabla_amortizacion
from ventanas import Window

#		- modulo de "ver créditos"
#			- mostrar tablas de amortización
#			- cuenta regresiva en días para pagar
#			- opción de pago
#				- mensaje de rectificación y pagar

class W_visualaize_credit(Window):\

    def __init__(self, window, title, geometry, table):
        super().__init__(window, title, geometry)
        
        self.user           =table[0]
        self.carrera        =table[1]
        self.opcion_fecha   =table[2]
        self.valor_inicial  =table[3]
        self.numero_cuotas  =table[4]
        self.tasa_mensual   =table[5]
        self.tasa_mora      =table[6]

        # frame de informacion
        frame = LabelFrame(self.wind, text='visualizar credito')
        frame.grid(row=0, column=0) 

        # nombre
        Label(frame, text= 'user : ').grid(row=2, column=0)
        Label(frame, text= self.user ).grid(row=2, column=1)

        # formula de fecha

        dias_ciclo_mes=[29,58,88,119,149,180,210,241,272,302,333,363]
        fecha_inicial= datetime.strptime("2022-01-01",'%Y-%m-%d')


        if self.opcion_fecha == 'periodo 1':
            fecha_de_inicio = fecha_inicial
            fecha_de_fin    =(fecha_inicial + timedelta(dias_ciclo_mes[int(self.numero_cuotas)-1]))
        else:
            fecha_de_inicio =(fecha_inicial + timedelta(dias_ciclo_mes[5]))
            fecha_de_fin    =(fecha_inicial + timedelta(dias_ciclo_mes[5+int(self.numero_cuotas)]))

        # fecha de inicio
        Label(frame, text= 'fecha de inicio : ').grid(row=3, column=0)
        Label(frame, text= fecha_de_inicio).grid(row=3, column=1)

        # fecha de fin
        Label(frame, text= 'fecha de fin : ').grid(row=4, column=0)
        Label(frame, text= fecha_de_fin).grid(row=4, column=1)

        # valor de prestamo
        Label(frame, text= 'valor de prestamo : ').grid(row=5, column=0)
        Label(frame, text= self.valor_inicial).grid(row=5, column=1)

        # numero de cuotas
        Label(frame, text= 'numero de cuotas : ').grid(row=6, column=0)
        Label(frame, text= self.numero_cuotas).grid(row=6, column=1)

        # cuota por mes

        cuota_por_mes = self.valor_inicial/((1-(1+0.02)**((self.numero_cuotas)*-1))/0.02)
        cuota_por_mes = round(cuota_por_mes,2)

        Label(frame, text= 'cuota por mes : ').grid(row=8, column=0)
        Label(frame, text= cuota_por_mes).grid(row=8, column=1)

        # tasa anual 

        tasa_anual= ((self.tasa_mensual+1)**12)-1
        tasa_anual= round(tasa_anual,2)

        Label(frame, text= 'tasa anual : ').grid(row=9, column=0)
        Label(frame, text= ('%',(tasa_anual)*100) ).grid(row=9, column=1)

        # tasa mensual
        Label(frame, text= 'tasa mensual : ').grid(row=10, column=0)
        Label(frame, text=  ('%',(self.tasa_mensual)*100)).grid(row=10, column=1)

        # tasa de mora
        Label(frame, text= 'tasa de mora : ').grid(row=11, column=0)
        Label(frame, text= ('%',(self.tasa_mora)*100)).grid(row=11, column=1)

        # tabla de amortizacion
        self.tree = ttk.Treeview(
            window ,height=12, columns=[f"#{n}" for n in range(1, 10)]
        )
        self.tree.grid(row= 0, column= 1)

        self.tree.heading('#0', text='N cuota')          
        self.tree.column('#0', width=40)
        self.tree.heading('#1', text='Fecha de pago')
        self.tree.column('#1', width=80)
        self.tree.heading('#2', text='Fecha pagada')
        self.tree.column('#2', width=80)
        self.tree.heading('#3', text='Cuota extra ')
        self.tree.column('#3', width=80)
        self.tree.heading('#4', text='Cuota normal  ')
        self.tree.column('#4', width=80)
        self.tree.heading('#5', text='Abono a capital')
        self.tree.column('#5', width=80)
        self.tree.heading('#6', text='Abono a intereses')
        self.tree.column('#6', width=90)
        self.tree.heading('#7', text='intereses de mora')
        self.tree.column('#7', width=80)
        self.tree.heading('#8', text='saldo   ')
        self.tree.column('#8', width=60)
        self.tree.heading('#9', text='pago    ')
        self.tree.column('#9', width=40)

        tabla=tabla_amortizacion(
                table[2],           #opcion_fecha,
                table[3],           #valor_inicial,
                table[4],           #numero_cuotas,
                table[5],           #tasa_mensual,
                table[6]            #tasa_mora
            )

        for i in range(table[4]-1,-1,-1):
            self.tree.insert("", 0, text=tabla[0][i], values=(tabla[1][i],tabla[2][i],tabla[3][i],tabla[4][i],tabla[5][i],tabla[6][i],tabla[7][i],tabla[8][i],tabla[9][i]))

        
        
        # boton pago abono
        Button(window, text= ' pagar abono ').grid(row=1, column=0)
        Button(window, text= ' pagar ').grid(row=2, column=0)