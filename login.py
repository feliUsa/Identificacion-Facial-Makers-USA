from tkinter import *
import os
import cv2
import imageio

from mtcnn.mtcnn import MTCNN
import database as db
import utils as ut


path = "/home/daniel/Universidad/Semillero/faceRecognition"
color_success = "\033[1;32;40m"
color_error = "\033[1;31;40m"
color_normal = "\033[0;37;40m"


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

    # Comparador de img
    comp = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    matches = comp.match(dac1, dac2)  # Verifica coincidencias

    similar = [x for x in matches if x.distance < 70]
    if len(matches) == 0:
        return 0
    return len(similar) / len(matches)


def login_capture(user_login, user_entry2, screen2):
    ''' 
    Captura la imagen de la cara para el inicio de sesión.
    '''
    img = f"{user_login}_login.jpg"
    img_path = os.path.join(path, img)
    img_user = f"{user_login}.jpg"

    ut.capture_image("Login Facial", img_path)

    user_entry2.delete(0, END)  # Limpiar la entrada

    pixels = imageio.imread(img_path)
    faces = MTCNN().detect_faces(pixels)  # Detectar caras en img
    ut.face(img_path, faces)
    ut.getEnter(screen2)
    # Obtiene el usuario de la base de datos
    res_db = db.getUser(user_login, path + "/" + img_user)

    if res_db["affected"]:
        my_files = os.listdir()  # Lista los archivos en el directorio actual
        if img_user in my_files:
            # Lee la imagen del registro en escala de grises
            face_reg = cv2.imread(img_user, 0)
            # Lee la imagen del login en escala de grises
            face_log = cv2.imread(img_path, 0)

            comp = compatibility(face_reg, face_log)  # Compara las imgs

            if comp >= 0.94:
                print("{}Compatibilidad del {:.1%}{}".format(
                    color_success, float(comp), color_normal))
                ut.printAndShow(screen2, f"Bienvenido, {user_login}", True)
            else:
                print("{}Compatibilidad del {:.1%}{}".format(
                    color_error, float(comp), color_normal))
                ut.printAndShow(screen2, "Incompatibilidad de datos", False)
            os.remove(img_user)  # Elimina la imagen temporal

        else:
            ut.printAndShow(screen2, "Usuario no ha sido encontrado", False)
    else:
        ut.printAndShow(screen2, "Usuario no ha sido encontrado", False)
    os.remove(img_path)  # Elimina la imagen temporal
