import sqlite3
from datetime import datetime, timedelta
from functools import partial
from tkinter import *
from tkinter import messagebox, ttk

from tabla import tabla_amortizacion
from ventanas import Window

class W_simulator_credit(Window):
    def __init__(self, window, title, geometry, user):
        super().__init__(window, title, geometry)

        self.user=user

        # frame modificacion de credito
        frame_mod = LabelFrame(self.wind, text='crea tu credito')
        frame_mod.grid(row=0, column=0)

        # input de carrera
        Label(frame_mod, text= 'periodo de inicio : ').grid(row=0, column=0)
        self.carrera=StringVar(frame_mod)
        self.carrera.set('ing.software')
        options_0=['ing.industrial','ing.software','adm.empresas','contaduria','seg y salud']
        option_0=OptionMenu(frame_mod,self.carrera,*options_0).grid(row=1, column=0)

        # input de valor a financiar  
        Label(frame_mod, text= 'valor a financiar : ').grid(row=0, column=1)
        self.valor_inicial = Entry(frame_mod)
        self.valor_inicial.grid(row=1, column=1)

        # input de periodo de inicio
        Label(frame_mod, text= 'periodo de inicio : ').grid(row=2, column=0)
        self.opcion_fecha=StringVar(frame_mod)
        self.opcion_fecha.set('periodo 1')
        options_1=['periodo 1','periodo 2']
        option_1=OptionMenu(frame_mod,self.opcion_fecha,*options_1).grid(row=3, column=0)

        
        # input de cuotas del credito
        Label(frame_mod, text= 'cuotas del credito: ').grid(row=2, column=1)
        self.numero_cuotas=StringVar(frame_mod)
        self.numero_cuotas.set(6)
        options_2=[1,2,3,4,5,6]
        option_2=OptionMenu(frame_mod,self.numero_cuotas,*options_2).grid(row=3, column=1)
            

        def frame_info():

            if validation_numbers():
                return

            # frame de informacion
            frame = LabelFrame(self.wind, text='visualizar pre credito')
            frame.grid(row=1, column=0)

            # nombre
            Label(frame, text= 'usuario : ').grid(row=2, column=0)
            Label(frame, text= self.user ).grid(row=2, column=1)

            # formula de fecha

            dias_ciclo_mes=[29,58,88,119,149,180,210,241,272,302,333,363]
            fecha_inicial= datetime.strptime("2022-01-01",'%Y-%m-%d')

            if self.opcion_fecha.get() == 'periodo 1':
                fecha_de_inicio = fecha_inicial
                fecha_de_fin    =(fecha_inicial + timedelta(dias_ciclo_mes[int(self.numero_cuotas.get())-1]))
            else:
                fecha_de_inicio =(fecha_inicial + timedelta(dias_ciclo_mes[5]))
                fecha_de_fin    =(fecha_inicial + timedelta(dias_ciclo_mes[5+int(self.numero_cuotas.get())]))

            # fecha de inicio
            Label(frame, text= 'fecha de inicio : ').grid(row=3, column=0)
            Label(frame, text= fecha_de_inicio).grid(row=3, column=1)

            # fecha de fin
            Label(frame, text= 'fecha de fin : ').grid(row=4, column=0)
            Label(frame, text= fecha_de_fin).grid(row=4, column=1)
            
            # valor de prestamo
            valor_inicial=int(self.valor_inicial.get())

            Label(frame, text= 'valor de prestamo : ').grid(row=5, column=0)
            Label(frame, text= valor_inicial).grid(row=5, column=1)

            # numero de cuotas

            numero_cuotas = int(self.numero_cuotas.get())

            Label(frame, text= 'numero de cuotas : ').grid(row=6, column=0)
            Label(frame, text= numero_cuotas).grid(row=6, column=1)

            # cuota por mes
            cuota_por_mes = valor_inicial/((1-(1+0.02)**((numero_cuotas)*-1))/0.02)
            cuota_por_mes = round(cuota_por_mes,2)

            Label(frame, text= 'cuota por mes : ').grid(row=7, column=0)
            Label(frame, text= cuota_por_mes).grid(row=7, column=1)

            # tasa mensual
            tasa_mensual=0.02

            Label(frame, text= 'tasa mensual : ').grid(row=9, column=0)
            Label(frame, text= ('%',tasa_mensual*100)).grid(row=9, column=1)

            # tasa anual
            tasa_anual= ((tasa_mensual+1)**12)-1
            tasa_anual= round(tasa_anual,2)

            Label(frame, text= 'tasa anual : ').grid(row=8, column=0)
            Label(frame, text= ('%',tasa_anual*100)).grid(row=8, column=1)

            # tasa de mora
            tasa_mora=0.03

            Label(frame, text= 'tasa de mora : ').grid(row=11, column=0)
            Label(frame, text= ('%',tasa_mora*100)).grid(row=11, column=1)

            # tabla de amortizacion
            self.tree = ttk.Treeview(
                window ,height=12, columns=[f"#{n}" for n in range(1, 6)]
            )
            self.tree.grid(row= 1, column= 1)

            self.tree.heading('#0', text='N cuota      ')          
            self.tree.column('#0', width=60)
            self.tree.heading('#1', text='Fecha de pago')
            self.tree.column('#1', width=100)
            self.tree.heading('#2', text='Cuota normal ')
            self.tree.column('#2', width=120)
            self.tree.heading('#3', text='Abono a capital  ')
            self.tree.column('#3', width=120)
            self.tree.heading('#4', text='Abono a intereses')
            self.tree.column('#4', width=120)
            self.tree.heading('#5', text='saldo        ')
            self.tree.column('#5', width=120)

            tabla=tabla_amortizacion(
                self.opcion_fecha.get(),
                valor_inicial,
                numero_cuotas,
                tasa_mensual,
                tasa_mora
            )

            for i in range(numero_cuotas-1,-1,-1):
                self.tree.insert("", 0, text=tabla[0][i], values=(tabla[1][i],tabla[4][i],tabla[5][i],tabla[6][i],tabla[8][i]))

            # boton que envia la informacion a la base de datos
            Button(window, text= ' hacer credito ',command=partial(insert_row,valor_inicial,numero_cuotas,tasa_mensual,tasa_mora)).grid(row=3, column=0)
            
            
        def validation_numbers():
            
            # valida que los espacion de valor sean numero 
            # caso contrario mando una alerta con el problema
            
            if self.valor_inicial.get().isdigit():
                return False
            
            messagebox.showinfo(message='el valor no es un numero',title='error')
            return True


        def insert_row(valor_inicial,numero_cuotas,tasa_mensual,tasa_mora):
            

            continuar=messagebox.askyesno(message="¿Desea continuar?", title="Título")
            
            if continuar:
                # se encarca de subir los datos

                conn = sqlite3.connect('prestamo.db')
                cursor = conn.cursor()
                cursor.execute(f"INSERT INTO credit_specifications VALUES ('{self.user}','{self.carrera.get()}','{self.opcion_fecha.get()}',{valor_inicial},{numero_cuotas},{tasa_mensual},{tasa_mora});")
                conn.commit()
                conn.close()
                messagebox.showinfo(message='el credito a sido exitoso',title='info')

        # boton para ganerar la tabla de amortizacion
        Button(self.wind, text="simular", command=frame_info).grid(row=0, column=1)

        # boton para devolverse
        Button(self.wind, text="volver", command=window.destroy ).grid(row=2, column=1)