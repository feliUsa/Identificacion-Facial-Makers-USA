from tkinter import *
from tkinter import messagebox as msg
import os
import cv2
from matplotlib import pyplot as plt
from mtcnn.mtcnn import MTCNN
import database as db

# Variables de inicio
path = "/home/daniel/Universidad/Semillero/faceRecognition"
txt_login = "Iniciar Sesión"
txt_register = "Registrarse"

color_white = "#f4f5f4"
color_black = "#101010"

color_black_btn = "#202020"
color_background = "#151515"

font_label = "Arial"
size_screen = "500x300"

# colors
color_success = "\033[1;32;40m"
color_error = "\033[1;31;40m"
color_normal = "\033[0;37;40m"

res_bd = {"id": 0, "affected": 0} # db variables

# GENERAL
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
        Label(screen, text=text, fg="red", bg=color_background, font=(font_label, 12)).pack()

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
    Label(screen, text=f"¡{text}!", fg=color_white, bg=color_black, font=(font_label, 18), width="500", height="2").pack()

def credentials(screen, var, flag):
    ''' 
    Configura la entrada de usuario.

    Parametros:
    screen (Tkinter.Toplevel): La pantalla donde se configurará la entrada.
    var (Tkinter.StringVar): Variable para almacenar el valor ingresado.
    flag (bool): Indica si es para iniciar sesión (True) o registrar (False).

    Return:
    Tkinter.Entry: La entrada de usuario configurada.
    '''
    Label(screen, text="Usuario:", fg=color_white, bg=color_background, font=(font_label, 12)).pack()
    entry = Entry(screen, textvariable=var, justify=CENTER, font=(font_label, 12))
    entry.focus_force()
    entry.pack(side=TOP, ipadx=30, ipady=6)

    getEnter(screen)
    if flag:
        Button(screen, text="Capturar rostro", fg=color_white, bg=color_black_btn, activebackground=color_background, borderwidth=0, font=(font_label, 14), height="2", width="40", command=login_capture).pack()
    else:
        Button(screen, text="Capturar rostro", fg=color_white, bg=color_black_btn, activebackground=color_background, borderwidth=0, font=(font_label, 14), height="2", width="40", command=register_capture).pack()
    return entry

def face(img, faces):
    ''' 
    Recorta y guarda las caras detectadas en una imagen.

    Parameters:
    img (str): La ruta de la imagen.
    faces (list): Lista de caras detectadas por MTCNN.
    '''
    data = plt.imread(img)
    for i in range(len(faces)):
        x1, y1, ancho, alto = faces[i]["box"]  # Coordenadas delimitadoras
        x2, y2 = x1 + ancho, y1 + alto  # Coordenadas borde inferior derecho
        plt.subplot(1, len(faces), i + 1)
        plt.axis("off")
        face = cv2.resize(data[y1:y2, x1:x2], (150, 200), interpolation=cv2.INTER_CUBIC)  # Redimensiona la cara
        cv2.imwrite(img, face)
        plt.imshow(data[y1:y2, x1:x2])
        


# REGISTER
def register_face_db(img):
    ''' 
    Registra la cara en la base de datos.

    Parameters:
    img (str): La ruta de la imagen.
    '''
    name_user = img.replace(".jpg", "").replace(".png", "")
    res_bd = db.registerUser(name_user, path + "/" + img)

    getEnter(screen1)
    if res_bd["affected"]:
        printAndShow(screen1, "Bienvenido al sistema. Se ha registrado correctamente", True)
    else:
        printAndShow(screen1, "Error, No se ha podido registrar", False)
    os.remove(path + "/" + img)

def register_capture():
    ''' 
    Captura la imagen de la cara para el registro.
    '''
    cap = cv2.VideoCapture(0)
    user_reg_img = user1.get()
    img = f"{user_reg_img}.jpg"
    img_path = os.path.join(path, img)

    while True:
        ret, frame = cap.read()
        cv2.imshow("Registro Facial", frame)
        if cv2.waitKey(1) == 27:  # Presionar 'ESC' para capturar
            break
    
    cv2.imwrite(img_path, frame)
    cap.release()
    cv2.destroyAllWindows()

    user_entry1.delete(0, END)
    
    pixels = plt.imread(img_path)
    faces = MTCNN().detect_faces(pixels)
    if faces:
        face(img_path, faces)
        register_face_db(img)
    else:
        printAndShow(screen1, "No hay ninguna cara para detectar", False)

