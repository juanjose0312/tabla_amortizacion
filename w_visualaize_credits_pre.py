import sqlite3 as sql
from tkinter import *
from tkinter import ttk
from w_visualaize_credit import W_visualaize_credit

from ventanas import Window

#		- modulo de "ver créditos"
#			- mostrar tablas de amortización
#			- cuenta regresiva en días para pagar
#			- opción de pago
#				- mensaje de rectificación y pagar

class W_visualaize_credits_pre(Window):\

    def __init__(self, window, title, geometry, user):
        super().__init__(window, title, geometry)
        
        self.user = user
        print(self.user)

        def seach_user():
            conn = sql.connect('prestamo.db')   
            cursor = conn.cursor()
            instruccion = f"SELECT * FROM credit_specifications WHERE user='{self.user}'"
            cursor.execute(instruccion)
            datos = cursor.fetchall()
            conn.commit()
            conn.close()

            return datos

        tabla = seach_user()

        self.tree = ttk.Treeview(window ,height=12, columns=[f"#{n}" for n in range(1, 7)])
        self.tree.grid(row= 1, column= 0)

        self.tree.heading('#0', text='#     ')          
        self.tree.column('#0', width=50)
        self.tree.heading('#1', text='carrera     ')          
        self.tree.column('#1', width=120)
        self.tree.heading('#2', text='periodo     ')
        self.tree.column('#2', width=100)
        self.tree.heading('#3', text='valor financiado')
        self.tree.column('#3', width=120)
        self.tree.heading('#4', text='# cuotas    ')
        self.tree.column('#4', width=80)
        self.tree.heading('#5', text='tasa mensual')
        self.tree.column('#5', width=80)
        self.tree.heading('#6', text='tasa mora   ')
        self.tree.column('#6', width=80)

        for i in range(len(tabla)-1,-1,-1):
                self.tree.insert("", 0, text=i+1, values=(tabla[i][1],tabla[i][2],tabla[i][3],tabla[i][4],tabla[i][5],tabla[i][6]))
        
        frame = LabelFrame(self.wind, text='seleciona')
        frame.grid(row=2, column=0)

        self.credit=StringVar(frame)
        self.credit.set(1)
        options=[]
        for i in range(len(tabla)):
            options.append(i+1)
        options=OptionMenu(frame,self.credit,*options).grid(row=1, column=0)

        

        def visualaize_credit():

            credit=tabla[int(self.credit.get())-1]

            w_visualaize_credit = Tk()
            W_visualaize_credit(w_visualaize_credit,"visualizar credito","1000x330", credit)


        Button(frame, text= ' inspeccionar ', command=visualaize_credit).grid(row=1, column=1)