from tkinter import *
import utils as ut
import registro as reg
import login as log

size_screen = "500x300"
txt_login = "Iniciar Sesión"
txt_register = "Registrarse"
blanco = "#FFFFFF"
negro = "#000000"
btn_negro = "#383636"
fondo = "#575454"
fuente = "Arial"


def register():
    ''' 
    Abre la pantalla de registro.
    '''
    global user1
    global user_entry1
    global screen1

    screen1 = Toplevel(root)
    user1 = StringVar()

    ut.configure_screen(screen1, txt_register)
    user_entry1 = ut.credentials(screen1, user1, lambda: reg.register_capture(
        user1.get(), user_entry1, screen1))


def login():
    ''' 
    Abre la pantalla de inicio de sesión.
    '''
    global screen2
    global user2
    global user_entry2

    screen2 = Toplevel(root)
    user2 = StringVar()

    ut.configure_screen(screen2, txt_login)
    user_entry2 = ut.credentials(screen2, user2, lambda: log.login_capture(
        user2.get(), user_entry2, screen2))


# Ventana principal
root = Tk()
root.geometry(size_screen)
root.title("AVM")
root.configure(bg=fondo)
Label(text="¡Bienvenido(a)!", fg=blanco, bg=negro,
      font=(fuente, 18), width="500", height="2").pack()

ut.getEnter(root)

# Registro
Button(text=txt_login, fg=blanco, bg=btn_negro, activebackground=fondo,
       borderwidth=0, font=(fuente, 14), height="2", width="40", command=login).pack()

ut.getEnter(root)

# Login
Button(text=txt_register, fg=blanco, bg=btn_negro, activebackground=fondo,
       borderwidth=0, font=(fuente, 14), height="2", width="40", command=register).pack()

root.mainloop()
