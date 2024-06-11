from tkinter import Tk, Label, Button, Toplevel, StringVar
import utils as ut
import registro as reg
import login as log

size_screen = "500x300"
txt_login = "Iniciar Sesión"
txt_register = "Registrarse"
color_white = "#f4f5f4"
color_black = "#101010"
color_black_btn = "#202020"
color_background = "#151515"
font_label = "Arial"


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
root.configure(bg=color_background)
Label(text="¡Bienvenido(a)!", fg=color_white, bg=color_black,
      font=(font_label, 18), width="500", height="2").pack()

ut.getEnter(root)

# Registro
Button(text=txt_login, fg=color_white, bg=color_black_btn, activebackground=color_background,
       borderwidth=0, font=(font_label, 14), height="2", width="40", command=login).pack()

ut.getEnter(root)

# Login
Button(text=txt_register, fg=color_white, bg=color_black_btn, activebackground=color_background,
       borderwidth=0, font=(font_label, 14), height="2", width="40", command=register).pack()

root.mainloop()
