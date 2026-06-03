# Elaborado por: Alejandro Madrigal y Brandon Meza
# Fecha de creacion: 27/05/2026
# Ultima modificacion: 30/05/2026
# Version de Python: 3.11

import tkinter as tk
from tkinter import messagebox
import pickle
import re
import random
from datetime import date
# =========================================================
# Tupla global con los tipos de sangre posibles
tiposDeSangre = ("O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-")

# Lista global que funciona como matriz para guardar los donadores
# Formato de cada donador:
# [[nombre, apellido1, apellido2], cedula, tipoSangre, sexo, (dia, mes, año), peso, correo, telefono, estado, justificacion]
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

# Diccionario global con las provincias
# Clave = numero de provincia, Valor = Provincia
nombreProvincias = {
    1: "San Jose",
    2: "Alajuela",
    3: "Cartago",
    4: "Heredia",
    5: "Guanacaste",
    6: "Puntarenas",
    7: "Limon"
}
# Diccionario con las justificaciones de GEMINI 
justificaciones = {
    1: "Enfermedades Infecciosas/Cronicas: Portador de VIH, Hepatitis B o C, sifilis, tuberculosis, diabetes insulinodependiente o afecciones graves de corazon, rinon o pulmon.",
    2: "Conductas de Riesgo: Nueva pareja sexual o mas de una pareja sexual en los ultimos 3 meses, o relaciones sexuales por dinero o drogas.",
    3: "Factores de Salud Fisica: Hemoglobina o hematocrito bajo o alto, presion arterial inestable, fiebre o infecciones recientes.",
    4: "Procedimientos Medicos: Ha recibido transfusiones, trasplantes, cirugias mayores, tatuajes, piercing o endoscopias recientes.",
    5: "Uso de Medicamentos: Consumo de farmacos inyectables sin receta o ciertos medicamentos restringidos.",
    6: "Estilo de Vida y Viajes: Uso de drogas recreativas, consumo de alcohol en las ultimas 24 horas, o viajes recientes a zonas endemicas de malaria o dengue.",
    7: "Situaciones Especificas: Embarazo, lactancia o menstruacion activa al momento de la donacion."
}
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




#Funciones principales del programa:
#=======================================================================================================
    #Validaciones y Datos del usuario
    
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


