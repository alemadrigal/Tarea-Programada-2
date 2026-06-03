# Elaborado por: Alejandro Madrigal y Brandon Meza
# Fecha de creacion: 03/06/2026
# Ultima modificacion: 03/06/2026
# Version de Python: 3.11

import tkinter as tk
from tkinter import messagebox
import pickle

# =========================================================
# Tupla global con los tipos de sangre
tiposDeSangre = ("O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-")

# Lista global que funciona como matriz de donadores
baseDeDatos = []

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
            return

        indice = buscarDonadorPorCedula(cedula)

        if indice == -1:
            messagebox.showwarning(
                "No encontrado",
                f"La persona con el numero de cedula: {cedula} no esta registrada en la base de datos del Banco de Sangre aun."
            )
            marcoInfo.pack_forget()
            return

        # Si ya esta inactivo
        if baseDeDatos[indice][8] == 0:
            messagebox.showwarning(
                "Aviso",
                f"El donador con cedula {cedula} ya se encuentra inactivo."
            )
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


# =========================================================
# Prueba rapida de la ventana
if __name__ == "__main__":
    # Datos de prueba
    baseDeDatos.append([
        ["Juan", "Perez", "Mora"],
        "1-1234-5678",
        0,
        True,
        (15, 3, 1990),
        75.0,
        "juan10@gmail.com",
        "8765-4321",
        1,
        0
    ])
    raiz = tk.Tk()
    raiz.withdraw()
    eliminarDonador(raiz)
    raiz.mainloop()
