from tkinter import *
from tkinter import messagebox as msg
import matplotlib as plt
import cv2
import imageio


color_white = "#f4f5f4"
color_black = "#101010"
color_black_btn = "#202020"
color_background = "#151515"
font_label = "Arial"
size_screen = "500x300"
color_success = "\033[1;32;40m"
color_error = "\033[1;31;40m"
color_normal = "\033[0;37;40m"


def getEnter(screen):
    ''' 
    Agrega un espacio en la pantalla.

    Parameters:
    screen (Tkinter.Toplevel): La pantalla donde se agregará el espacio.
    '''
    Label(screen, text="", bg=color_background).pack()


def printAndShow(screen, text, flag):
    ''' 
    Imprime y muestra un mensaje en la pantalla.

    Parametros:
    screen (Tkinter.Toplevel): La pantalla donde se mostrará el mensaje.
    text (str): El texto del mensaje.
    flag (bool): Indica si el mensaje es de éxito (True) o de error (False).
    '''
    if flag:
        print(color_success + text + color_normal)
        screen.destroy()
        msg.showinfo(message=text, title="¡Éxito!")
    else:
        print(color_error + text + color_normal)
        Label(screen, text=text, fg="red", bg=color_background,
              font=(font_label, 12)).pack()


def configure_screen(screen, text):
    ''' 
    Configura los estilos globales de una pantalla.

    Parametros:
    screen (Tkinter.Toplevel): La pantalla a configurar.
    text (str): El texto del título de la pantalla.
    '''
    screen.title(text)
    screen.geometry(size_screen)
    screen.configure(bg=color_background)
    Label(screen, text=f"¡{text}!", fg=color_white, bg=color_black, font=(
        font_label, 18), width="500", height="2").pack()


def credentials(screen, var, flag, command):
    ''' 
    Configura la entrada de usuario.

    Parametros:
    screen (Tkinter.Toplevel): La pantalla donde se configurará la entrada.
    var (Tkinter.StringVar): Variable para almacenar el valor ingresado.
    command: Eepecifica el comando dependiendo de si es registro o ingreso al sistema

    Return:
    Tkinter.Entry: La entrada de usuario configurada.
    '''
    Label(screen, text="Usuario:", fg=color_white,
          bg=color_background, font=(font_label, 12)).pack()
    entry = Entry(screen, textvariable=var,
                  justify=CENTER, font=(font_label, 12))
    entry.focus_force()
    entry.pack(side=TOP, ipadx=30, ipady=6)

    getEnter(screen)
    Button(screen, text="Capturar rostro", fg=color_white, bg=color_black_btn, activebackground=color_background,
           borderwidth=0, font=(font_label, 14), height="2", width="40", command=command).pack()
    return entry


def face(img, faces):
    ''' 
    Recorta y guarda las caras detectadas en una imagen.

    Parametros:
    img (str): La ruta de la imagen.
    faces (list): Lista de caras detectadas por MTCNN.
    '''
    data = imageio.imread(img)
    for i, face in enumerate(faces):
        x1, y1, width, height = face["box"]
        x2, y2 = x1 + width, y1 + height
        cropped_face = data[y1:y2, x1:x2]
        resized_face = cv2.resize(
            cropped_face, (150, 200), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(f"{img}_face_{i}.jpg", resized_face)


def capture_image(window_name, img_path):
    ''' 
    Captura una imagen desde la cámara y la guarda en la ruta especificada.

    Parametros:
    window_name (str): El nombre de la ventana de captura.
    img_path (str): La ruta donde se guardará la imagen capturada.
    '''
    cap = cv2.VideoCapture(0)
    cv2.namedWindow(window_name)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error al acceder a la cámara.")
            break
        
        cv2.imshow(window_name, frame)

        key = cv2.waitKey(1) & 0xFF
        if key == 32:  # Código de la tecla Espacio
            cv2.imwrite(img_path, frame)
            print(f"Imagen guardada en {img_path}")
            break
        elif key == 27:  # Código de la tecla ESC
            print("Captura cancelada.")
            break

    cap.release()
    cv2.destroyAllWindows()