#=======================================================================================================
    #INSERTAR DONADOR

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

    tk.Label(
        ventana,
        text="Insertar Donador",
        font=("Arial", 14, "bold"),
        fg="red"
    ).grid(row=0, column=0, columnspan=2, pady=10)

    # Campos del formulario
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
    sexoVar.set(True)  # Masculino por omision
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
        Funcionalidad: Limpia todos los campos del formulario y los deja en su
                       estado inicial.
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
        Funcionalidad: Valida todos los campos del formulario y si son correctos
                       agrega el donador a la base de datos. Muestra realimentacion
                       al usuario sobre su elegibilidad para donar.
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

        # Validaciones
        if not validarCedula(cedula):
            messagebox.showerror("Error", "Cedula invalida. Formato: #-####-####, primer digito no puede ser 0.")
            ventana.lift()
            return
        if nombre == "" or apellido1 == "" or apellido2 == "":
            messagebox.showerror("Error", "Nombre completo es requerido.")
            ventana.lift()
            return
        if not validarFecha(fecha):
            messagebox.showerror("Error", "Fecha invalida. Formato: DD/MM/AAAA.")
            ventana.lift()
            return
        if not validarPeso(peso):
            messagebox.showerror("Error", "Peso invalido. Debe ser mayor a 50 y menor a 120 kg.")
            ventana.lift()
            return
        if not validarTelefono(telefono):
            messagebox.showerror("Error", "Telefono invalido. Formato: ####-####, primer digito no puede ser 0, 1, 3 ni 5.")
            ventana.lift()
            return
        if not validarCorreo(correo):
            messagebox.showerror("Error", "Correo invalido.")
            ventana.lift()
            return

        # Verifica si la cedula ya esta registrada
        for donador in baseDeDatos:
            if donador[1] == cedula:
                messagebox.showerror("Error", f"La cedula {cedula} ya esta registrada.")
                ventana.lift()
                return

        # Arma la tupla de fecha y el registro
        partesFecha = fecha.split("/")
        tuplafecha = (int(partesFecha[0]), int(partesFecha[1]), int(partesFecha[2]))

        nuevoDonador = [
            [nombre, apellido1, apellido2],
            cedula,
            tiposDeSangre.index(tipoSangre),
            sexo,
            tuplafecha,
            float(peso),
            correo,
            telefono,
            1,
            0
        ]
        baseDeDatos.append(nuevoDonador)
        guardarBaseDeDatos()

        # Realimentacion al usuario
        numeroProvincia = obtenerProvinciaPorCedula(cedula)
        lugaresTexto = ", ".join(lugaresDonacion.get(numeroProvincia, ["No disponible"]))

        if esMayorDeEdad(fecha):
            mensajeEdad = "Dado su fecha de nacimiento usted ya puede ser donador."
        else:
            mensajeEdad = "Dado su fecha de nacimiento usted aun no puede ser donador."

        if float(peso) <= 50:
            mensajePeso = "Usted debe pesar mas de 50 kgms para poder ser donador."
        elif float(peso) >= 120:
            mensajePeso = "Dado su sobre peso, no es posible donar sangre."
        else:
            mensajePeso = "Usted posee un peso adecuado, correcto para ser donador de sangre."

        mensajeSangre = obtenerInfoTipoDeSangre(tipoSangre)

        mensajeFinal = (
            f"{mensajeEdad}\n\n"
            f"Dado que usted nacio en la provincia de: {nombreProvincias.get(numeroProvincia, 'Desconocida')}, "
            f"usted podria donar en: {lugaresTexto}.\n\n"
            f"{mensajePeso}\n\n"
            f"Dado su tipo de sangre {tipoSangre}: {mensajeSangre}"
        )

        if tipoSangre in ("A+", "A-"):
            mensajeFinal += "\n\nSu tipo de sangre tiene particularidades especiales. Le recomendamos ver: 'Particularidades de la sangre tipo A: Responde diferente al estres segun la ciencia.'"

        messagebox.showinfo("Donador registrado", mensajeFinal)
        limpiarCampos()
        ventana.lift()

    # Botones
    marcoBotones = tk.Frame(ventana)
    marcoBotones.grid(row=12, column=0, columnspan=2, pady=15)

    tk.Button(marcoBotones, text="Registrar", width=12, bg="green", fg="white", command=registrarDonador).grid(row=0, column=0, padx=10)
    tk.Button(marcoBotones, text="Limpiar", width=12, command=limpiarCampos).grid(row=0, column=1, padx=10)
    tk.Button(marcoBotones, text="Regresar", width=12, bg="red", fg="white", command=ventana.destroy).grid(row=0, column=2, padx=10)

#Fin de Insertar Donador.
#======================================================================================
    #GENERAR DONADORES:

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


def generarFechaAleatoria(esDonador):
    """
    Funcionalidad: Genera una fecha de nacimiento aleatoria. Si es donador
                   genera una fecha que resulte en mayor de edad (18-65 anos),
                   si no es donador puede ser menor de edad.
    Entradas:
        - esDonador(bool): True si debe ser mayor de edad, False si puede ser menor.
    Salidas:
        - fecha(tuple): Tupla con (dia, mes, año) de la fecha generada.
    """
    if esDonador:
        año = random.randint(1960, 2006)
    else:
        año = random.randint(2010, 2020)

    mes = random.randint(1, 12)
    dia = random.randint(1, 28)
    return (dia, mes, año)


