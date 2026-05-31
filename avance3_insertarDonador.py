# Elaborado por: Alejandro Madrigal y Brandon Meza
# Fecha de creacion: 29/05/2026
# Ultima modificacion: 29/05/2026
# Version de Python: 3.11

import tkinter as tk
from tkinter import messagebox
import re
from datetime import date

# =========================================================
# Tupla global con los tipos de sangre
tiposDeSangre = ("O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-")

# Lista global que funciona como matriz de donadores
baseDeDatos = []

# Diccionario de lugares de donacion por provincia
lugaresDonacion = {
    1: ["Banco Nacional de Sangre", "Hospital Mexico", "Hospital San Juan de Dios"],
    2: ["Hospital San Rafael de Alajuela", "Hospital de San Ramon", "Hospital del Canton Norteno"],
    3: ["Hospital Max Peralta"],
    4: ["Hospital San Vicente de Paul"],
    5: ["Hospital La Anexion en Nicoya", "Hospital Enrique Baltodano de Liberia"],
    6: ["Hospital Monsenor Sanabria"],
    7: ["Hospital Tony Facio", "Hospital de Guapiles"]
}

nombreProvincias = {
    1: "San Jose",
    2: "Alajuela",
    3: "Cartago",
    4: "Heredia",
    5: "Guanacaste",
    6: "Puntarenas",
    7: "Limon"
}
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
        anio = int(partes[2])
        date(anio, mes, dia)
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
                   fecha de nacimiento con la fecha actual por mes y anio.
    Entradas:
        - fecha(str): La fecha de nacimiento en formato DD/MM/AAAA.
    Salidas: Retorna True si es mayor de edad, False en caso contrario.
    """
    partes = fecha.split("/")
    anioNac = int(partes[2])
    mesNac = int(partes[1])
    hoy = date.today()
    if hoy.year - anioNac > 18:
        return True
    if hoy.year - anioNac == 18 and hoy.month >= mesNac:
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

        # Verifica si la cedula ya esta registrada
        for donador in baseDeDatos:
            if donador[1] == cedula:
                messagebox.showerror("Error", f"La cedula {cedula} ya esta registrada.")
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

    # Botones
    marcoBotones = tk.Frame(ventana)
    marcoBotones.grid(row=12, column=0, columnspan=2, pady=15)

    tk.Button(marcoBotones, text="Registrar", width=12, bg="green", fg="white", command=registrarDonador).grid(row=0, column=0, padx=10)
    tk.Button(marcoBotones, text="Limpiar", width=12, command=limpiarCampos).grid(row=0, column=1, padx=10)
    tk.Button(marcoBotones, text="Regresar", width=12, bg="red", fg="white", command=ventana.destroy).grid(row=0, column=2, padx=10)


# =========================================================
# Prueba rapida de la ventana
if __name__ == "__main__":
    raiz = tk.Tk()
    raiz.withdraw()
    insertarDonador(raiz)
    raiz.mainloop()
