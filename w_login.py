import sqlite3 as sql
from tkinter import * 
from tkinter import messagebox

from ventanas import Window
from w_option import W_option
from w_register import W_register


class W_login(Window):
    def __init__(self, window, title, geometry):
        super().__init__(window, title, geometry)

        # crear un frame container
        frame = LabelFrame(self.wind, text='iniciar sesion')
        frame.grid(row=0, column=1, columnspan=3, pady= 20, padx= 40) 

        # crear el input de usuario
        Label(frame, text= 'usuario : ').grid(row=0, column=0)
        self.user = Entry(frame)
        self.user.focus()
        self.user.grid(row=0, column=1)

        # crear el input de clave
        Label(frame, text= 'clave : ').grid(row=1, column=0)
        self.password = Entry(frame, show="*")
        self.password.grid(row=1, column=1)

        def seach_user():

            # buscar los registros por el usuario y traer a comparacion
            conn = sql.connect('prestamo.db')   
            cursor = conn.cursor()
            instruccion = f"SELECT * FROM login WHERE user='{self.user.get()}'"
            cursor.execute(instruccion)
            datos = cursor.fetchall()
            conn.commit()
            conn.close()

            if len(datos)==0:
                # en caso de que no haya ningun usuario con ese nombre
                messagebox.showinfo(message='usuarion o clave incorrectos',title='info')
                return False
            
            if datos[0][1]==self.password.get():
                # en caso de ser el usuario y la clave correcta
                return True

            messagebox.showinfo(message='usuarion o clave incorrectos',title='info')
            return False    

        # crear boton de entrar

        def open_option():
            if seach_user(): 
                w_option = Tk()
                W_option(w_option,"opciones","350x150",self.user)
                window.destroy()

        Button(frame, text= 'entrar', command= open_option).grid(row=2, column=0)

        # crear boton de registro

        def open_register():
            w_register = Tk()
            W_register(w_register,"registrarse","350x250")

        Button(frame, text= 'registrarse', command= open_register).grid(row=2, column=1)