def generarNombreAleatorio():
    """
    Funcionalidad: Genera un nombre completo aleatorio usando listas de nombres
                   y apellidos predefinidos.
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

    nombre = random.choice(nombres)
    apellido1 = random.choice(apellidos)
    apellido2 = random.choice(apellidos)
    return [nombre, apellido1, apellido2]


def generarCorreoAleatorio(nombre):
    """
    Funcionalidad: Genera un correo electronico aleatorio basado en el nombre
                   del donador con dominios validos.
    Entradas:
        - nombre(str): El nombre del donador para construir el correo.
    Salidas:
        - correo(str): Correo electronico generado.
    """
    dominios = ["gmail.com", "costarricense.cr", "racsa.go.cr", "ccss.sa.cr"]
    numero = random.randint(1, 999)
    dominio = random.choice(dominios)
    return f"{nombre.lower()}{numero}@{dominio}"


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


def generarDonadores(ventanaPadre):
    """
    Funcionalidad: Abre una ventana que permite al usuario indicar cuantos
                   donadores desea generar dinamicamente. Crea donadores con
                   datos aleatorios, algunos validos y algunos no validos,
                   y los agrega a la base de datos con su justificacion.
    Entradas:
        - ventanaPadre(tk.Tk): La ventana principal del programa.
    Salidas: Ninguna. Modifica la lista global baseDeDatos.
    """
    ventana = tk.Toplevel(ventanaPadre)
    ventana.title("Generar Donadores")
    ventana.geometry("500x500")
    ventana.resizable(False, False)

    tk.Label(
        ventana,
        text="Generar Donadores",
        font=("Arial", 14, "bold"),
        fg="red"
    ).pack(pady=15)

    tk.Label(
        ventana,
        text="Cantidad de donadores a generar:",
        font=("Arial", 11)
    ).pack()

    campoCantidad = tk.Entry(ventana, width=15, font=("Arial", 11))
    campoCantidad.pack(pady=8)

    # Area de texto para mostrar el resultado
    tk.Label(ventana, text="Resultado:", font=("Arial", 11)).pack()

    areaResultado = tk.Text(ventana, height=16, width=58, font=("Courier New", 9))
    areaResultado.pack(pady=5)

    def ejecutarGeneracion():
        """
        Funcionalidad: Lee la cantidad ingresada, valida que sea mayor a 0,
                       y genera los donadores dinamicamente con datos aleatorios.
        Entradas: Ninguna. Lee el valor del campo campoCantidad.
        Salidas: Ninguna. Modifica baseDeDatos y muestra resultados en pantalla.
        """
        areaResultado.delete("1.0", tk.END)

        cantidad = campoCantidad.get().strip()

        # Validacion de la cantidad
        if not cantidad.isdigit() or int(cantidad) <= 0:
            messagebox.showerror("Error", "Debe ingresar un numero entero mayor a 0.")
            ventana.lift()
            return

        cantidad = int(cantidad)
        generados = 0
        noValidos = 0

        for _ in range(cantidad):
            # Decide aleatoriamente si el donador sera valido o no
            seraValido = random.random() > 0.3

            nombre = generarNombreAleatorio()
            cedula = generarCedulaAleatoria()

            # Asegura que la cedula no este repetida
            intentos = 0
            while cedulaYaExiste(cedula) and intentos < 100:
                cedula = generarCedulaAleatoria()
                intentos += 1

            tipoSangreIndex = random.randint(0, len(tiposDeSangre) - 1)
            sexo = random.choice([True, False])
            fecha = generarFechaAleatoria(seraValido)
            peso = round(random.uniform(55, 110) if seraValido else random.uniform(30, 49), 1)
            correo = generarCorreoAleatorio(nombre[0])
            telefono = f"{random.randint(2, 9)}{random.randint(100,999)}-{random.randint(1000,9999)}"

            if seraValido:
                estado = 1
                justificacion = 0
            else:
                estado = 0
                # Justificacion aleatoria del 1 al 7 segun razones de GEMINI
                justificacion = random.randint(1, 7)
                noValidos += 1

            nuevoDonador = [
                nombre,
                cedula,
                tipoSangreIndex,
                sexo,
                fecha,
                float(peso),
                correo,
                telefono,
                estado,
                justificacion
            ]
            baseDeDatos.append(nuevoDonador)
            generados += 1

            # Muestra en el area de texto
            nombreCompleto = f"{nombre[0]} {nombre[1]} {nombre[2]}"
            estadoTexto = "ACTIVO  " if estado == 1 else f"INACTIVO (justif. {justificacion})"
            areaResultado.insert(
                tk.END,
                f"{cedula} | {nombreCompleto:<30} | {tiposDeSangre[tipoSangreIndex]:<3} | {estadoTexto}\n"
            )
        guardarBaseDeDatos() #Guarda los datos en la memoria secundaria.
        
        areaResultado.insert(
            tk.END,
            f"\n{'='*55}\n"
            f"Total generados: {generados} | Activos: {generados - noValidos} | Inactivos: {noValidos}\n"
        )

    # Botones
    marcoBotones = tk.Frame(ventana)
    marcoBotones.pack(pady=8)

    tk.Button(
        marcoBotones,
        text="Generar",
        width=15,
        bg="green",
        fg="white",
        command=ejecutarGeneracion
    ).grid(row=0, column=0, padx=10)

    tk.Button(
        marcoBotones,
        text="Regresar",
        width=15,
        bg="red",
        fg="white",
        command=ventana.destroy
    ).grid(row=0, column=1, padx=10)

    
#Fin Generar Donador.
#======================================================================================
    #ACTUALIZAR DATOS DEL DONADOR:
def ActualizarDonador(ventanaPadre):
    """
    Funcionalidad: Abre el formulario y pide el numero de cedula, si lo encuentra
                   da todos los datos para que el usuario pueda modificarlos.
                   Valida cada campo con expresiones regulares y
                   Confirma si se hicieron los cambios.
    Entradas:
        - ventanaPadre(tk.Tk): La ventana principal del programa.
    Salidas: Ninguna. Modifica al donador en la lista global baseDeDatos si es valido.
    """    
    ventana = tk.Toplevel(ventanaPadre)
    ventana.title("Actualizar Donador")
    ventana.geometry("500x580")
    ventana.resizable(False, False)

    tk.Label(
        ventana,
        text="Actualizar Datos del Donador",
        font=("Arial", 14, "bold"),
        fg="red"
    ).grid(row=0, column=0, columnspan=2, pady=10)

    # Campos del formulario
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
    sexoVar.set(True)  # Masculino por omision
    radMasculino= tk.Radiobutton(ventana, text="Masculino", variable=sexoVar, value=True,state="disabled")
    radMasculino.grid(row=7, column=1, sticky="w", padx=10)
    radFemenino=tk.Radiobutton(ventana, text="Femenino", variable=sexoVar, value=False,state="disabled")
    radFemenino.grid(row=8, column=1, sticky="w", padx=10)

    tk.Label(ventana, text="Peso (kg):", anchor="w").grid(row=9, column=0, padx=20, pady=5, sticky="w")
    campoPeso = tk.Entry(ventana, width=30)
    campoPeso.grid(row=9, column=1, padx=10)

    tk.Label(ventana, text="Telefono (####-####):", anchor="w").grid(row=10, column=0, padx=20, pady=5, sticky="w")
    campoTelefono = tk.Entry(ventana, width=30)
    campoTelefono.grid(row=10, column=1, padx=10)

    tk.Label(ventana, text="Correo:", anchor="w").grid(row=11, column=0, padx=20, pady=5, sticky="w")
    campoCorreo = tk.Entry(ventana, width=30)
    campoCorreo.grid(row=11, column=1, padx=10)

    #Lista con nombres de las entradas de datos para poder deshabilitarlos o habilitarlos
    camposDatos = [campoNombre,campoApellido1,campoApellido2,campoFecha,campoPeso,campoTelefono,campoCorreo]
    for estado in camposDatos:
        estado.config(state="disabled")

    cajaTipoSangre.config(state="disabled")

    #Revisa la cedula y marca los espacios vacios:
    def buscarCedula():
        
        """Funcionalidad: Toma el dato escrito en el campoCedula, le quita los espacios y la valida,
        luego busca una cedula igual en todos los datos y cambia el estado de todas las entradas
        e inserta la información guardada en los campos vacios."""

        cedula = campoCedula.get().strip()

        if not validarCedula(cedula):
            messagebox.showerror("Error","Cedula invalida. Formato: #-####-####, primer digito no puede ser 0.")
            ventana.lift()
            return
        
        for donador in baseDeDatos:
            if donador[1] == cedula:

                campoCedula.config(state="readonly")

                for campo in camposDatos:
                    campo.config(state="normal")
                cajaTipoSangre.config(state="normal")


                campoNombre.insert(0, donador[0][0])
                campoApellido1.insert(0, donador[0][1])
                campoApellido2.insert(0, donador[0][2])

                fecha = donador[4]
                fecha = donador[4]

                dia=str(fecha[0])
                mes=str(fecha[1])
                año=str(fecha[2])
                if fecha[0]< 10:
                    dia= "0"+ dia
                if fecha[1]< 10:
                    mes= "0"+ mes

                campoFecha.insert(0, dia+"/"+mes+"/"+año)

                tipoSangreVar.set(tiposDeSangre[donador[2]])
                sexoVar.set(donador[3])

                campoPeso.insert(0, str(donador[5]))
                campoCorreo.insert(0, donador[6])
                campoTelefono.insert(0, donador[7])

                radMasculino.config(state="normal")
                radFemenino.config(state="normal")
                botonBuscar.config(state="disabled")
                botonRegistrar.config(state="normal")

                ventana.lift()
                return

        messagebox.showerror("No encontrado",f"La persona con el número de cédula: {cedula} no está registrado en la base de datos del Banco de Sangre aún.")
        ventana.lift()

    def registrarCambios():
        """Funcionalidad: Valida todos los campos que el usuario cambia o no cambia y los guarda.
        Entradas:nada, Lee los valores de las entradas
        Salidas: ninguna. Modifica la base de datos.
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

        # Validaciones
        if nombre == "" or apellido1 == "" or apellido2 == "":
            messagebox.showerror("Error", "Nombre completo es requerido.")
            ventana.lift()
            return

        if not validarFecha(fecha):
            messagebox.showerror("Error", "Fecha invalida. Formato: DD/MM/AAAA.")
            ventana.lift()
            return

        if not validarPeso(peso):
            messagebox.showerror("Error", "Peso invalido. Debe ser mayor a 50 y menor a 120 kg.")
            ventana.lift()
            return

        if not validarTelefono(telefono):
            messagebox.showerror("Error", "Telefono invalido. Formato: ####-####, primer digito no puede ser 0, 1, 3 ni 5.")
            ventana.lift()
            return

        if not validarCorreo(correo):
            messagebox.showerror("Error", "Correo invalido.")
            ventana.lift()
            return

        # Arma la tupla de fecha...
        partesFecha = fecha.split("/")
        tuplaFecha = (int(partesFecha[0]), int(partesFecha[1]), int(partesFecha[2]))

        # Busca el donador y lo actualiza 
        for donador in baseDeDatos:
            if donador[1] == cedula:
                donador[0] = [nombre, apellido1, apellido2]
                donador[2] = tiposDeSangre.index(tipoSangre)
                donador[3] = sexo
                donador[4] = tuplaFecha
                donador[5] = float(peso)
                donador[6] = correo
                donador[7] = telefono

                guardarBaseDeDatos()
                messagebox.showinfo("Éxito", "Se actualizaron los datos del donador.")
                ventana.lift()
                return



    # Botones
    marcoBotones = tk.Frame(ventana)
    marcoBotones.grid(row=12, column=0, columnspan=2, pady=15)

    botonBuscar = tk.Button(marcoBotones, text="Buscar cedula", width=12, bg="lightgreen", command=buscarCedula)
    botonBuscar.grid(row=0, column=0, padx=10)
    botonRegistrar = tk.Button(marcoBotones, text="Registrar",width=12,state="disabled", command=registrarCambios)
    botonRegistrar.grid(row=0, column=1, padx=10)
    tk.Button(marcoBotones, text="Regresar", width=12, bg="red", fg="white", command=ventana.destroy).grid(row=0, column=2, padx=10)

