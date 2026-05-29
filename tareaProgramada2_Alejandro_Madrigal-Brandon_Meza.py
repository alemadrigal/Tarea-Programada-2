# Elaborado por: Alejandro Madrigal y Brandon Meza
# Fecha de creacion: 27/05/2026
# Ultima modificacion: 27/05/2026
# Version de Python: 3.11

import tkinter as tk
from tkinter import messagebox
import pickle

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
        command=lambda: print("Insertar donador")  # Por implementar
    )
    boton1.pack(pady=5)

    # Boton 2 - siempre activo
    boton2 = tk.Button(
        ventana,
        text="2. Generar donadores",
        width=30,
        command=lambda: print("Generar donadores")  # Por implementar
    )
    boton2.pack(pady=5)

    # Boton 3 - solo si hay base de datos
    boton3 = tk.Button(
        ventana,
        text="3. Actualizar datos del donador",
        width=30,
        state=estadoBotones,
        command=lambda: print("Actualizar donador")  # Por implementar
    )
    boton3.pack(pady=5)

    # Boton 4 - solo si hay base de datos
    boton4 = tk.Button(
        ventana,
        text="4. Eliminar donador",
        width=30,
        state=estadoBotones,
        command=lambda: print("Eliminar donador")  # Por implementar
    )
    boton4.pack(pady=5)

    # Boton 5 - siempre activo
    boton5 = tk.Button(
        ventana,
        text="5. Insertar lugar de donacion",
        width=30,
        command=lambda: print("Insertar lugar")  # Por implementar
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
