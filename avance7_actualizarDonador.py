# Elaborado por: Alejandro Madrigal y Brandon Meza
# Fecha de creacion: 27/05/2026
# Ultima modificacion: 03/06/2026
# Version de Python: 3.11

import tkinter as tk
from tkinter import messagebox
import pickle
import re
from datetime import date

# =========================================================
# Tupla global con los tipos de sangre
tiposDeSangre = ("O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-")

# Lista global que funciona como matriz de donadores
baseDeDatos = []
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


def actualizarDonador(ventanaPadre):
    """
    Funcionalidad: Abre una ventana que permite buscar un donador por cedula
                   y modificar cualquiera de sus datos excepto la cedula.
                   Si confirma guarda los cambios, si rechaza se mantiene en
                   la ventana sin guardar.
    Entradas:
        - ventanaPadre(tk.Tk): La ventana principal del programa.
    Salidas: Ninguna. Modifica el donador en la lista global baseDeDatos si confirma.
    """
    ventana = tk.Toplevel(ventanaPadre)
    ventana.title("Actualizar Datos del Donador")
    ventana.geometry("520x620")
    ventana.resizable(False, False)

    tk.Label(
        ventana,
        text="Actualizar Datos del Donador",
        font=("Arial", 14, "bold"),
        fg="red"
    ).pack(pady=10)

    # Campo de busqueda por cedula
    marcoBusqueda = tk.Frame(ventana)
    marcoBusqueda.pack(pady=5)

    tk.Label(marcoBusqueda, text="Cedula (#-####-####):", font=("Arial", 11)).grid(row=0, column=0, padx=10)
    campoCedula = tk.Entry(marcoBusqueda, width=20, font=("Arial", 11))
    campoCedula.grid(row=0, column=1, padx=5)

    tk.Button(
        marcoBusqueda,
        text="Buscar",
        width=10,
        bg="blue",
        fg="white",
        command=lambda: buscarYCargar()
    ).grid(row=0, column=2, padx=5)

    # Marco del formulario (oculto al inicio)
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

    # Guarda el indice del donador encontrado
    indiceEncontrado = [-1]

    def buscarYCargar():
        """
        Funcionalidad: Busca el donador por cedula y si existe carga sus datos
                       en el formulario para que el usuario los pueda modificar.
        Entradas: Ninguna. Lee el valor del campo campoCedula.
        Salidas: Ninguna. Carga el formulario con los datos del donador encontrado.
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
            marcoFormulario.pack_forget()
            marcoBotones.pack_forget()
            return

        indiceEncontrado[0] = indice
        donador = baseDeDatos[indice]

        # Carga los datos actuales en el formulario
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
        Funcionalidad: Valida los campos modificados y si todo es correcto
                       guarda los cambios en la base de datos y en memoria secundaria.
        Entradas: Ninguna. Lee los valores de los campos del formulario.
        Salidas: Ninguna. Modifica baseDeDatos y guarda en baseDeDatos.pkl si es valido.
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
            messagebox.showerror("Error", "Fecha invalida. Formato: DD/MM/AAAA.")
            return
        if not validarPeso(peso):
            messagebox.showerror("Error", "Peso invalido. Debe ser mayor a 50 y menor a 120 kg.")
            return
        if not validarTelefono(telefono):
            messagebox.showerror("Error", "Telefono invalido. Formato: ####-####.")
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
        Funcionalidad: Cancela la actualizacion y mantiene los datos sin cambios.
        Entradas: Ninguna.
        Salidas: Ninguna. Muestra mensaje y se mantiene en la ventana.
        """
        messagebox.showinfo("Cancelado", "Datos No actualizados.")

    # Marco de botones (oculto al inicio)
    marcoBotones = tk.Frame(ventana)

    tk.Button(
        marcoBotones,
        text="Confirmar",
        width=14,
        bg="green",
        fg="white",
        command=confirmarActualizacion
    ).grid(row=0, column=0, padx=10)

    tk.Button(
        marcoBotones,
        text="Rechazar",
        width=14,
        bg="orange",
        command=rechazarActualizacion
    ).grid(row=0, column=1, padx=10)

    tk.Button(
        marcoBotones,
        text="Regresar",
        width=14,
        bg="red",
        fg="white",
        command=ventana.destroy
    ).grid(row=0, column=2, padx=10)


# =========================================================
# Prueba rapida de la ventana
if __name__ == "__main__":
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
    actualizarDonador(raiz)
    raiz.mainloop()