#Fin Actualizar datos del donador
#======================================================================================
    #ELIMINAR DONADOR:

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
    
def eliminarDonador(ventanaPadre):
    """
    Funcionalidad: Abre una ventana que permite al usuario eliminar un donador
                   de la base de datos ingresando su cedula. Si existe, muestra
                   una justificacion via caja de seleccion y pide confirmacion.
                   El donador no se borra fisicamente, su estado cambia a inactivo.
    Entradas:
        - ventanaPadre(tk.Tk): La ventana principal del programa.
    Salidas: Ninguna. Modifica el estado del donador en la lista global baseDeDatos.
    """
    ventana = tk.Toplevel(ventanaPadre)
    ventana.title("Eliminar Donador")
    ventana.geometry("500x400")
    ventana.resizable(False, False)

    tk.Label(
        ventana,
        text="Eliminar Donador",
        font=("Arial", 14, "bold"),
        fg="red"
    ).pack(pady=15)

    # Campo de cedula
    marcoCedula = tk.Frame(ventana)
    marcoCedula.pack(pady=5)

    tk.Label(marcoCedula, text="Cedula (#-####-####):", font=("Arial", 11)).grid(row=0, column=0, padx=10)
    campoCedula = tk.Entry(marcoCedula, width=20, font=("Arial", 11))
    campoCedula.grid(row=0, column=1, padx=10)

    # Marco de informacion del donador (oculto al inicio)
    marcoInfo = tk.Frame(ventana)

    etiquetaNombre = tk.Label(marcoInfo, text="", font=("Arial", 11))
    etiquetaNombre.pack(pady=5)

    # Caja de seleccion de justificacion
    tk.Label(marcoInfo, text="Justificacion de eliminacion:", font=("Arial", 11)).pack()

    opcionesJustificacion = [f"{k} - {v[:50]}..." for k, v in justificaciones.items()]
    justificacionVar = tk.StringVar()
    justificacionVar.set(opcionesJustificacion[0])

    cajaJustificacion = tk.OptionMenu(marcoInfo, justificacionVar, *opcionesJustificacion)
    cajaJustificacion.config(width=50)
    cajaJustificacion.pack(pady=5)

    # Marco de botones de confirmacion (oculto al inicio)
    marcoBotonesConfirmar = tk.Frame(marcoInfo)
    marcoBotonesConfirmar.pack(pady=10)

    def confirmarEliminacion():
        """
        Funcionalidad: Cambia el estado del donador a inactivo (0) con la
                       justificacion seleccionada y guarda en memoria secundaria.
        Entradas: Ninguna. Lee la cedula y justificacion de los campos.
        Salidas: Ninguna. Modifica baseDeDatos y guarda en baseDeDatos.pkl.
        """
        cedula = campoCedula.get().strip()
        indice = buscarDonadorPorCedula(cedula)

        numeroJustificacion = int(justificacionVar.get().split(" - ")[0])

        baseDeDatos[indice][8] = 0
        baseDeDatos[indice][9] = numeroJustificacion
        guardarBaseDeDatos()

        messagebox.showinfo("Exito", "Donador eliminado satisfactoriamente.")
        ventana.destroy()

    def rechazarEliminacion():
        """
        Funcionalidad: Cancela la eliminacion y mantiene el donador como activo.
        Entradas: Ninguna.
        Salidas: Ninguna. Muestra mensaje y se mantiene en la ventana.
        """
        messagebox.showinfo("Cancelado", "Donador NO eliminado.")
        marcoInfo.pack_forget()
        campoCedula.delete(0, tk.END)

    tk.Button(
        marcoBotonesConfirmar,
        text="Confirmar",
        width=15,
        bg="green",
        fg="white",
        command=confirmarEliminacion
    ).grid(row=0, column=0, padx=10)

    tk.Button(
        marcoBotonesConfirmar,
        text="Cancelar",
        width=15,
        bg="orange",
        command=rechazarEliminacion
    ).grid(row=0, column=1, padx=10)

    def buscarDonador():
        """
        Funcionalidad: Busca al donador por cedula y muestra el formulario de
                       justificacion si existe, o un mensaje de error si no.
        Entradas: Ninguna. Lee el valor del campo campoCedula.
        Salidas: Ninguna. Muestra u oculta el marco de informacion segun resultado.
        """
        cedula = campoCedula.get().strip()

        if cedula == "":
            messagebox.showwarning("Aviso", "Debe ingresar un numero de cedula.")
            ventana.lift()
            return

        indice = buscarDonadorPorCedula(cedula)

        if indice == -1:
            messagebox.showwarning(
                "No encontrado",
                f"La persona con el numero de cedula: {cedula} no esta registrada en la base de datos del Banco de Sangre aun."
            )
            marcoInfo.pack_forget()
            ventana.lift()
            return

        # Si ya esta inactivo
        if baseDeDatos[indice][8] == 0:
            messagebox.showwarning(
                "Aviso",
                f"El donador con cedula {cedula} ya se encuentra inactivo."
            )
            ventana.lift()
            return

        # Muestra la informacion del donador encontrado
        nombre = baseDeDatos[indice][0]
        nombreCompleto = f"{nombre[0]} {nombre[1]} {nombre[2]}"
        tipoSangre = tiposDeSangre[baseDeDatos[indice][2]]

        etiquetaNombre.config(
            text=f"Donador: {nombreCompleto} | Tipo de sangre: {tipoSangre}"
        )
        marcoInfo.pack(pady=10)

    # Boton de buscar
    tk.Button(
        ventana,
        text="Buscar",
        width=15,
        bg="blue",
        fg="white",
        command=buscarDonador
    ).pack(pady=8)

    # Boton regresar
    tk.Button(
        ventana,
        text="Regresar",
        width=15,
        bg="red",
        fg="white",
        command=ventana.destroy
    ).pack(pady=5)



    

