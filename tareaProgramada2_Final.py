# Elaborado por: Alejandro Madrigal y Brandon Meza
# Fecha de creacion: 27/05/2026
# Ultima modificacion: 04/06/2026
# Version de Python: 3.11

import tkinter as tk
from tkinter import messagebox
import pickle
import re
import random
from datetime import date, datetime

# =========================================================
# Tupla global con los tipos de sangre posibles
tiposDeSangre = ("O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-")

# Lista global que funciona como matriz para guardar los donadores
# Formato de cada donador:
# [[nombre, apellido1, apellido2], cedula, tipoSangre(int), sexo(bool), (dia, mes, año), peso, correo, telefono, estado, justificacion]
baseDeDatos = []

# Diccionario global con los lugares de donacion por provincia
# Clave = numero de provincia, Valor = lista de lugares
lugaresDonacion = {
    1: ["Banco Nacional de Sangre", "Hospital Mexico", "Hospital San Juan de Dios"],
    2: ["Hospital San Rafael de Alajuela", "Hospital de San Ramon", "Hospital del Canton Norteno"],
    3: ["Hospital Max Peralta"],
    4: ["Hospital San Vicente de Paul"],
    5: ["Hospital La Anexion en Nicoya", "Hospital Enrique Baltodano de Liberia"],
    6: ["Hospital Monsenor Sanabria"],
    7: ["Hospital Tony Facio", "Hospital de Guapiles"]
}

# Diccionario global con los nombres de provincia
nombreProvincias = {
    1: "San Jose",
    2: "Alajuela",
    3: "Cartago",
    4: "Heredia",
    5: "Guanacaste",
    6: "Puntarenas",
    7: "Limon"
}

# Diccionario con las justificaciones de GEMINI para donantes inactivos
justificaciones = {
    1: "Enfermedades Infecciosas/Cronicas: Portador de VIH, Hepatitis B o C, sifilis, tuberculosis, diabetes insulinodependiente o afecciones graves de corazon, rinon o pulmon.",
    2: "Conductas de Riesgo: Nueva pareja sexual o mas de una pareja sexual en los ultimos 3 meses, o relaciones sexuales por dinero o drogas.",
    3: "Factores de Salud Fisica: Hemoglobina o hematocrito bajo o alto, presion arterial inestable, fiebre o infecciones recientes.",
    4: "Procedimientos Medicos: Ha recibido transfusiones, trasplantes, cirugias mayores, tatuajes, piercing o endoscopias recientes.",
    5: "Uso de Medicamentos: Consumo de farmacos inyectables sin receta o ciertos medicamentos restringidos.",
    6: "Estilo de Vida y Viajes: Uso de drogas recreativas, consumo de alcohol en las ultimas 24 horas, o viajes recientes a zonas endemicas de malaria o dengue.",
    7: "Situaciones Especificas: Embarazo, lactancia o menstruacion activa al momento de la donacion."
}

# Diccionario de compatibilidad sanguinea - a quien puede donar cada tipo
compatibilidadDonar = {
    "O-":  ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"],
    "O+":  ["O+", "A+", "B+", "AB+"],
    "A-":  ["A-", "A+", "AB-", "AB+"],
    "A+":  ["A+", "AB+"],
    "B-":  ["B-", "B+", "AB-", "AB+"],
    "B+":  ["B+", "AB+"],
    "AB-": ["AB-", "AB+"],
    "AB+": ["AB+"]
}

# Diccionario de compatibilidad sanguinea - de quien puede recibir cada tipo
compatibilidadRecibir = {
    "O-":  ["O-"],
    "O+":  ["O-", "O+"],
    "A-":  ["O-", "A-"],
    "A+":  ["O-", "O+", "A-", "A+"],
    "B-":  ["O-", "B-"],
    "B+":  ["O-", "O+", "B-", "B+"],
    "AB-": ["O-", "A-", "B-", "AB-"],
    "AB+": ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"]
}
# =========================================================


# =========================================================
# FUNCIONES UTILITARIAS
# =========================================================

def cargarBaseDeDatos():
    """
    Funcionalidad: Intenta cargar la base de datos desde el archivo binario
                   baseDeDatos.pkl en memoria. Si no existe, la deja vacia.
    Entradas: Ninguna.
    Salidas: Retorna True si se cargo exitosamente, False si no existia el archivo.
    """
    global baseDeDatos
    try:
        archivo = open("baseDeDatos.pkl", "rb")
        baseDeDatos = pickle.load(archivo)
        archivo.close()
        return True
    except:
        baseDeDatos = []
        return False


def guardarBaseDeDatos():
    """
    Funcionalidad: Guarda la base de datos actual en el archivo binario baseDeDatos.pkl.
    Entradas: Ninguna.
    Salidas: Ninguna. Escribe el archivo baseDeDatos.pkl en la carpeta del programa.
    """
    archivo = open("baseDeDatos.pkl", "wb")
    pickle.dump(baseDeDatos, archivo)
    archivo.close()


def buscarDonadorPorCedula(cedula):
    """
    Funcionalidad: Busca un donador en la base de datos por su numero de cedula.
    Entradas:
        - cedula(str): El numero de cedula a buscar.
    Salidas:
        - indice(int): El indice del donador en la lista, o -1 si no existe.
    """
    for i in range(len(baseDeDatos)):
        if baseDeDatos[i][1] == cedula:
            return i
    return -1


def calcularEdad(tuplaFecha):
    """
    Funcionalidad: Calcula la edad actual de una persona a partir de su
                   fecha de nacimiento almacenada como tupla.
    Entradas:
        - tuplaFecha(tuple): Tupla con (dia, mes, año) de nacimiento.
    Salidas:
        - edad(int): La edad actual de la persona en años.
    """
    hoy = datetime.today()
    dia, mes, año = tuplaFecha
    edad = hoy.year - año
    if (hoy.month, hoy.day) < (mes, dia):
        edad -= 1
    return edad


def cedulaYaExiste(cedula):
    """
    Funcionalidad: Verifica si una cedula ya esta registrada en la base de datos.
    Entradas:
        - cedula(str): La cedula a verificar.
    Salidas: Retorna True si ya existe, False en caso contrario.
    """
    for donador in baseDeDatos:
        if donador[1] == cedula:
            return True
    return False


