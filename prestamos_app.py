from tkinter import *
from w_login import W_login

if __name__ == "__main__":
    
    w_login = Tk()
    application = W_login(w_login,"prestamos","350x150")
    w_login.mainloop()