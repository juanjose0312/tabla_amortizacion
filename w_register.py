from tkinter import *
from tkinter import messagebox
import sqlite3 as sql

from ventanas import Window


class W_register(Window):

	def __init__(self, window, title, geometry):
		super().__init__(window, title, geometry)

		# crear un frame container
		frame = LabelFrame(self.wind, text='registrarse')
		frame.grid(row=0, column=1, columnspan=3, pady= 20, padx= 40) 

		# crear el input de nombre
		Label(frame, text= 'nombre : ').grid(row=1, column=0)
		self.name = Entry(frame)
		self.name.focus()
		self.name.grid(row=1, column=1)

		# texto y input del tipo de identificacion desplegable

		Label(frame, text= 'tipo identificacion : ').grid(row=2, column=0)
		self.id_type=StringVar(frame)
		self.id_type.set('CC')
		options=['TI','CC','TE']
		option=OptionMenu(frame,self.id_type,*options).grid(row=2, column=1)

		# numero y input del de identificacion	

		Label(frame, text= 'identificacion : ').grid(row=3, column=0)
		self.id_number = Entry(frame)
		self.id_number.grid(row=3, column=1)


		# texto y input del edad
		# solo se puedan poner numero
		
		Label(frame, text= 'edad : ').grid(row=4, column=0)
		self.age = Entry(frame)
		self.age.grid(row=4, column=1)

		# texto y input del correo
		# solo se puedan poner tipo correo o compruebe que es un correo 

		Label(frame, text= 'email : ').grid(row=5, column=0)
		self.email = Entry(frame)
		self.email.grid(row=5, column=1)

		# texto y input del usuario 
		# limite de caracteres

		Label(frame, text= 'usuario : ').grid(row=6, column=0)
		self.user = Entry(frame)
		self.user.grid(row=6, column=1)

		# texto y input del clave
		# se ponga en modo clave y se vean solo asteriscos 

		Label(frame, text= 'clave : ').grid(row=7, column=0)
		password = Entry(frame, show="*")
		password.grid(row=7, column=1)

		# texto y input del nombre
		# lo mismo que la otra clave

		Label(frame, text= 'confirmar clave : ').grid(row=8, column=0)
		password2 = Entry(frame, show="*")
		password2.grid(row=8, column=1)


		def validation_password():

			# compara la password con la password2 y si son iguales la agrega al sistema
			# caso contrario manda una alerta con el problema

			if password.get()==password2.get():
				self.password=password
				return True
			else:
				messagebox.showerror(title='error', message='la clave de confirmacion no coincide')
				return False


		def validation_numbers():

			# valida que los espacion de id_number y age sean numero 
			# caso contrario mando una alerta con el problema
			
			if self.id_number.get().isdigit():
				if self.age.get().isdigit():
					return True
			
			messagebox.showerror(title='error',message='la cedula o la edad no es un numero')
			return False


		def seach_user():

			# busca en la base de datos si la variabel 'self.user' ya esta ingresada de ser asi 
			# devuelve un True
			# de lo contrario 
			# devuelve un False y un menseje que notifica el fallo 

			conn = sql.connect('prestamo.db')
			cursor = conn.cursor()
			instruccion = f"SELECT * FROM login WHERE user='{self.user.get()}'"
			cursor.execute(instruccion)
			datos = cursor.fetchall()
			conn.commit()
			conn.close()
			if len(datos)==0:
				return True

			messagebox.showinfo(message='el usuario ya existe',title='error')
			return False
			
		
		def validation():

			# despues de validar passwords y numeros revisa que los espacios no esten vacios
			# de estar correcto guarda las variables en la DB con la funcion 'insert_row()'
			# caso contrario mando una alerta con el problema

			if validation_password() and validation_numbers() and seach_user():

				if (    
				len(self.user.get())    !=0 and
				len(self.password.get())!=0 and
				len(self.name.get())    !=0 and
				len(self.id_type.get()) !=0 and
				len(self.id_number.get())!=0 and
				len(self.age.get())     !=0 and
				len(self.email.get())   !=0
				):
					insert_row()
					window.destroy()
					messagebox.showinfo(message='registro exitoso',title='exitoso')
					
					
				else:
					messagebox.showinfo(message='complete todos los espacios',title='error')
		
		def insert_row():

			# se encarca de subir los datos

			conn = sql.connect('prestamo.db')
			cursor = conn.cursor()
			cursor.execute(f"INSERT INTO login VALUES ('{self.user.get()}','{self.password.get()}','{self.name.get()}','{self.id_type.get()}',{self.id_number.get()},{self.age.get()},'{self.email.get()}');")
			conn.commit()
			conn.close()
			
		
		# boton que devuelva a la ventana, verifique los datos, suba a la base de datos

		Button(frame, text= 'registrar', command= validation).grid(row=9, column=0)

		# boton que devuelve al menu de login

		Button(frame, text= 'volver', command= window.destroy).grid(row=9, column=1)