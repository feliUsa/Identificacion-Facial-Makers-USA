import mysql.connector as db
import json

with open('conexion.json') as json_file:
    keys = json.load(json_file)

def convertToBinaryData(filename):
    ''' 
    Convierte un archivo a datos binarios.

    Parametros:
    filename (str): La ruta del archivo a convertir.

    Return:
    bytes: Los datos binarios del archivo.
    '''
    try:
        with open(filename, 'rb') as file:
            binaryData = file.read()
        return binaryData
    except Exception as e:
        print(f"Error al convertir archivo a binario: {e}")
        return None

def write_file(data, path):
    ''' 
    Escribe datos binarios en un archivo.

    Parametros:
    data (bytes): Los datos binarios a escribir.
    path (str): La ruta del archivo donde se escribirán los datos.
    '''
    try:
        with open(path, 'wb') as file:
            file.write(data)
    except Exception as e:
        print(f"Error al escribir archivo: {e}")

def registerUser(name, photo):
    ''' 
    Registra un usuario en la base de datos.

    Parametros:
    name (str): El nombre del usuario.
    photo (str): La ruta de la foto del usuario.

    Return:
    dict: Un diccionario con el id del usuario y el número de filas afectadas.
    '''
    id = 0
    inserted = 0
    try:
        con = get_db_connection()
        cursor = con.cursor()
        sql = "INSERT INTO usuarios(name, photo) VALUES (%s, %s)"
        pic = convertToBinaryData(photo)

        if pic:
            cursor.execute(sql, (name, pic))
            con.commit()
            inserted = cursor.rowcount
            id = cursor.lastrowid
    except db.Error as e:
        print(f"Failed inserting image: {e}")
    finally:
        if con.is_connected():
            cursor.close()
            con.close()
    return {"id": id, "affected": inserted}

def getUser(name, path):
    ''' 
    Obtiene un usuario de la base de datos.

    Parametros:
    name (str): El nombre del usuario.
    path (str): La ruta donde se guardará la foto del usuario.

    Return:
    dict: Un diccionario con el id del usuario y el número de filas afectadas.
    '''
    id = 0
    rows = 0
    try:
        con = db.connect(host=keys["host"], user=keys["user"], password=keys["password"], database=keys["database"])
        cursor = con.cursor()
        sql = "SELECT * FROM usuarios WHERE name = %s"
        cursor.execute(sql, (name,))
        records = cursor.fetchall()

        for row in records: # Escribir la foto
            id = row[0]
            write_file(row[2], path)
        rows = len(records)
    except db.Error as e:
        print(f"Failed to read image: {e}")
    finally:
        if con.is_connected():
            cursor.close()
            con.close()
    return {"id": id, "affected": rows}

def get_db_connection():
    return db.connect(host=keys["host"], user=keys["user"], password=keys["password"], database=keys["database"])