def generarHtmlBase(titulo, fechaHora, encabezados, filas):
    """
    Funcionalidad: Genera el contenido HTML base para todos los reportes,
                   con estilos, titulo, fecha y tabla de datos.
    Entradas:
        - titulo(str): Titulo del reporte que se muestra en el HTML.
        - fechaHora(str): Fecha y hora de generacion del reporte.
        - encabezados(list): Lista de strings con los titulos de cada columna.
        - filas(list): Lista de listas con los datos de cada fila.
    Salidas:
        - html(str): String con el contenido HTML completo del reporte.
    """
    encabezadosHtml = "".join([f"<th>{e}</th>" for e in encabezados])

    filasHtml = ""
    for i in range(len(filas)):
        color = "#ffffff" if i % 2 == 0 else "#f2f2f2"
        celdas = "".join([f"<td>{c}</td>" for c in filas[i]])
        filasHtml += f'<tr style="background-color:{color};text-align:center;">{celdas}</tr>'

    if filasHtml == "":
        colspan = len(encabezados)
        filasHtml = f"<tr><td colspan='{colspan}' style='text-align:center;'>No hay datos disponibles.</td></tr>"

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8"/>
    <title>{titulo}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 30px; }}
        h1 {{ color: red; }}
        h2 {{ color: #555; font-size: 16px; }}
        table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
        th {{ background-color: #c0392b; color: white; padding: 10px; text-align: center; }}
        td {{ border: 1px solid #ddd; padding: 8px; }}
    </style>
</head>
<body>
    <h1>Reporte de Traduccion</h1>
    <h1>{titulo}</h1>
    <h2>Generado el: {fechaHora}</h2>
    <table>
        <tr>{encabezadosHtml}</tr>
        {filasHtml}
    </table>
</body>
</html>"""


def guardarHtml(contenido, nombreArchivo):
    """
    Funcionalidad: Guarda el contenido HTML en un archivo y muestra mensaje al usuario.
    Entradas:
        - contenido(str): El contenido HTML a guardar.
        - nombreArchivo(str): El nombre del archivo donde se guardara.
    Salidas: Ninguna. Crea el archivo HTML en la carpeta del programa.
    """
    try:
        archivo = open(nombreArchivo, "w", encoding="utf-8")
        archivo.write(contenido)
        archivo.close()
        messagebox.showinfo("Exito", "Reporte creado satisfactoriamente.")
    except:
        messagebox.showerror("Error", "Reporte no creado.")


def ordenarPorNombre(lista):
    """
    Funcionalidad: Ordena una lista de donadores por nombre completo
                   usando el algoritmo de burbuja.
    Entradas:
        - lista(list): Lista de donadores a ordenar.
    Salidas:
        - lista(list): La misma lista ordenada por nombre completo.
    """
    for i in range(len(lista) - 1):
        for j in range(i + 1, len(lista)):
            nombreI = f"{lista[i][0][0]} {lista[i][0][1]} {lista[i][0][2]}"
            nombreJ = f"{lista[j][0][0]} {lista[j][0][1]} {lista[j][0][2]}"
            if nombreI > nombreJ:
                lista[i], lista[j] = lista[j], lista[i]
    return lista


def ordenarPorEdad(lista, descendente=False):
    """
    Funcionalidad: Ordena una lista de donadores por edad usando burbuja.
    Entradas:
        - lista(list): Lista de donadores a ordenar.
        - descendente(bool): Si es True ordena de mayor a menor edad.
    Salidas:
        - lista(list): La misma lista ordenada por edad.
    """
    for i in range(len(lista) - 1):
        for j in range(i + 1, len(lista)):
            edadI = calcularEdad(lista[i][4])
            edadJ = calcularEdad(lista[j][4])
            if (not descendente and edadI > edadJ) or (descendente and edadI < edadJ):
                lista[i], lista[j] = lista[j], lista[i]
    return lista


def ordenarPorProvincia(lista, descendente=False):
    """
    Funcionalidad: Ordena una lista de donadores por numero de provincia
                   usando el primer digito de la cedula y el algoritmo de burbuja.
    Entradas:
        - lista(list): Lista de donadores a ordenar.
        - descendente(bool): Si es True ordena de mayor a menor provincia.
    Salidas:
        - lista(list): La misma lista ordenada por provincia.
    """
    for i in range(len(lista) - 1):
        for j in range(i + 1, len(lista)):
            provI = int(lista[i][1][0])
            provJ = int(lista[j][1][0])
            if (not descendente and provI > provJ) or (descendente and provI < provJ):
                lista[i], lista[j] = lista[j], lista[i]
    return lista


# =========================================================
# VALIDACIONES
# =========================================================

def validarCedula(cedula):
    """
    Funcionalidad: Valida que la cedula tenga el formato #-####-#### y que
                   el primer digito no sea 0.
    Entradas:
        - cedula(str): El numero de cedula ingresado por el usuario.
    Salidas: Retorna True si la cedula es valida, False en caso contrario.
    """
    patron = r'^[1-9]-\d{4}-\d{4}$'
    return re.match(patron, cedula) is not None


def validarFecha(fecha):
    """
    Funcionalidad: Valida que la fecha tenga el formato DD/MM/AAAA y que
                   los valores sean correctos.
    Entradas:
        - fecha(str): La fecha ingresada por el usuario en formato DD/MM/AAAA.
    Salidas: Retorna True si la fecha es valida, False en caso contrario.
    """
    patron = r'^\d{2}/\d{2}/\d{4}$'
    if not re.match(patron, fecha):
        return False
    try:
        partes = fecha.split("/")
        dia = int(partes[0])
        mes = int(partes[1])
        año = int(partes[2])
        date(año, mes, dia)
        return True
    except:
        return False


def validarCorreo(correo):
    """
    Funcionalidad: Valida que el correo tenga uno de los formatos permitidos:
                   texto@texto.texto o texto@texto.texto.texto
    Entradas:
        - correo(str): El correo ingresado por el usuario.
    Salidas: Retorna True si el correo es valido, False en caso contrario.
    """
    patron = r'^[a-zA-Z0-9]+@[a-zA-Z]+\.[a-zA-Z]+(\.[a-zA-Z]+)?$'
    return re.match(patron, correo) is not None


def validarTelefono(telefono):
    """
    Funcionalidad: Valida que el telefono tenga el formato ####-#### y que
                   el primer digito no sea 0, 1, 3 ni 5.
    Entradas:
        - telefono(str): El telefono ingresado por el usuario.
    Salidas: Retorna True si el telefono es valido, False en caso contrario.
    """
    patron = r'^[2467890]\d{3}-\d{4}$'
    return re.match(patron, telefono) is not None


def validarPeso(peso):
    """
    Funcionalidad: Valida que el peso sea un numero mayor a 50 y menor a 120.
    Entradas:
        - peso(str): El peso ingresado por el usuario.
    Salidas: Retorna True si el peso es valido, False en caso contrario.
    """
    try:
        pesoFloat = float(peso)
        return 50 < pesoFloat < 120
    except:
        return False


def esMayorDeEdad(fecha):
    """
    Funcionalidad: Verifica si la persona es mayor de edad comparando su
                   fecha de nacimiento con la fecha actual por mes y año.
    Entradas:
        - fecha(str): La fecha de nacimiento en formato DD/MM/AAAA.
    Salidas: Retorna True si es mayor de edad, False en caso contrario.
    """
    partes = fecha.split("/")
    añoNac = int(partes[2])
    mesNac = int(partes[1])
    hoy = date.today()
    if hoy.year - añoNac > 18:
        return True
    if hoy.year - añoNac == 18 and hoy.month >= mesNac:
        return True
    return False


def obtenerProvinciaPorCedula(cedula):
    """
    Funcionalidad: Obtiene el numero de provincia segun el primer digito
                   de la cedula del donador.
    Entradas:
        - cedula(str): El numero de cedula en formato #-####-####.
    Salidas:
        - numeroProvincia(int): El numero de provincia correspondiente.
    """
    return int(cedula[0])


def obtenerInfoTipoDeSangre(tipoSangre):
    """
    Funcionalidad: Retorna la recomendacion de donacion segun el tipo de sangre.
    Entradas:
        - tipoSangre(str): El tipo de sangre del donador.
    Salidas:
        - info(str): Texto con la recomendacion de donacion para ese tipo.
    """
    recomendaciones = {
        "A+":  "Se recomienda donar sangre entera y plaquetas.",
        "A-":  "Se recomienda donar sangre entera y globulos rojos dobles.",
        "B+":  "Se recomienda donar sangre entera y globulos rojos dobles.",
        "B-":  "Se recomienda donar sangre entera o plaquetas.",
        "O+":  "Se recomienda donar globulos rojos dobles y sangre entera.",
        "O-":  "Eres donante universal. Se recomienda donar globulos rojos dobles y sangre entera.",
        "AB+": "Se recomienda hacer donaciones de plaquetas y de plasma.",
        "AB-": "Se recomienda donar plaquetas y plasma."
    }
    return recomendaciones.get(tipoSangre, "")


# =========================================================
# INSERTAR DONADOR
# =========================================================

def insertarDonador(ventanaPadre):
    """
    Funcionalidad: Abre el formulario para registrar un nuevo donador con todos
                   sus datos. Valida cada campo con expresiones regulares y
                   muestra realimentacion al usuario al registrar.
    Entradas:
        - ventanaPadre(tk.Tk): La ventana principal del programa.
    Salidas: Ninguna. Agrega el donador a la lista global baseDeDatos si es valido.
    """
    ventana = tk.Toplevel(ventanaPadre)
    ventana.title("Insertar Donador")
    ventana.geometry("500x580")
    ventana.resizable(False, False)

    tk.Label(ventana, text="Insertar Donador", font=("Arial", 14, "bold"), fg="red").grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(ventana, text="Cedula (#-####-####):", anchor="w").grid(row=1, column=0, padx=20, pady=5, sticky="w")
    campoCedula = tk.Entry(ventana, width=30)
    campoCedula.grid(row=1, column=1, padx=10)

    tk.Label(ventana, text="Nombre:", anchor="w").grid(row=2, column=0, padx=20, pady=5, sticky="w")
    campoNombre = tk.Entry(ventana, width=30)
    campoNombre.grid(row=2, column=1, padx=10)

    tk.Label(ventana, text="Primer apellido:", anchor="w").grid(row=3, column=0, padx=20, pady=5, sticky="w")
    campoApellido1 = tk.Entry(ventana, width=30)
    campoApellido1.grid(row=3, column=1, padx=10)

    tk.Label(ventana, text="Segundo apellido:", anchor="w").grid(row=4, column=0, padx=20, pady=5, sticky="w")
    campoApellido2 = tk.Entry(ventana, width=30)
    campoApellido2.grid(row=4, column=1, padx=10)

    tk.Label(ventana, text="Fecha de nacimiento (DD/MM/AAAA):", anchor="w").grid(row=5, column=0, padx=20, pady=5, sticky="w")
    campoFecha = tk.Entry(ventana, width=30)
    campoFecha.grid(row=5, column=1, padx=10)

    tk.Label(ventana, text="Tipo de sangre:", anchor="w").grid(row=6, column=0, padx=20, pady=5, sticky="w")
    tipoSangreVar = tk.StringVar()
    tipoSangreVar.set(tiposDeSangre[0])
    cajaTipoSangre = tk.OptionMenu(ventana, tipoSangreVar, *tiposDeSangre)
    cajaTipoSangre.config(width=27)
    cajaTipoSangre.grid(row=6, column=1, padx=10)

    tk.Label(ventana, text="Sexo:", anchor="w").grid(row=7, column=0, padx=20, pady=5, sticky="w")
    sexoVar = tk.BooleanVar()
    sexoVar.set(True)
    tk.Radiobutton(ventana, text="Masculino", variable=sexoVar, value=True).grid(row=7, column=1, sticky="w", padx=10)
    tk.Radiobutton(ventana, text="Femenino", variable=sexoVar, value=False).grid(row=8, column=1, sticky="w", padx=10)

    tk.Label(ventana, text="Peso (kg):", anchor="w").grid(row=9, column=0, padx=20, pady=5, sticky="w")
    campoPeso = tk.Entry(ventana, width=30)
    campoPeso.grid(row=9, column=1, padx=10)

    tk.Label(ventana, text="Telefono (####-####):", anchor="w").grid(row=10, column=0, padx=20, pady=5, sticky="w")
    campoTelefono = tk.Entry(ventana, width=30)
    campoTelefono.grid(row=10, column=1, padx=10)

    tk.Label(ventana, text="Correo:", anchor="w").grid(row=11, column=0, padx=20, pady=5, sticky="w")
    campoCorreo = tk.Entry(ventana, width=30)
    campoCorreo.grid(row=11, column=1, padx=10)

    def limpiarCampos():
        """
        Funcionalidad: Limpia todos los campos del formulario a su estado inicial.
        Entradas: Ninguna.
        Salidas: Ninguna.
        """
        campoCedula.delete(0, tk.END)
        campoNombre.delete(0, tk.END)
        campoApellido1.delete(0, tk.END)
        campoApellido2.delete(0, tk.END)
        campoFecha.delete(0, tk.END)
        campoPeso.delete(0, tk.END)
        campoTelefono.delete(0, tk.END)
        campoCorreo.delete(0, tk.END)
        tipoSangreVar.set(tiposDeSangre[0])
        sexoVar.set(True)

    def registrarDonador():
        """
        Funcionalidad: Valida todos los campos y agrega el donador a la base de datos.
                       Muestra realimentacion completa al usuario tras el registro.
        Entradas: Ninguna. Lee los valores de los campos de la ventana.
        Salidas: Ninguna. Modifica la lista global baseDeDatos si todo es valido.
        """
        cedula    = campoCedula.get().strip()
        nombre    = campoNombre.get().strip()
        apellido1 = campoApellido1.get().strip()
        apellido2 = campoApellido2.get().strip()
        fecha     = campoFecha.get().strip()
        tipoSangre = tipoSangreVar.get()
        sexo      = sexoVar.get()
        peso      = campoPeso.get().strip()
        telefono  = campoTelefono.get().strip()
        correo    = campoCorreo.get().strip()

        if not validarCedula(cedula):
            messagebox.showerror("Error", "Cedula invalida. Formato: #-####-####, primer digito no puede ser 0.")
            return
        if nombre == "" or apellido1 == "" or apellido2 == "":
            messagebox.showerror("Error", "Nombre completo es requerido.")
            return
        if not validarFecha(fecha):
            messagebox.showerror("Error", "Fecha invalida. Formato: DD/MM/AAAA.")
            return
        if not validarPeso(peso):
            messagebox.showerror("Error", "Peso invalido. Debe ser mayor a 50 y menor a 120 kg.")
            return
        if not validarTelefono(telefono):
            messagebox.showerror("Error", "Telefono invalido. Formato: ####-####, primer digito no puede ser 0, 1, 3 ni 5.")
            return
        if not validarCorreo(correo):
            messagebox.showerror("Error", "Correo invalido.")
            return
        if cedulaYaExiste(cedula):
            messagebox.showerror("Error", f"La cedula {cedula} ya esta registrada.")
            return

        partesFecha = fecha.split("/")
        tuplaFecha = (int(partesFecha[0]), int(partesFecha[1]), int(partesFecha[2]))

        nuevoDonador = [
            [nombre, apellido1, apellido2],
            cedula,
            tiposDeSangre.index(tipoSangre),
            sexo,
            tuplaFecha,
            float(peso),
            correo,
            telefono,
            1,
            0
        ]
        baseDeDatos.append(nuevoDonador)
        guardarBaseDeDatos()

        numeroProvincia = obtenerProvinciaPorCedula(cedula)
        lugaresTexto = ", ".join(lugaresDonacion.get(numeroProvincia, ["No disponible"]))

        mensajeEdad = "Dado su fecha de nacimiento usted ya puede ser donador." if esMayorDeEdad(fecha) else "Dado su fecha de nacimiento usted aun no puede ser donador."

        if float(peso) <= 50:
            mensajePeso = "Usted debe pesar mas de 50 kgms para poder ser donador."
        elif float(peso) >= 120:
            mensajePeso = "Dado su sobre peso, no es posible donar sangre."
        else:
            mensajePeso = "Usted posee un peso adecuado, correcto para ser donador de sangre."

        mensajeFinal = (
            f"{mensajeEdad}\n\n"
            f"Dado que usted nacio en la provincia de: {nombreProvincias.get(numeroProvincia, 'Desconocida')}, "
            f"usted podria donar en: {lugaresTexto}.\n\n"
            f"{mensajePeso}\n\n"
            f"Dado su tipo de sangre {tipoSangre}: {obtenerInfoTipoDeSangre(tipoSangre)}"
        )

        if tipoSangre in ("A+", "A-"):
            mensajeFinal += "\n\nLe recomendamos ver: 'Particularidades de la sangre tipo A: Responde diferente al estres segun la ciencia.'"

        messagebox.showinfo("Donador registrado", mensajeFinal)
        limpiarCampos()

    marcoBotones = tk.Frame(ventana)
    marcoBotones.grid(row=12, column=0, columnspan=2, pady=15)
    tk.Button(marcoBotones, text="Registrar", width=12, bg="green", fg="white", command=registrarDonador).grid(row=0, column=0, padx=10)
    tk.Button(marcoBotones, text="Limpiar", width=12, command=limpiarCampos).grid(row=0, column=1, padx=10)
    tk.Button(marcoBotones, text="Regresar", width=12, bg="red", fg="white", command=ventana.destroy).grid(row=0, column=2, padx=10)


# =========================================================
# GENERAR DONADORES
# =========================================================

def generarCedulaAleatoria():
    """
    Funcionalidad: Genera un numero de cedula aleatorio con el formato #-####-####
                   donde el primer digito no puede ser 0.
    Entradas: Ninguna.
    Salidas:
        - cedula(str): Cedula generada en formato #-####-####.
    """
    provincia = random.randint(1, 7)
    tomo = random.randint(1000, 9999)
    asiento = random.randint(1000, 9999)
    return f"{provincia}-{tomo}-{asiento}"


def generarNombreAleatorio():
    """
    Funcionalidad: Genera un nombre completo aleatorio con nombres y apellidos predefinidos.
    Entradas: Ninguna.
    Salidas:
        - nombre(list): Lista con [nombre, apellido1, apellido2].
    """
    nombres = ["Carlos", "Maria", "Luis", "Ana", "Jose", "Laura",
               "Diego", "Sofia", "Andres", "Valeria", "Miguel", "Paula",
               "Fernando", "Daniela", "Ricardo", "Gabriela"]
    apellidos = ["Rodriguez", "Gonzalez", "Mora", "Jimenez", "Vargas",
                 "Castro", "Herrera", "Sanchez", "Ramirez", "Torres",
                 "Nunez", "Rojas", "Mendez", "Vega", "Soto", "Arias"]
    return [random.choice(nombres), random.choice(apellidos), random.choice(apellidos)]


def generarDonadores(ventanaPadre):
    """
    Funcionalidad: Abre una ventana para generar dinamicamente donadores con
                   datos aleatorios. Algunos seran activos y otros inactivos.
    Entradas:
        - ventanaPadre(tk.Tk): La ventana principal del programa.
    Salidas: Ninguna. Modifica la lista global baseDeDatos.
    """
    ventana = tk.Toplevel(ventanaPadre)
    ventana.title("Generar Donadores")
    ventana.geometry("500x500")
    ventana.resizable(False, False)

    tk.Label(ventana, text="Generar Donadores", font=("Arial", 14, "bold"), fg="red").pack(pady=15)
    tk.Label(ventana, text="Cantidad de donadores a generar:", font=("Arial", 11)).pack()

    campoCantidad = tk.Entry(ventana, width=15, font=("Arial", 11))
    campoCantidad.pack(pady=8)

    tk.Label(ventana, text="Resultado:", font=("Arial", 11)).pack()
    areaResultado = tk.Text(ventana, height=16, width=58, font=("Courier New", 9))
    areaResultado.pack(pady=5)

    def ejecutarGeneracion():
        """
        Funcionalidad: Lee la cantidad ingresada y genera los donadores dinamicamente.
        Entradas: Ninguna. Lee el valor del campo campoCantidad.
        Salidas: Ninguna. Modifica baseDeDatos y muestra resultados en pantalla.
        """
        areaResultado.delete("1.0", tk.END)
        cantidad = campoCantidad.get().strip()

        if not cantidad.isdigit() or int(cantidad) <= 0:
            messagebox.showerror("Error", "Debe ingresar un numero entero mayor a 0.")
            return

        cantidad = int(cantidad)
        generados = 0
        noValidos = 0

        for _ in range(cantidad):
            seraValido = random.random() > 0.3
            nombre = generarNombreAleatorio()
            cedula = generarCedulaAleatoria()

            intentos = 0
            while cedulaYaExiste(cedula) and intentos < 100:
                cedula = generarCedulaAleatoria()
                intentos += 1

            tipoSangreIndex = random.randint(0, len(tiposDeSangre) - 1)
            sexo = random.choice([True, False])

            if seraValido:
                año = random.randint(1960, 2006)
            else:
                año = random.randint(2010, 2020)

            mes = random.randint(1, 12)
            dia = random.randint(1, 28)
            tuplaFecha = (dia, mes, año)
            peso = round(random.uniform(55, 110) if seraValido else random.uniform(30, 49), 1)
            correo = f"{nombre[0].lower()}{random.randint(1,999)}@gmail.com"
            telefono = f"{random.randint(2,9)}{random.randint(100,999)}-{random.randint(1000,9999)}"
            estado = 1 if seraValido else 0
            justificacion = 0 if seraValido else random.randint(1, 7)

            if not seraValido:
                noValidos += 1

            baseDeDatos.append([nombre, cedula, tipoSangreIndex, sexo, tuplaFecha, float(peso), correo, telefono, estado, justificacion])
            generados += 1

            nombreCompleto = f"{nombre[0]} {nombre[1]} {nombre[2]}"
            estadoTexto = "ACTIVO  " if estado == 1 else f"INACTIVO (justif. {justificacion})"
            areaResultado.insert(tk.END, f"{cedula} | {nombreCompleto:<28} | {tiposDeSangre[tipoSangreIndex]:<3} | {estadoTexto}\n")

        guardarBaseDeDatos()
        areaResultado.insert(tk.END, f"\n{'='*55}\nTotal: {generados} | Activos: {generados - noValidos} | Inactivos: {noValidos}\n")

    marcoBotones = tk.Frame(ventana)
    marcoBotones.pack(pady=8)
    tk.Button(marcoBotones, text="Generar", width=15, bg="green", fg="white", command=ejecutarGeneracion).grid(row=0, column=0, padx=10)
    tk.Button(marcoBotones, text="Regresar", width=15, bg="red", fg="white", command=ventana.destroy).grid(row=0, column=1, padx=10)


# =========================================================
# ACTUALIZAR DONADOR
# =========================================================

def actualizarDonador(ventanaPadre):
    """
    Funcionalidad: Abre una ventana para buscar un donador por cedula y modificar
                   sus datos. La cedula es de solo lectura. Guarda si confirma.
    Entradas:
        - ventanaPadre(tk.Tk): La ventana principal del programa.
    Salidas: Ninguna. Modifica baseDeDatos y guarda en archivo si confirma.
    """
    ventana = tk.Toplevel(ventanaPadre)
    ventana.title("Actualizar Datos del Donador")
    ventana.geometry("520x620")
    ventana.resizable(False, False)

    tk.Label(ventana, text="Actualizar Datos del Donador", font=("Arial", 14, "bold"), fg="red").pack(pady=10)

    marcoBusqueda = tk.Frame(ventana)
    marcoBusqueda.pack(pady=5)
    tk.Label(marcoBusqueda, text="Cedula (#-####-####):", font=("Arial", 11)).grid(row=0, column=0, padx=10)
    campoCedula = tk.Entry(marcoBusqueda, width=20, font=("Arial", 11))
    campoCedula.grid(row=0, column=1, padx=5)
    tk.Button(marcoBusqueda, text="Buscar", width=10, bg="blue", fg="white", command=lambda: buscarYCargar()).grid(row=0, column=2, padx=5)

    marcoFormulario = tk.Frame(ventana)

    tk.Label(marcoFormulario, text="Nombre:", anchor="w").grid(row=0, column=0, padx=20, pady=4, sticky="w")
    campoNombre = tk.Entry(marcoFormulario, width=30)
    campoNombre.grid(row=0, column=1, padx=10)

    tk.Label(marcoFormulario, text="Primer apellido:", anchor="w").grid(row=1, column=0, padx=20, pady=4, sticky="w")
    campoApellido1 = tk.Entry(marcoFormulario, width=30)
    campoApellido1.grid(row=1, column=1, padx=10)

    tk.Label(marcoFormulario, text="Segundo apellido:", anchor="w").grid(row=2, column=0, padx=20, pady=4, sticky="w")
    campoApellido2 = tk.Entry(marcoFormulario, width=30)
    campoApellido2.grid(row=2, column=1, padx=10)

    tk.Label(marcoFormulario, text="Fecha de nacimiento (DD/MM/AAAA):", anchor="w").grid(row=3, column=0, padx=20, pady=4, sticky="w")
    campoFecha = tk.Entry(marcoFormulario, width=30)
    campoFecha.grid(row=3, column=1, padx=10)

    tk.Label(marcoFormulario, text="Tipo de sangre:", anchor="w").grid(row=4, column=0, padx=20, pady=4, sticky="w")
    tipoSangreVar = tk.StringVar()
    cajaTipoSangre = tk.OptionMenu(marcoFormulario, tipoSangreVar, *tiposDeSangre)
    cajaTipoSangre.config(width=27)
    cajaTipoSangre.grid(row=4, column=1, padx=10)

    tk.Label(marcoFormulario, text="Sexo:", anchor="w").grid(row=5, column=0, padx=20, pady=4, sticky="w")
    sexoVar = tk.BooleanVar()
    tk.Radiobutton(marcoFormulario, text="Masculino", variable=sexoVar, value=True).grid(row=5, column=1, sticky="w", padx=10)
    tk.Radiobutton(marcoFormulario, text="Femenino", variable=sexoVar, value=False).grid(row=6, column=1, sticky="w", padx=10)

    tk.Label(marcoFormulario, text="Peso (kg):", anchor="w").grid(row=7, column=0, padx=20, pady=4, sticky="w")
    campoPeso = tk.Entry(marcoFormulario, width=30)
    campoPeso.grid(row=7, column=1, padx=10)

    tk.Label(marcoFormulario, text="Telefono (####-####):", anchor="w").grid(row=8, column=0, padx=20, pady=4, sticky="w")
    campoTelefono = tk.Entry(marcoFormulario, width=30)
    campoTelefono.grid(row=8, column=1, padx=10)

    tk.Label(marcoFormulario, text="Correo:", anchor="w").grid(row=9, column=0, padx=20, pady=4, sticky="w")
    campoCorreo = tk.Entry(marcoFormulario, width=30)
    campoCorreo.grid(row=9, column=1, padx=10)

    indiceEncontrado = [-1]

    def buscarYCargar():
        """
        Funcionalidad: Busca el donador por cedula y carga sus datos en el formulario.
        Entradas: Ninguna. Lee el campo campoCedula.
        Salidas: Ninguna. Muestra el formulario con los datos si existe.
        """
        cedula = campoCedula.get().strip()
        if cedula == "":
            messagebox.showwarning("Aviso", "Debe ingresar un numero de cedula.")
            return

        indice = buscarDonadorPorCedula(cedula)
        if indice == -1:
            messagebox.showwarning("No encontrado", f"La persona con el numero de cedula: {cedula} no esta registrada en la base de datos del Banco de Sangre aun.")
            marcoFormulario.pack_forget()
            marcoBotones.pack_forget()
            return

        indiceEncontrado[0] = indice
        donador = baseDeDatos[indice]

        campoNombre.delete(0, tk.END)
        campoNombre.insert(0, donador[0][0])
        campoApellido1.delete(0, tk.END)
        campoApellido1.insert(0, donador[0][1])
        campoApellido2.delete(0, tk.END)
        campoApellido2.insert(0, donador[0][2])

        fecha = donador[4]
        campoFecha.delete(0, tk.END)
        campoFecha.insert(0, f"{fecha[0]:02d}/{fecha[1]:02d}/{fecha[2]}")

        tipoSangreVar.set(tiposDeSangre[donador[2]])
        sexoVar.set(donador[3])

        campoPeso.delete(0, tk.END)
        campoPeso.insert(0, str(donador[5]))
        campoTelefono.delete(0, tk.END)
        campoTelefono.insert(0, donador[7])
        campoCorreo.delete(0, tk.END)
        campoCorreo.insert(0, donador[6])

        marcoFormulario.pack(pady=5)
        marcoBotones.pack(pady=10)

    def confirmarActualizacion():
        """
        Funcionalidad: Valida los campos y guarda los cambios en la base de datos.
        Entradas: Ninguna. Lee los campos del formulario.
        Salidas: Ninguna. Modifica baseDeDatos y guarda en archivo si es valido.
        """
        nombre    = campoNombre.get().strip()
        apellido1 = campoApellido1.get().strip()
        apellido2 = campoApellido2.get().strip()
        fecha     = campoFecha.get().strip()
        tipoSangre = tipoSangreVar.get()
        sexo      = sexoVar.get()
        peso      = campoPeso.get().strip()
        telefono  = campoTelefono.get().strip()
        correo    = campoCorreo.get().strip()

        if nombre == "" or apellido1 == "" or apellido2 == "":
            messagebox.showerror("Error", "Nombre completo es requerido.")
            return
        if not validarFecha(fecha):
            messagebox.showerror("Error", "Fecha invalida.")
            return
        if not validarPeso(peso):
            messagebox.showerror("Error", "Peso invalido.")
            return
        if not validarTelefono(telefono):
            messagebox.showerror("Error", "Telefono invalido.")
            return
        if not validarCorreo(correo):
            messagebox.showerror("Error", "Correo invalido.")
            return

        partesFecha = fecha.split("/")
        tuplaFecha = (int(partesFecha[0]), int(partesFecha[1]), int(partesFecha[2]))
        indice = indiceEncontrado[0]

        baseDeDatos[indice][0] = [nombre, apellido1, apellido2]
        baseDeDatos[indice][2] = tiposDeSangre.index(tipoSangre)
        baseDeDatos[indice][3] = sexo
        baseDeDatos[indice][4] = tuplaFecha
        baseDeDatos[indice][5] = float(peso)
        baseDeDatos[indice][6] = correo
        baseDeDatos[indice][7] = telefono

        guardarBaseDeDatos()
        messagebox.showinfo("Exito", "Datos actualizados correctamente.")
        ventana.destroy()

    def rechazarActualizacion():
        """
        Funcionalidad: Cancela la actualizacion sin guardar cambios.
        Entradas: Ninguna.
        Salidas: Ninguna. Muestra mensaje y se mantiene en la ventana.
        """
        messagebox.showinfo("Cancelado", "Datos No actualizados.")

    marcoBotones = tk.Frame(ventana)
    tk.Button(marcoBotones, text="Confirmar", width=14, bg="green", fg="white", command=confirmarActualizacion).grid(row=0, column=0, padx=10)
    tk.Button(marcoBotones, text="Rechazar", width=14, bg="orange", command=rechazarActualizacion).grid(row=0, column=1, padx=10)
    tk.Button(marcoBotones, text="Regresar", width=14, bg="red", fg="white", command=ventana.destroy).grid(row=0, column=2, padx=10)


# =========================================================
# ELIMINAR DONADOR
# =========================================================

def eliminarDonador(ventanaPadre):
    """
    Funcionalidad: Abre una ventana para buscar un donador por cedula y marcarlo
                   como inactivo con una justificacion. No lo borra fisicamente.
    Entradas:
        - ventanaPadre(tk.Tk): La ventana principal del programa.
    Salidas: Ninguna. Modifica el estado del donador en baseDeDatos.
    """
    ventana = tk.Toplevel(ventanaPadre)
    ventana.title("Eliminar Donador")
    ventana.geometry("500x380")
    ventana.resizable(False, False)

    tk.Label(ventana, text="Eliminar Donador", font=("Arial", 14, "bold"), fg="red").pack(pady=15)

    marcoCedula = tk.Frame(ventana)
    marcoCedula.pack(pady=5)
    tk.Label(marcoCedula, text="Cedula (#-####-####):", font=("Arial", 11)).grid(row=0, column=0, padx=10)
    campoCedula = tk.Entry(marcoCedula, width=20, font=("Arial", 11))
    campoCedula.grid(row=0, column=1, padx=10)

    marcoInfo = tk.Frame(ventana)
    etiquetaNombre = tk.Label(marcoInfo, text="", font=("Arial", 11))
    etiquetaNombre.pack(pady=5)

    tk.Label(marcoInfo, text="Justificacion de eliminacion:", font=("Arial", 11)).pack()
    opcionesJustificacion = [f"{k} - {v[:50]}..." for k, v in justificaciones.items()]
    justificacionVar = tk.StringVar()
    justificacionVar.set(opcionesJustificacion[0])
    cajaJustificacion = tk.OptionMenu(marcoInfo, justificacionVar, *opcionesJustificacion)
    cajaJustificacion.config(width=50)
    cajaJustificacion.pack(pady=5)

    marcoBotonesConfirmar = tk.Frame(marcoInfo)
    marcoBotonesConfirmar.pack(pady=10)

    indiceEncontrado = [-1]

    def confirmarEliminacion():
        """
        Funcionalidad: Cambia el estado del donador a inactivo con la justificacion
                       seleccionada y guarda en memoria secundaria.
        Entradas: Ninguna.
        Salidas: Ninguna. Modifica baseDeDatos y guarda en baseDeDatos.pkl.
        """
        numeroJustificacion = int(justificacionVar.get().split(" - ")[0])
        baseDeDatos[indiceEncontrado[0]][8] = 0
        baseDeDatos[indiceEncontrado[0]][9] = numeroJustificacion
        guardarBaseDeDatos()
        messagebox.showinfo("Exito", "Donador eliminado satisfactoriamente.")
        ventana.destroy()

    def rechazarEliminacion():
        """
        Funcionalidad: Cancela la eliminacion y mantiene el donador activo.
        Entradas: Ninguna.
        Salidas: Ninguna. Muestra mensaje y se mantiene en la ventana.
        """
        messagebox.showinfo("Cancelado", "Donador NO eliminado.")
        marcoInfo.pack_forget()
        campoCedula.delete(0, tk.END)

    tk.Button(marcoBotonesConfirmar, text="Confirmar", width=15, bg="green", fg="white", command=confirmarEliminacion).grid(row=0, column=0, padx=10)
    tk.Button(marcoBotonesConfirmar, text="Cancelar", width=15, bg="orange", command=rechazarEliminacion).grid(row=0, column=1, padx=10)

    def buscarDonador():
        """
        Funcionalidad: Busca al donador por cedula y muestra el formulario de
                       justificacion si existe y esta activo.
        Entradas: Ninguna. Lee el campo campoCedula.
        Salidas: Ninguna. Muestra u oculta el marco de informacion.
        """
        cedula = campoCedula.get().strip()
        if cedula == "":
            messagebox.showwarning("Aviso", "Debe ingresar un numero de cedula.")
            return

        indice = buscarDonadorPorCedula(cedula)
        if indice == -1:
            messagebox.showwarning("No encontrado", f"La persona con el numero de cedula: {cedula} no esta registrada en la base de datos del Banco de Sangre aun.")
            marcoInfo.pack_forget()
            return

        if baseDeDatos[indice][8] == 0:
            messagebox.showwarning("Aviso", f"El donador con cedula {cedula} ya se encuentra inactivo.")
            return

        indiceEncontrado[0] = indice
        nombre = baseDeDatos[indice][0]
        nombreCompleto = f"{nombre[0]} {nombre[1]} {nombre[2]}"
        tipoSangre = tiposDeSangre[baseDeDatos[indice][2]]
        etiquetaNombre.config(text=f"Donador: {nombreCompleto} | Tipo de sangre: {tipoSangre}")
        marcoInfo.pack(pady=10)

    tk.Button(ventana, text="Buscar", width=15, bg="blue", fg="white", command=buscarDonador).pack(pady=8)
    tk.Button(ventana, text="Regresar", width=15, bg="red", fg="white", command=ventana.destroy).pack(pady=5)


# =========================================================
# INSERTAR LUGAR DE DONACION
# =========================================================

def insertarLugarDonacion(ventanaPadre):
    """
    Funcionalidad: Abre una ventana para insertar un nuevo lugar de donacion
                   en una provincia seleccionada. Verifica que no este duplicado.
    Entradas:
        - ventanaPadre(tk.Tk): La ventana principal del programa.
    Salidas: Ninguna. Modifica el diccionario global lugaresDonacion.
    """
    ventana = tk.Toplevel(ventanaPadre)
    ventana.title("Insertar Lugar de Donacion")
    ventana.geometry("450x350")
    ventana.resizable(False, False)

    tk.Label(ventana, text="Insertar Lugar de Donacion", font=("Arial", 14, "bold"), fg="red").pack(pady=15)
    tk.Label(ventana, text="Provincia:", font=("Arial", 11)).pack()

    opcionesProvincias = [f"{k} - {v}" for k, v in nombreProvincias.items()]
    provinciaSeleccionada = tk.StringVar()
    provinciaSeleccionada.set(opcionesProvincias[0])
    cajaProvincias = tk.OptionMenu(ventana, provinciaSeleccionada, *opcionesProvincias)
    cajaProvincias.config(width=30)
    cajaProvincias.pack(pady=5)

    tk.Label(ventana, text="Nuevo lugar de donacion:", font=("Arial", 11)).pack(pady=5)
    areaTexto = tk.Text(ventana, height=4, width=40, font=("Arial", 10))
    areaTexto.pack(pady=5)

    def confirmarInsercion():
        """
        Funcionalidad: Valida y ejecuta la insercion del nuevo lugar en el diccionario.
        Entradas: Ninguna. Lee los campos de la ventana.
        Salidas: Ninguna. Modifica lugaresDonacion si la insercion es valida.
        """
        nuevoLugar = areaTexto.get("1.0", tk.END).strip()
        if nuevoLugar == "":
            messagebox.showwarning("Aviso", "Debe ingresar un lugar de donacion.")
            return

        numeroProvincia = int(provinciaSeleccionada.get().split(" - ")[0])
        for lugar in lugaresDonacion[numeroProvincia]:
            if lugar.lower() == nuevoLugar.lower():
                messagebox.showwarning("Aviso", f"El lugar '{nuevoLugar}' ya esta registrado en {nombreProvincias[numeroProvincia]}.")
                return

        lugaresDonacion[numeroProvincia].append(nuevoLugar)
        messagebox.showinfo("Exito", f"Lugar '{nuevoLugar}' agregado exitosamente en {nombreProvincias[numeroProvincia]}.")
        areaTexto.delete("1.0", tk.END)

    marcosBotones = tk.Frame(ventana)
    marcosBotones.pack(pady=10)
    tk.Button(marcosBotones, text="Insertar", width=15, bg="green", fg="white", command=confirmarInsercion).grid(row=0, column=0, padx=10)
    tk.Button(marcosBotones, text="Salir", width=15, bg="red", fg="white", command=ventana.destroy).grid(row=0, column=1, padx=10)


# =========================================================
# REPORTES
# =========================================================

def abrirMenuReportes(ventanaPadre):
    """
    Funcionalidad: Abre la ventana del menu de reportes con todos los botones
                   disponibles para generar los distintos reportes HTML.
    Entradas:
        - ventanaPadre(tk.Tk): La ventana principal del programa.
    Salidas: Ninguna. Abre la ventana de reportes.
    """
    ventana = tk.Toplevel(ventanaPadre)
    ventana.title("Reportes")
    ventana.geometry("400x560")
    ventana.resizable(False, False)

    tk.Label(ventana, text="Reportes", font=("Arial", 14, "bold"), fg="red").pack(pady=15)

    botones = [
        ("1. Donantes por provincia",        lambda: reporteDonanteProvincia(ventana)),
        ("2. Por rango de edad",             lambda: reporteRangoEdad(ventana)),
        ("3. Por tipo de sangre y provincia", lambda: reporteTipoSangreProvincia(ventana)),
        ("4. Lista completa de donadores",   lambda: reporteListaCompleta(ventana)),
        ("5. Mujeres donantes O-",           lambda: reporteMujeresONegativo(ventana)),
        ("6. A quien puede donar",           lambda: reporteAQuienPuedeDonar(ventana)),
        ("7. De quien puede recibir",        lambda: reporteDeQuienPuedeRecibir(ventana)),
        ("8. Donantes no activos",           lambda: reporteDonantesNoActivos(ventana)),
        ("9. Lugares de donacion",           lambda: reporteLugaresDonacion(ventana)),
    ]

    for texto, comando in botones:
        tk.Button(ventana, text=texto, width=35, command=comando).pack(pady=4)

    tk.Button(ventana, text="Regresar", width=35, bg="red", fg="white", command=ventana.destroy).pack(pady=10)


def reporteDonanteProvincia(ventanaPadre):
    """
    Funcionalidad: Genera un reporte HTML con los donantes activos de una
                   provincia seleccionada, ordenados por nombre completo.
    Entradas:
        - ventanaPadre(tk.Toplevel): La ventana de reportes.
    Salidas: Ninguna. Crea un archivo HTML con el reporte.
    """
    ventana = tk.Toplevel(ventanaPadre)
    ventana.title("Donantes por Provincia")
    ventana.geometry("400x250")
    ventana.resizable(False, False)

    tk.Label(ventana, text="Donantes por Provincia", font=("Arial", 13, "bold"), fg="red").pack(pady=15)
    tk.Label(ventana, text="Seleccione la provincia:", font=("Arial", 11)).pack()

    opcionesProvincias = [f"{k} - {v}" for k, v in nombreProvincias.items()]
    provinciaVar = tk.StringVar()
    provinciaVar.set(opcionesProvincias[0])
    cajaProvincias = tk.OptionMenu(ventana, provinciaVar, *opcionesProvincias)
    cajaProvincias.config(width=30)
    cajaProvincias.pack(pady=8)

    def generar():
        """
        Funcionalidad: Filtra, ordena y genera el HTML con donantes activos
                       de la provincia seleccionada.
        Entradas: Ninguna. Lee la provincia seleccionada.
        Salidas: Ninguna. Crea el archivo HTML del reporte.
        """
        numeroProvincia = int(provinciaVar.get().split(" - ")[0])
        nombreProv = nombreProvincias[numeroProvincia]

        lista = [d for d in baseDeDatos if int(d[1][0]) == numeroProvincia and d[8] == 1]
        lista = ordenarPorNombre(lista)

        filas = []
        for d in lista:
            nombreCompleto = f"{d[0][0]} {d[0][1]} {d[0][2]}"
            fecha = d[4]
            filas.append([d[1], nombreCompleto, f"{fecha[0]:02d}/{fecha[1]:02d}/{fecha[2]}", d[7], d[6]])

        ahora = datetime.now()
        fechaHora = ahora.strftime("%d/%m/%Y %H:%M:%S")
        nombreArchivo = f"reporte_provincia_{numeroProvincia}_{ahora.strftime('%d-%m-%Y_%H-%M-%S')}.html"
        html = generarHtmlBase(f"Donantes Activos - {nombreProv}", fechaHora, ["Cedula", "Nombre Completo", "Fecha Nacimiento", "Telefono", "Correo"], filas)
        guardarHtml(html, nombreArchivo)

    marcoBotones = tk.Frame(ventana)
    marcoBotones.pack(pady=12)
    tk.Button(marcoBotones, text="Generar reporte", width=16, bg="green", fg="white", command=generar).grid(row=0, column=0, padx=10)
    tk.Button(marcoBotones, text="Regresar", width=16, bg="red", fg="white", command=ventana.destroy).grid(row=0, column=1, padx=10)


def reporteRangoEdad(ventanaPadre):
    """
    Funcionalidad: Genera un reporte HTML con donantes activos dentro de un
                   rango de edad. La edad debe estar entre 18 y 65 años.
    Entradas:
        - ventanaPadre(tk.Toplevel): La ventana de reportes.
    Salidas: Ninguna. Crea un archivo HTML con el reporte.
    """
    ventana = tk.Toplevel(ventanaPadre)
    ventana.title("Por Rango de Edad")
    ventana.geometry("400x280")
    ventana.resizable(False, False)

    tk.Label(ventana, text="Por Rango de Edad", font=("Arial", 13, "bold"), fg="red").pack(pady=15)

    marcoEdades = tk.Frame(ventana)
    marcoEdades.pack(pady=5)

    tk.Label(marcoEdades, text="Edad inicial:", font=("Arial", 11)).grid(row=0, column=0, padx=10, pady=5)
    campoEdadInicial = tk.Entry(marcoEdades, width=10, font=("Arial", 11))
    campoEdadInicial.grid(row=0, column=1, padx=10)

    tk.Label(marcoEdades, text="Edad final:", font=("Arial", 11)).grid(row=1, column=0, padx=10, pady=5)
    campoEdadFinal = tk.Entry(marcoEdades, width=10, font=("Arial", 11), state=tk.DISABLED)
    campoEdadFinal.grid(row=1, column=1, padx=10)

    def validarEdadInicial(event):
        """
        Funcionalidad: Habilita el campo de edad final solo si la edad inicial es valida.
        Entradas:
            - event: Evento de tkinter (tecla presionada).
        Salidas: Ninguna. Habilita o deshabilita campoEdadFinal.
        """
        valor = campoEdadInicial.get().strip()
        if valor.isdigit() and 18 <= int(valor) <= 65:
            campoEdadFinal.config(state=tk.NORMAL)
        else:
            campoEdadFinal.config(state=tk.DISABLED)
            campoEdadFinal.delete(0, tk.END)

    campoEdadInicial.bind("<KeyRelease>", validarEdadInicial)

    def generar():
        """
        Funcionalidad: Filtra donantes activos dentro del rango de edad indicado
                       y genera el reporte HTML.
        Entradas: Ninguna. Lee los campos de edad.
        Salidas: Ninguna. Crea el archivo HTML del reporte.
        """
        edadInicialStr = campoEdadInicial.get().strip()
        edadFinalStr = campoEdadFinal.get().strip()

        if not edadInicialStr.isdigit() or not (18 <= int(edadInicialStr) <= 65):
            messagebox.showerror("Error", "Edad inicial invalida. Debe ser entre 18 y 65.")
            return

        edadInicial = int(edadInicialStr)
        edadFinal = int(edadFinalStr) if edadFinalStr.isdigit() and 18 <= int(edadFinalStr) <= 65 else edadInicial

        lista = []
        for d in baseDeDatos:
            if d[8] == 1:
                edad = calcularEdad(d[4])
                if edadInicial <= edad <= edadFinal:
                    lista.append(d)

        lista = ordenarPorNombre(lista)
        filas = []
        for d in lista:
            nombreCompleto = f"{d[0][0]} {d[0][1]} {d[0][2]}"
            fecha = d[4]
            filas.append([d[1], nombreCompleto, f"{fecha[0]:02d}/{fecha[1]:02d}/{fecha[2]}", d[7], d[6]])

        ahora = datetime.now()
        fechaHora = ahora.strftime("%d/%m/%Y %H:%M:%S")
        nombreArchivo = f"reporte_edad_{edadInicial}_{edadFinal}_{ahora.strftime('%d-%m-%Y_%H-%M-%S')}.html"
        html = generarHtmlBase(f"Donantes por Rango de Edad ({edadInicial} - {edadFinal} años)", fechaHora, ["Cedula", "Nombre Completo", "Fecha Nacimiento", "Telefono", "Correo"], filas)
        guardarHtml(html, nombreArchivo)

    marcoBotones = tk.Frame(ventana)
    marcoBotones.pack(pady=12)
    tk.Button(marcoBotones, text="Generar reporte", width=16, bg="green", fg="white", command=generar).grid(row=0, column=0, padx=10)
    tk.Button(marcoBotones, text="Regresar", width=16, bg="red", fg="white", command=ventana.destroy).grid(row=0, column=1, padx=10)


def reporteTipoSangreProvincia(ventanaPadre):
    """
    Funcionalidad: Genera un reporte HTML con donantes activos de un tipo
                   de sangre especifico en una provincia seleccionada.
    Entradas:
        - ventanaPadre(tk.Toplevel): La ventana de reportes.
    Salidas: Ninguna. Crea un archivo HTML con el reporte.
    """
    ventana = tk.Toplevel(ventanaPadre)
    ventana.title("Por Tipo de Sangre y Provincia")
    ventana.geometry("400x280")
    ventana.resizable(False, False)

    tk.Label(ventana, text="Por Tipo de Sangre y Provincia", font=("Arial", 13, "bold"), fg="red").pack(pady=15)

    tk.Label(ventana, text="Tipo de sangre:", font=("Arial", 11)).pack()
    tipoSangreVar = tk.StringVar()
    tipoSangreVar.set(tiposDeSangre[0])
    tk.OptionMenu(ventana, tipoSangreVar, *tiposDeSangre).pack(pady=5)

    tk.Label(ventana, text="Provincia:", font=("Arial", 11)).pack()
    opcionesProvincias = [f"{k} - {v}" for k, v in nombreProvincias.items()]
    provinciaVar = tk.StringVar()
    provinciaVar.set(opcionesProvincias[0])
    tk.OptionMenu(ventana, provinciaVar, *opcionesProvincias).pack(pady=5)

    def generar():
        """
        Funcionalidad: Filtra donantes activos del tipo de sangre y provincia
                       indicados y genera el reporte HTML.
        Entradas: Ninguna. Lee los campos de tipo de sangre y provincia.
        Salidas: Ninguna. Crea el archivo HTML del reporte.
        """
        tipoSangre = tipoSangreVar.get()
        numeroProvincia = int(provinciaVar.get().split(" - ")[0])
        tipoIndex = tiposDeSangre.index(tipoSangre)

        lista = [d for d in baseDeDatos if d[8] == 1 and d[2] == tipoIndex and int(d[1][0]) == numeroProvincia]
        lista = ordenarPorNombre(lista)

        filas = []
        for d in lista:
            nombreCompleto = f"{d[0][0]} {d[0][1]} {d[0][2]}"
            fecha = d[4]
            filas.append([d[1], nombreCompleto, f"{fecha[0]:02d}/{fecha[1]:02d}/{fecha[2]}", d[7], d[6]])

        ahora = datetime.now()
        fechaHora = ahora.strftime("%d/%m/%Y %H:%M:%S")
        nombreArchivo = f"reporte_tipo_{tipoSangre}_{numeroProvincia}_{ahora.strftime('%d-%m-%Y_%H-%M-%S')}.html"
        html = generarHtmlBase(f"Donantes {tipoSangre} - {nombreProvincias[numeroProvincia]}", fechaHora, ["Cedula", "Nombre Completo", "Fecha Nacimiento", "Telefono", "Correo"], filas)
        guardarHtml(html, nombreArchivo)

    marcoBotones = tk.Frame(ventana)
    marcoBotones.pack(pady=12)
    tk.Button(marcoBotones, text="Generar reporte", width=16, bg="green", fg="white", command=generar).grid(row=0, column=0, padx=10)
    tk.Button(marcoBotones, text="Regresar", width=16, bg="red", fg="white", command=ventana.destroy).grid(row=0, column=1, padx=10)


def reporteListaCompleta(ventanaPadre):
    """
    Funcionalidad: Genera un reporte HTML con todos los donantes activos
                   ordenados por provincia ascendentemente.
    Entradas:
        - ventanaPadre(tk.Toplevel): La ventana de reportes.
    Salidas: Ninguna. Crea un archivo HTML con el reporte.
    """
    lista = [d for d in baseDeDatos if d[8] == 1]
    lista = ordenarPorProvincia(lista)

    filas = []
    for d in lista:
        nombreCompleto = f"{d[0][0]} {d[0][1]} {d[0][2]}"
        fecha = d[4]
        sexoTexto = "Masculino" if d[3] else "Femenino"
        filas.append([d[1], nombreCompleto, tiposDeSangre[d[2]], f"{fecha[0]:02d}/{fecha[1]:02d}/{fecha[2]}", str(d[5]), sexoTexto, d[7], d[6]])

    ahora = datetime.now()
    fechaHora = ahora.strftime("%d/%m/%Y %H:%M:%S")
    nombreArchivo = f"reporte_lista_completa_{ahora.strftime('%d-%m-%Y_%H-%M-%S')}.html"
    html = generarHtmlBase("Lista Completa de Donadores", fechaHora, ["Cedula", "Nombre Completo", "Tipo Sangre", "Fecha Nacimiento", "Peso", "Sexo", "Telefono", "Correo"], filas)
    guardarHtml(html, nombreArchivo)


def reporteMujeresONegativo(ventanaPadre):
    """
    Funcionalidad: Genera un reporte HTML con mujeres donantes activas de tipo
                   O- menores de 45 años, ordenadas por edad.
    Entradas:
        - ventanaPadre(tk.Toplevel): La ventana de reportes.
    Salidas: Ninguna. Crea un archivo HTML con el reporte.
    """
    tipoIndex = tiposDeSangre.index("O-")
    lista = []
    for d in baseDeDatos:
        if d[8] == 1 and d[3] == False and d[2] == tipoIndex:
            edad = calcularEdad(d[4])
            if edad < 45:
                lista.append(d)

    lista = ordenarPorEdad(lista)

    filas = []
    for d in lista:
        nombreCompleto = f"{d[0][0]} {d[0][1]} {d[0][2]}"
        fecha = d[4]
        filas.append([d[1], nombreCompleto, f"{fecha[0]:02d}/{fecha[1]:02d}/{fecha[2]}", d[7], d[6]])

    ahora = datetime.now()
    fechaHora = ahora.strftime("%d/%m/%Y %H:%M:%S")
    nombreArchivo = f"reporte_mujeres_oneg_{ahora.strftime('%d-%m-%Y_%H-%M-%S')}.html"
    html = generarHtmlBase("Mujeres Donantes O- Menores de 45 años", fechaHora, ["Cedula", "Nombre Completo", "Fecha Nacimiento", "Telefono", "Correo"], filas)
    guardarHtml(html, nombreArchivo)


def reporteAQuienPuedeDonar(ventanaPadre):
    """
    Funcionalidad: Genera un reporte HTML con donantes activos que pueden donar
                   a un tipo de sangre dado, agrupados por provincia ascendentemente.
    Entradas:
        - ventanaPadre(tk.Toplevel): La ventana de reportes.
    Salidas: Ninguna. Crea un archivo HTML con el reporte.
    """
    ventana = tk.Toplevel(ventanaPadre)
    ventana.title("A quien puede donar")
    ventana.geometry("400x220")
    ventana.resizable(False, False)

    tk.Label(ventana, text="A quien puede donar", font=("Arial", 13, "bold"), fg="red").pack(pady=15)
    tk.Label(ventana, text="Tipo de sangre:", font=("Arial", 11)).pack()
    tipoSangreVar = tk.StringVar()
    tipoSangreVar.set(tiposDeSangre[0])
    tk.OptionMenu(ventana, tipoSangreVar, *tiposDeSangre).pack(pady=5)

    def generar():
        """
        Funcionalidad: Filtra donantes activos que pueden donar al tipo de sangre
                       indicado y genera el reporte agrupado por provincia ascendente.
        Entradas: Ninguna. Lee el tipo de sangre seleccionado.
        Salidas: Ninguna. Crea el archivo HTML del reporte.
        """
        tipoSangre = tipoSangreVar.get()
        tiposQueReciben = compatibilidadDonar[tipoSangre]

        lista = []
        for d in baseDeDatos:
            if d[8] == 1 and tiposDeSangre[d[2]] in tiposQueReciben:
                lista.append(d)

        lista = ordenarPorProvincia(lista)
        filas = []
        for d in lista:
            nombreCompleto = f"{d[0][0]} {d[0][1]} {d[0][2]}"
            filas.append([d[1], nombreCompleto, tiposDeSangre[d[2]], d[7], d[6]])

        ahora = datetime.now()
        fechaHora = ahora.strftime("%d/%m/%Y %H:%M:%S")
        nombreArchivo = f"reporte_donar_a_{tipoSangre}_{ahora.strftime('%d-%m-%Y_%H-%M-%S')}.html"
        html = generarHtmlBase(f"Donantes que pueden donar a {tipoSangre}", fechaHora, ["Cedula", "Nombre Completo", "Tipo Sangre", "Telefono", "Correo"], filas)
        guardarHtml(html, nombreArchivo)

    marcoBotones = tk.Frame(ventana)
    marcoBotones.pack(pady=12)
    tk.Button(marcoBotones, text="Generar reporte", width=16, bg="green", fg="white", command=generar).grid(row=0, column=0, padx=10)
    tk.Button(marcoBotones, text="Regresar", width=16, bg="red", fg="white", command=ventana.destroy).grid(row=0, column=1, padx=10)


def reporteDeQuienPuedeRecibir(ventanaPadre):
    """
    Funcionalidad: Genera un reporte HTML con donantes activos de los tipos
                   compatibles para donar a un tipo dado, agrupados por provincia
                   descendentemente.
    Entradas:
        - ventanaPadre(tk.Toplevel): La ventana de reportes.
    Salidas: Ninguna. Crea un archivo HTML con el reporte.
    """
    ventana = tk.Toplevel(ventanaPadre)
    ventana.title("De quien puede recibir")
    ventana.geometry("400x220")
    ventana.resizable(False, False)

    tk.Label(ventana, text="De quien puede recibir", font=("Arial", 13, "bold"), fg="red").pack(pady=15)
    tk.Label(ventana, text="Tipo de sangre:", font=("Arial", 11)).pack()
    tipoSangreVar = tk.StringVar()
    tipoSangreVar.set(tiposDeSangre[0])
    tk.OptionMenu(ventana, tipoSangreVar, *tiposDeSangre).pack(pady=5)

    def generar():
        """
        Funcionalidad: Filtra donantes activos que pueden donar al tipo de sangre
                       indicado y genera el reporte agrupado por provincia descendente.
        Entradas: Ninguna. Lee el tipo de sangre seleccionado.
        Salidas: Ninguna. Crea el archivo HTML del reporte.
        """
        tipoSangre = tipoSangreVar.get()
        tiposCompatibles = compatibilidadRecibir[tipoSangre]

        lista = []
        for d in baseDeDatos:
            if d[8] == 1 and tiposDeSangre[d[2]] in tiposCompatibles:
                lista.append(d)

        lista = ordenarPorProvincia(lista, descendente=True)
        filas = []
        for d in lista:
            nombreCompleto = f"{d[0][0]} {d[0][1]} {d[0][2]}"
            filas.append([d[1], nombreCompleto, tiposDeSangre[d[2]], d[7], d[6]])

        ahora = datetime.now()
        fechaHora = ahora.strftime("%d/%m/%Y %H:%M:%S")
        nombreArchivo = f"reporte_recibir_de_{tipoSangre}_{ahora.strftime('%d-%m-%Y_%H-%M-%S')}.html"
        html = generarHtmlBase(f"Tipos que pueden donar a {tipoSangre}", fechaHora, ["Cedula", "Nombre Completo", "Tipo Sangre", "Telefono", "Correo"], filas)
        guardarHtml(html, nombreArchivo)

    marcoBotones = tk.Frame(ventana)
    marcoBotones.pack(pady=12)
    tk.Button(marcoBotones, text="Generar reporte", width=16, bg="green", fg="white", command=generar).grid(row=0, column=0, padx=10)
    tk.Button(marcoBotones, text="Regresar", width=16, bg="red", fg="white", command=ventana.destroy).grid(row=0, column=1, padx=10)


def reporteDonantesNoActivos(ventanaPadre):
    """
    Funcionalidad: Genera un reporte HTML con todos los donantes inactivos,
                   mostrando la justificacion completa de cada uno.
    Entradas:
        - ventanaPadre(tk.Toplevel): La ventana de reportes.
    Salidas: Ninguna. Crea un archivo HTML con el reporte.
    """
    lista = [d for d in baseDeDatos if d[8] == 0]

    filas = []
    for d in lista:
        nombreCompleto = f"{d[0][0]} {d[0][1]} {d[0][2]}"
        fecha = d[4]
        sexoTexto = "Masculino" if d[3] else "Femenino"
        justificacionTexto = justificaciones.get(d[9], "Sin justificacion")
        filas.append([justificacionTexto, d[1], nombreCompleto, tiposDeSangre[d[2]], f"{fecha[0]:02d}/{fecha[1]:02d}/{fecha[2]}", str(d[5]), sexoTexto, d[7], d[6]])

    ahora = datetime.now()
    fechaHora = ahora.strftime("%d/%m/%Y %H:%M:%S")
    nombreArchivo = f"reporte_inactivos_{ahora.strftime('%d-%m-%Y_%H-%M-%S')}.html"
    html = generarHtmlBase("Donantes No Activos", fechaHora, ["Justificacion", "Cedula", "Nombre Completo", "Tipo Sangre", "Fecha Nacimiento", "Peso", "Sexo", "Telefono", "Correo"], filas)
    guardarHtml(html, nombreArchivo)


def reporteLugaresDonacion(ventanaPadre):
    """
    Funcionalidad: Genera un reporte HTML con todas las provincias ordenadas
                   ascendentemente, la cantidad de donadores registrados en cada
                   una y los recintos disponibles para donar.
    Entradas:
        - ventanaPadre(tk.Toplevel): La ventana de reportes.
    Salidas: Ninguna. Crea un archivo HTML con el reporte.
    """
    filas = []
    for numProv in sorted(nombreProvincias.keys()):
        cantidad = 0
        for d in baseDeDatos:
            if int(d[1][0]) == numProv:
                cantidad += 1
        recintos = ", ".join(lugaresDonacion.get(numProv, []))
        filas.append([nombreProvincias[numProv], str(cantidad), recintos])

    ahora = datetime.now()
    fechaHora = ahora.strftime("%d/%m/%Y %H:%M:%S")
    nombreArchivo = f"reporte_lugares_{ahora.strftime('%d-%m-%Y_%H-%M-%S')}.html"
    html = generarHtmlBase("Lugares de Donacion por Provincia", fechaHora, ["Provincia", "Cantidad de Donadores", "Recintos de Recaudacion"], filas)
    guardarHtml(html, nombreArchivo)


# =========================================================
# MENU PRINCIPAL
# =========================================================

def abrirVentanaMenuPrincipal():
    """
    Funcionalidad: Crea y muestra la ventana principal del programa con los 7 botones
                   del menu. Si hay base de datos activa todos los botones, si no
                   solo activa los botones 1, 2, 5 y 7.
    Entradas: Ninguna.
    Salidas: Ninguna. Abre la ventana principal del programa.
    """
    hayBaseDeDatos = cargarBaseDeDatos()

    ventana = tk.Tk()
    ventana.title("Sistema de Banco de Sangre")
    ventana.geometry("400x500")
    ventana.resizable(False, False)

    tk.Label(ventana, text="Banco de Sangre\nSistema de Informacion", font=("Arial", 16, "bold"), fg="red").pack(pady=20)

    estadoBotones = tk.NORMAL if hayBaseDeDatos else tk.DISABLED

    tk.Button(ventana, text="1. Insertar donador", width=30, command=lambda: insertarDonador(ventana)).pack(pady=5)
    tk.Button(ventana, text="2. Generar donadores", width=30, command=lambda: generarDonadores(ventana)).pack(pady=5)
    tk.Button(ventana, text="3. Actualizar datos del donador", width=30, state=estadoBotones, command=lambda: actualizarDonador(ventana)).pack(pady=5)
    tk.Button(ventana, text="4. Eliminar donador", width=30, state=estadoBotones, command=lambda: eliminarDonador(ventana)).pack(pady=5)
    tk.Button(ventana, text="5. Insertar lugar de donacion", width=30, command=lambda: insertarLugarDonacion(ventana)).pack(pady=5)
    tk.Button(ventana, text="6. Reportes", width=30, state=estadoBotones, command=lambda: abrirMenuReportes(ventana)).pack(pady=5)
    tk.Button(ventana, text="7. Salir", width=30, fg="white", bg="red", command=lambda: salir(ventana)).pack(pady=5)

    if not hayBaseDeDatos:
        tk.Label(ventana, text="* Sin base de datos: solo opciones 1, 2, 5 y 7 disponibles.", font=("Arial", 8), fg="gray").pack(pady=5)

    ventana.mainloop()


def salir(ventana):
    """
    Funcionalidad: Muestra el mensaje de despedida y cierra la aplicacion.
    Entradas:
        - ventana(tk.Tk): La ventana principal del programa que se va a cerrar.
    Salidas: Ninguna. Cierra la ventana y termina el programa.
    """
    messagebox.showinfo("Hasta luego", "Donar sangre, es donar vida")
    ventana.destroy()


# =========================================================
# Punto de entrada del programa
abrirVentanaMenuPrincipal()
