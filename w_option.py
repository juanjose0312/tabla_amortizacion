from tkinter import *

from ventanas import Window
from w_simulator_credit import W_simulator_credit
from w_visualaize_credits_pre import W_visualaize_credits_pre


class W_option(Window):

    def __init__(self, window, title, geometry, user):
        super().__init__(window, title, geometry)

        self.user = user.get()

        # crear un frame container
        frame = LabelFrame(self.wind, text='opciones')
        frame.grid(row=0, column=1, columnspan=3, pady= 20, padx= 40) 

        def open_simulator_credit():
            w_simulator_credit = Tk()
            W_simulator_credit(w_simulator_credit,"simular credito","1000x450", self.user)

        Button(frame, text= ' simular credito', command= open_simulator_credit).grid(row=1, column=0)

        def visualaize_credits_pre():
            w_visualaize_credits = Tk()
            W_visualaize_credits_pre(w_visualaize_credits,"visualizar credito","1000x330", self.user)

        Button(frame, text= '  ver creditos  ', command= visualaize_credits_pre).grid(row=2, column=0)