#Fin Eliminar Donador.
#======================================================================================
    #INSERTAR LUGAR DE DONACIÓN SEGÚN PROVINCIA:


def insertarLugarDonacion(ventanaPadre):
    """
    Funcionalidad: Abre una ventana que permite al usuario insertar un nuevo
                   lugar de donacion en una provincia seleccionada. Verifica
                   que el lugar no este ya registrado antes de agregarlo.
    Entradas:
        - ventanaPadre(tk.Tk): La ventana principal del programa para poder
                               regresar a ella al salir.
    Salidas: Ninguna. Modifica el diccionario global lugaresDonacion.
    """
    ventana = tk.Toplevel(ventanaPadre)
    ventana.title("Insertar Lugar de Donacion")
    ventana.geometry("450x350")
    ventana.resizable(False, False)

    # Titulo
    tk.Label(
        ventana,
        text="Insertar Lugar de Donacion",
        font=("Arial", 14, "bold"),
        fg="red"
    ).pack(pady=15)

    # Seleccion de provincia
    tk.Label(ventana, text="Provincia:", font=("Arial", 11)).pack()

    opcionesProvincias = [f"{k} - {v}" for k, v in nombreProvincias.items()]
    provinciaSeleccionada = tk.StringVar()
    provinciaSeleccionada.set(opcionesProvincias[0])

    cajaProvincias = tk.OptionMenu(ventana, provinciaSeleccionada, *opcionesProvincias)
    cajaProvincias.config(width=30)
    cajaProvincias.pack(pady=5)

    # Campo para el nuevo lugar
    tk.Label(ventana, text="Nuevo lugar de donacion:", font=("Arial", 11)).pack(pady=5)

    areaTexto = tk.Text(ventana, height=4, width=40, font=("Arial", 10))
    areaTexto.pack(pady=5)

    # Funcion interna del boton Insertar
    def confirmarInsercion():
        """
        Funcionalidad: Valida y ejecuta la insercion del nuevo lugar en el
                       diccionario global lugaresDonacion.
        Entradas: Ninguna. Lee los valores de los campos de la ventana.
        Salidas: Ninguna. Modifica lugaresDonacion si la insercion es valida.
        """
        nuevoLugar = areaTexto.get("1.0", tk.END).strip()

        if nuevoLugar == "":
            messagebox.showwarning("Aviso", "Debe ingresar un lugar de donacion.")
            return

        # Obtiene el numero de provincia del string seleccionado
        numeroProvincia = int(provinciaSeleccionada.get().split(" - ")[0])

        # Verifica que el lugar no este ya registrado en esa provincia
        for lugar in lugaresDonacion[numeroProvincia]:
            if lugar.lower() == nuevoLugar.lower():
                messagebox.showwarning(
                    "Aviso",
                    f"El lugar '{nuevoLugar}' ya esta registrado en {nombreProvincias[numeroProvincia]}."
                )
                ventana.lift()
                return

        # Agrega el nuevo lugar
        lugaresDonacion[numeroProvincia].append(nuevoLugar)

        
        messagebox.showinfo(
            "Exito",
            f"Lugar '{nuevoLugar}' agregado exitosamente en {nombreProvincias[numeroProvincia]}."
        )
        areaTexto.delete("1.0", tk.END)
        ventana.lift()

    # Botones
    marcosBotones = tk.Frame(ventana)
    marcosBotones.pack(pady=10)

    tk.Button(
        marcosBotones,
        text="Insertar",
        width=15,
        bg="green",
        fg="white",
        command=confirmarInsercion
    ).grid(row=0, column=0, padx=10)

    tk.Button(
        marcosBotones,
        text="Salir",
        width=15,
        bg="red",
        fg="white",
        command=ventana.destroy
    ).grid(row=0, column=1, padx=10)