def register():
    ''' 
    Abre la pantalla de registro.
    '''
    global user1
    global user_entry1
    global screen1

    screen1 = Toplevel(root)
    user1 = StringVar()

    configure_screen(screen1, txt_register)
    user_entry1 = credentials(screen1, user1, 0)

# LOGIN #
def compatibility(img1, img2):
    ''' 
    Compara dos imágenes de caras usando ORB.

    Parameters:
    img1 (numpy.ndarray): La primera imagen.
    img2 (numpy.ndarray): La segunda imagen.

    Returns:
    float: La proporción de coincidencias entre las dos imágenes.
    '''
    orb = cv2.ORB_create()

    kpa, dac1 = orb.detectAndCompute(img1, None)
    kpa, dac2 = orb.detectAndCompute(img2, None)

    comp = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True) # Comparador de img

    matches = comp.match(dac1, dac2) # Verifica coincidencias

    similar = [x for x in matches if x.distance < 70]
    if len(matches) == 0:
        return 0
    return len(similar) / len(matches)

def login_capture():
    ''' 
    Captura la imagen de la cara para el inicio de sesión.
    '''
    cap = cv2.VideoCapture(0)
    user_login = user2.get()
    img = f"{user_login}_login.jpg"
    img_path = os.path.join(path, img)
    img_user = f"{user_login}.jpg"

    while True: # Caputar el frame
        ret, frame = cap.read()
        cv2.imshow("Login Facial", frame)
        if cv2.waitKey(1) == 27:  # Presiona 'ESC' para capturar
            break
    
    cv2.imwrite(img_path, frame)  # Guarda el frame
    cap.release()
    cv2.destroyAllWindows()

    user_entry2.delete(0, END) # Limpiar la entrada
    
    pixels = plt.imread(img_path)
    faces = MTCNN().detect_faces(pixels)  # Detectar caras en img

    face(img_path, faces)
    getEnter(screen2)

    res_db = db.getUser(user_login, path + "/" + img_user)  # Obtiene el usuario de la base de datos
    if res_db["affected"]:
        my_files = os.listdir()  # Lista los archivos en el directorio actual
        if img_user in my_files:
            face_reg = cv2.imread(img_user, 0)  # Lee la imagen del registro en escala de grises
            face_log = cv2.imread(img_path, 0)  # Lee la imagen del login en escala de grises

            comp = compatibility(face_reg, face_log)  # Compara las imgs
            
            if comp >= 0.94:
                print("{}Compatibilidad del {:.1%}{}".format(color_success, float(comp), color_normal))
                printAndShow(screen2, f"Bienvenido, {user_login}", True)
            else:
                print("{}Compatibilidad del {:.1%}{}".format(color_error, float(comp), color_normal))
                printAndShow(screen2, "Incompatibilidad de datos", False)
            os.remove(img_user)  # Elimina la imagen temporal
    
        else:
            printAndShow(screen2, "Usuario no ha sido encontrado", False)
    else:
        printAndShow(screen2, "Usuario no ha sido encontrado", False)
    os.remove(img_path)  # Elimina la imagen temporal

def login():
    ''' 
    Abre la pantalla de inicio de sesión.
    '''
    global screen2
    global user2
    global user_entry2

    screen2 = Toplevel(root)
    user2 = StringVar()

    configure_screen(screen2, txt_login)
    user_entry2 = credentials(screen2, user2, 1)

root = Tk()
root.geometry(size_screen)
root.title("AVM")
root.configure(bg=color_background)
Label(text="¡Bienvenido(a)!", fg=color_white, bg=color_black, font=(font_label, 18), width="500", height="2").pack()

getEnter(root)
Button(text=txt_login, fg=color_white, bg=color_black_btn, activebackground=color_background, borderwidth=0, font=(font_label, 14), height="2", width="40", command=login).pack()

getEnter(root)
Button(text=txt_register, fg=color_white, bg=color_black_btn, activebackground=color_background, borderwidth=0, font=(font_label, 14), height="2", width="40", command=register).pack()

root.mainloop()