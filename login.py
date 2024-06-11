from tkinter import *
import os
import cv2
import imageio
import face_recognition
from deepface import DeepFace
from mtcnn.mtcnn import MTCNN
import database as db
import utils as ut

path = "/home/daniel/Universidad/Semillero/faceRecognition"
success = "\033[1;32;40m"
error = "\033[1;31;40m"
base = "\033[0;36;40m"


def compatibility(img1, img2):
    ''' 
    Compara dos imágenes de caras usando ORB.

    Parametros:
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

    Parametros:
    user_login (str): El nombre del usuario que intenta iniciar sesión.
    user_entry2 (Tkinter.Entry): Entrada de usuario que se limpiará después de la captura.
    screen2 (Tkinter.Toplevel): La pantalla donde se mostrará el mensaje de resultado.
    '''
    img = f"{user_login}_login.jpg"
    img_path = os.path.join(path, img)
    img_user = f"{user_login}.jpg"

    ut.capture_image_mediapipe("Login Facial", img_path)

    user_entry2.delete(0, END)  # Limpiar la entrada

    ut.getEnter(screen2)

    # Obtiene el usuario de la base de datos
    res_db = db.getUser(user_login, path + "/" + img_user)

    if res_db["affected"]:
        my_files = os.listdir()  # Lista los archivos en el directorio actual
        if img_user in my_files:
            # Comparacion usando ORB
            comp_orb = compatibility(cv2.imread(
                img_user, 0), cv2.imread(img_path, 0))
            # Comparacion usando DeepFace
            verified_deepface, distance_deepface = compatibility_deepface(
                img_user, img_path)
            # Comparacion usando face_recognition
            verified_face_recognition = compatibility_face_recognition(
                img_user, img_path)

            # Añadimos una verificación adicional con MediaPipe
            faces = ut.detect_faces_mediapipe(img_path)
            verified_mediapipe = len(faces) > 0

            # Condiciones de acceso
            if (comp_orb >= 0.95 and (verified_deepface or verified_face_recognition or verified_mediapipe)) or \
                (comp_orb >= 0.90 and verified_deepface and verified_face_recognition and verified_mediapipe) or \
                (verified_deepface and verified_face_recognition and verified_mediapipe):
                print("{}Compatibilidad ORB: {:.1%}, DeepFace: {}, face_recognition: {}, MediaPipe: {}{}".format(
                    success, float(comp_orb), verified_deepface, verified_face_recognition, verified_mediapipe, base))
                ut.printAndShow(screen2, f"Bienvenido, {user_login}", True)
            else:
                print("{}Compatibilidad ORB: {:.1%}, DeepFace: {}, face_recognition: {}, MediaPipe: {}{}".format(
                    error, float(comp_orb), verified_deepface, verified_face_recognition, verified_mediapipe, base))
                ut.printAndShow(screen2, "Incompatibilidad de datos", False)
            os.remove(img_user)  # Elimina la imagen temporal

        else:
            ut.printAndShow(screen2, "Usuario no ha sido encontrado", False)
    else:
        ut.printAndShow(screen2, "Usuario no ha sido encontrado", False)
    os.remove(img_path)  # Elimina la imagen temporal


def compatibility_deepface(img1_path, img2_path):
    ''' 
    Compara dos imágenes de caras usando DeepFace con diferentes modelos.

    Parametros:
    img1_path (str): La ruta de la primera imagen.
    img2_path (str): La ruta de la segunda imagen.

    Returns:
    tuple: Un booleano que indica si alguna verificación es exitosa y la distancia de la coincidencia.
    '''
    models = ['VGG-Face', 'Facenet', 'OpenFace', 'DeepFace', 'DeepID']
    for model in models:
        try:
            # Verifica las img1_path e img2_path usando DeepFace
            result = DeepFace.verify(
                img1_path, img2_path, model_name=model, enforce_detection=False)
            if result["verified"]:
                return True, result["distance"]
        except Exception as e:
            print(f"Error loading model {model}: {e}")
    return False, None


def compatibility_face_recognition(img1_path, img2_path):
    ''' 
    Compara dos imágenes de caras usando face_recognition.

    Parametros:
    img1_path (str): La ruta de la primera imagen.
    img2_path (str): La ruta de la segunda imagen.

    Returns:
    bool: True si las imágenes coinciden, False en caso contrario.
    '''
    img1 = face_recognition.load_image_file(img1_path)
    img2 = face_recognition.load_image_file(img2_path)

    encodings1 = face_recognition.face_encodings(img1)
    encodings2 = face_recognition.face_encodings(img2)

    if len(encodings1) > 0 and len(encodings2) > 0:
        return face_recognition.compare_faces([encodings1[0]], encodings2[0])[0]
    return False
