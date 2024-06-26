from tkinter import *
import os
import imageio
from mtcnn.mtcnn import MTCNN
import database as db
import utils as ut

# Variables de inicio
path = "/home/daniel/Universidad/Semillero/faceRecognition"

res_bd = {"id": 0, "affected": 0}  # db variables


def register_face_db(img, screen1):
    ''' 
    Registra la cara en la base de datos.

    Parametros:
    img (str): La ruta de la imagen.
    screen1 (Tkinter.Toplevel): La pantalla donde se mostrará el mensaje de resultado.
    '''
    name_user = img.replace(".jpg", "").replace(".png", "")
    res_bd = db.registerUser(name_user, path + "/" + img)

    ut.getEnter(screen1)
    if res_bd["affected"]:
        ut.printAndShow(
            screen1, "Bienvenido al sistema. Se ha registrado correctamente", True)
    else:
        ut.printAndShow(screen1, "Error, No se ha podido registrar", False)
    os.remove(path + "/" + img)


def register_capture(user_reg_img, user_entry1, screen1):
    ''' 
    Captura la imagen de la cara para el registro.

    Parametros:
    user_reg_img (str): Nombre del archivo de imagen para el registro.
    user_entry1 (Tkinter.Entry): Entrada de usuario que se limpiará después de la captura.
    screen1 (Tkinter.Toplevel): La pantalla donde se mostrará el mensaje de resultado.
    '''
    img = f"{user_reg_img}.jpg"
    img_path = os.path.join(path, img)

    ut.capture_image("Registro Facial", img_path)

    user_entry1.delete(0, END)

    pixels = imageio.imread(img_path)
    faces = MTCNN().detect_faces(pixels)
    if faces:
        # Si se detectan caras, procesa la imagen y registra la cara en la base de datos
        ut.face(img_path, faces)
        register_face_db(img, screen1)
    else:
        ut.printAndShow(screen1, "No hay ninguna cara para detectar", False)