#Fin Insertar lugar de donación según provincia. 
#======================================================================================
    #REPORTES:




#Fin Reportes.
#======================================================================================
#FIN DE FUNCIONES PRINCIPALES.
#=======================================================================================================
    #VENTANA DEL MENÚ PRINCIPAL:
    
def abrirVentanaMenuPrincipal():
    """
    Funcionalidad: Crea y muestra la ventana principal del programa con los 7 botones
                   del menu. Si hay base de datos activa todos los botones, si no,
                   solo activa los botones 1, 2, 5 y 7.
    Entradas: Ninguna.
    Salidas: Ninguna. Abre la ventana principal del programa.
    """
    hayBaseDeDatos = cargarBaseDeDatos()

    ventana = tk.Tk()
    ventana.title("Sistema de Banco de Sangre")
    ventana.geometry("400x500")
    ventana.resizable(False, False)

    # Titulo principal
    etiquetaTitulo = tk.Label(
        ventana,
        text="Banco de Sangre\nSistema de Informacion",
        font=("Arial", 16, "bold"),
        fg="red"
    )
    etiquetaTitulo.pack(pady=20)

    # Determina el estado de cada boton segun si hay base de datos o no
    if hayBaseDeDatos:
        estadoBotones = tk.NORMAL
    else:
        estadoBotones = tk.DISABLED

    # Boton 1 - siempre activo
    boton1 = tk.Button(
        ventana,
        text="1. Insertar donador",
        width=30,
        command=lambda: insertarDonador(ventana)
    )
    boton1.pack(pady=5)

    # Boton 2 - siempre activo
    boton2 = tk.Button(
        ventana,
        text="2. Generar donadores",
        width=30,
        command=lambda: generarDonadores(ventana)
    )
    boton2.pack(pady=5)

    # Boton 3 - solo si hay base de datos
    boton3 = tk.Button(
        ventana,
        text="3. Actualizar datos del donador",
        width=30,
        state=estadoBotones,
        command=lambda: ActualizarDonador(ventana)
    )
    boton3.pack(pady=5)

    # Boton 4 - solo si hay base de datos
    boton4 = tk.Button(
        ventana,
        text="4. Eliminar donador",
        width=30,
        state=estadoBotones,
        command=lambda: eliminarDonador(ventana)
    )
    boton4.pack(pady=5)

    # Boton 5 - siempre activo
    boton5 = tk.Button(
        ventana,
        text="5. Insertar lugar de donacion",
        width=30,
        command=lambda: insertarLugarDonacion(ventana)
    )
    boton5.pack(pady=5)

    # Boton 6 - solo si hay base de datos
    boton6 = tk.Button(
        ventana,
        text="6. Reportes",
        width=30,
        state=estadoBotones,
        command=lambda: print("Reportes")  # Por implementar
    )
    boton6.pack(pady=5)

    # Boton 7 - siempre activo
    boton7 = tk.Button(
        ventana,
        text="7. Salir",
        width=30,
        fg="white",
        bg="red",
        command=lambda: salir(ventana)
    )
    boton7.pack(pady=5)

    # Mensaje informativo si no hay base de datos
    if not hayBaseDeDatos:
        etiquetaAviso = tk.Label(
            ventana,
            text="* Sin base de datos: solo opciones 1, 2, 5 y 7 disponibles.",
            font=("Arial", 8),
            fg="gray"
        )
        etiquetaAviso.pack(pady=5)

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
