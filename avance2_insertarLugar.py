# Elaborado por: Alejandro Madrigal y Brandon Meza
# Fecha de creacion: 28/05/2026
# Ultima modificacion: 28/05/2026
# Version de Python: 3.11

import tkinter as tk
from tkinter import messagebox

# =========================================================
# Diccionario global con los lugares de donacion por provincia
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
                return

        # Agrega el nuevo lugar
        lugaresDonacion[numeroProvincia].append(nuevoLugar)
        messagebox.showinfo(
            "Exito",
            f"Lugar '{nuevoLugar}' agregado exitosamente en {nombreProvincias[numeroProvincia]}."
        )
        areaTexto.delete("1.0", tk.END)

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


# =========================================================
# Prueba rapida de la ventana
if __name__ == "__main__":
    raiz = tk.Tk()
    raiz.withdraw()
    insertarLugarDonacion(raiz)
    raiz.mainloop()
