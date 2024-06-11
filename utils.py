from tkinter import *
from tkinter import messagebox as msg
import cv2
import imageio
import mediapipe as mp


blanco = "#FFFFFF"
negro = "#000000"
btn_negro = "#383636"
fondo = "#575454"
fuente = "Arial"
size_screen = "500x300"
success = "\033[1;32;40m"
error = "\033[1;31;40m"
base = "\033[0;36;40m"

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils


def getEnter(screen):
    ''' 
    Agrega un espacio en la pantalla.

    Parametros:
    screen (Tkinter.Toplevel): La pantalla donde se agregará el espacio.
    '''
    Label(screen, text="", bg=fondo).pack()


def printAndShow(screen, text, flag):
    ''' 
    Imprime y muestra un mensaje en la pantalla.

    Parametros:
    screen (Tkinter.Toplevel): La pantalla donde se mostrará el mensaje.
    text (str): El texto del mensaje.
    flag (bool): Indica si el mensaje es de éxito (True) o de error (False).
    '''
    if flag:
        print(success + text + base)
        screen.destroy()
        msg.showinfo(message=text, title="¡Éxito!")
    else:
        print(error + text + base)
        Label(screen, text=text, fg="red", bg=fondo,
              font=(fuente, 12)).pack()


def configure_screen(screen, text):
    ''' 
    Configura los estilos globales de una pantalla.

    Parametros:
    screen (Tkinter.Toplevel): La pantalla a configurar.
    text (str): El texto del título de la pantalla.
    '''
    screen.title(text)
    screen.geometry(size_screen)
    screen.configure(bg=fondo)
    Label(screen, text=f"¡{text}!", fg=blanco, bg=negro, font=(
        fuente, 18), width="500", height="2").pack()


def credentials(screen, var, command):
    ''' 
    Configura la entrada de usuario.

    Parametros:
    screen (Tkinter.Toplevel): La pantalla donde se configurará la entrada.
    var (Tkinter.StringVar): Variable para almacenar el valor ingresado.
    command (function): Especifica el comando dependiendo de si es registro o ingreso al sistema.

    Return:
    Tkinter.Entry: La entrada de usuario configurada.
    '''
    Label(screen, text="Usuario:", fg=blanco,
          bg=fondo, font=(fuente, 12)).pack()
    entry = Entry(screen, textvariable=var,
                  justify=CENTER, font=(fuente, 12))
    entry.focus_force()
    entry.pack(side=TOP, ipadx=30, ipady=6)

    getEnter(screen)
    Button(screen, text="Capturar rostro", fg=blanco, bg=btn_negro, activebackground=fondo,
           borderwidth=0, font=(fuente, 14), height="2", width="40", command=command).pack()
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
        x1, y1, width, height = face["box"]  # Obtener coordenadas del rostro
        x2, y2 = x1 + width, y1 + height
        # Identifica y recorta la cara en la imagen completa
        cropped_face = data[y1:y2, x1:x2]
        resized_face = cv2.resize(
            cropped_face, (150, 200), interpolation=cv2.INTER_CUBIC)  # Redimensiona
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
        if key == 32:  # Espacio
            cv2.imwrite(img_path, frame)
            print(f"Imagen guardada en {img_path}")
            break
        elif key == 27:  # ESC
            print("Captura cancelada.")
            break

    cap.release()
    cv2.destroyAllWindows()


def detect_faces_mediapipe(image_path):
    ''' 
    Detecta rostros en una imagen usando MediaPipe.

    Parametros:
    image_path (str): La ruta de la imagen a procesar.

    Returns:
    list: Lista de caras detectadas.
    '''
    image = cv2.imread(image_path)
    with mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection:
        results = face_detection.process(
            cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        if results.detections:
            faces = []
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = image.shape
                x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin *
                                                       ih), int(bboxC.width * iw), int(bboxC.height * ih)
                faces.append({"box": [x, y, w, h]})
            return faces
        else:
            return []

# Actualizamos la función de captura de imágenes para incluir MediaPipe


def capture_image_mediapipe(window_name, img_path):
    ''' 
    Captura una imagen desde la cámara y la guarda en la ruta especificada usando MediaPipe para la detección.

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
        if key == 32:  # Espacio
            cv2.imwrite(img_path, frame)
            print(f"Imagen guardada en {img_path}")
            break
        elif key == 27:  # ESC
            print("Captura cancelada.")
            break

    cap.release()
    cv2.destroyAllWindows()

    faces = detect_faces_mediapipe(img_path)
    if faces:
        face(img_path, faces)
    else:
        print("No se detectó ningún rostro con MediaPipe.")
