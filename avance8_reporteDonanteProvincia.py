# Elaborado por: Alejandro Madrigal y Brandon Meza
# Fecha de creacion: 27/05/2026
# Ultima modificacion: 04/06/2026
# Version de Python: 3.11

import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# =========================================================
# Tupla global con los tipos de sangre
tiposDeSangre = ("O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-")

# Lista global que funciona como matriz de donadores
baseDeDatos = []

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
# =========================================================


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


def generarReporteDonanteProvincia(ventanaPadre):
    """
    Funcionalidad: Abre una ventana que permite al usuario seleccionar una
                   provincia y generar un reporte HTML con los donantes activos
                   de esa provincia, ordenados por nombre completo.
    Entradas:
        - ventanaPadre(tk.Tk): La ventana principal del programa.
    Salidas: Ninguna. Crea un archivo HTML en la carpeta del programa.
    """
    ventana = tk.Toplevel(ventanaPadre)
    ventana.title("Reporte - Donantes por Provincia")
    ventana.geometry("420x280")
    ventana.resizable(False, False)

    tk.Label(
        ventana,
        text="Reporte: Donantes por Provincia",
        font=("Arial", 13, "bold"),
        fg="red"
    ).pack(pady=15)

    tk.Label(ventana, text="Seleccione la provincia:", font=("Arial", 11)).pack()

    opcionesProvincias = [f"{k} - {v}" for k, v in nombreProvincias.items()]
    provinciaVar = tk.StringVar()
    provinciaVar.set(opcionesProvincias[0])

    cajaProvincias = tk.OptionMenu(ventana, provinciaVar, *opcionesProvincias)
    cajaProvincias.config(width=30)
    cajaProvincias.pack(pady=8)

    def generarReporte():
        """
        Funcionalidad: Filtra los donantes activos de la provincia seleccionada,
                       los ordena por nombre completo y genera el archivo HTML
                       con el reporte correspondiente.
        Entradas: Ninguna. Lee la provincia seleccionada del campo provinciaVar.
        Salidas: Ninguna. Crea el archivo HTML del reporte en la carpeta del programa.
        """
        numeroProvincia = int(provinciaVar.get().split(" - ")[0])
        nombreProv = nombreProvincias[numeroProvincia]

        # Filtra donantes activos de esa provincia
        donantesProvicia = []
        for donador in baseDeDatos:
            cedulaProv = int(donador[1][0])
            if cedulaProv == numeroProvincia and donador[8] == 1:
                donantesProvicia.append(donador)

        # Ordena por nombre completo
        for i in range(len(donantesProvicia) - 1):
            for j in range(i + 1, len(donantesProvicia)):
                nombreI = f"{donantesProvicia[i][0][0]} {donantesProvicia[i][0][1]} {donantesProvicia[i][0][2]}"
                nombreJ = f"{donantesProvicia[j][0][0]} {donantesProvicia[j][0][1]} {donantesProvicia[j][0][2]}"
                if nombreI > nombreJ:
                    donantesProvicia[i], donantesProvicia[j] = donantesProvicia[j], donantesProvicia[i]

        ahora = datetime.now()
        fechaHora = ahora.strftime("%d/%m/%Y %H:%M:%S")
        nombreArchivo = f"reporte_provincia_{numeroProvincia}_{ahora.strftime('%d-%m-%Y_%H-%M-%S')}.html"

        # Genera las filas de la tabla
        filasHtml = ""
        for i in range(len(donantesProvicia)):
            d = donantesProvicia[i]
            nombreCompleto = f"{d[0][0]} {d[0][1]} {d[0][2]}"
            fecha = d[4]
            fechaNac = f"{fecha[0]:02d}/{fecha[1]:02d}/{fecha[2]}"
            colorFila = "#ffffff" if i % 2 == 0 else "#f2f2f2"
            filasHtml += f"""
            <tr style="background-color:{colorFila}; text-align:center;">
                <td>{d[1]}</td>
                <td>{nombreCompleto}</td>
                <td>{fechaNac}</td>
                <td>{d[7]}</td>
                <td>{d[6]}</td>
            </tr>"""

        if filasHtml == "":
            filasHtml = "<tr><td colspan='5' style='text-align:center;'>No hay donantes activos en esta provincia.</td></tr>"

        contenidoHtml = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8"/>
    <title>Reporte de Donantes - {nombreProv}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 30px; }}
        h1 {{ color: red; }}
        h2 {{ color: #555; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th {{ background-color: #c0392b; color: white; padding: 10px; text-align: center; }}
        td {{ border: 1px solid #ddd; padding: 8px; }}
    </style>
</head>
<body>
    <h1>Reporte de Traduccion</h1>
    <h1>Donantes Activos - Provincia de {nombreProv}</h1>
    <h2>Generado el: {fechaHora}</h2>
    <table>
        <tr>
            <th>Cedula</th>
            <th>Nombre Completo</th>
            <th>Fecha de Nacimiento</th>
            <th>Telefono</th>
            <th>Correo</th>
        </tr>
        {filasHtml}
    </table>
</body>
</html>"""

        try:
            archivo = open(nombreArchivo, "w", encoding="utf-8")
            archivo.write(contenidoHtml)
            archivo.close()
            messagebox.showinfo("Exito", "Reporte creado satisfactoriamente.")
        except:
            messagebox.showerror("Error", "Reporte no creado.")

    # Botones
    marcoBotones = tk.Frame(ventana)
    marcoBotones.pack(pady=15)

    tk.Button(
        marcoBotones,
        text="Generar reporte",
        width=16,
        bg="green",
        fg="white",
        command=generarReporte
    ).grid(row=0, column=0, padx=10)

    tk.Button(
        marcoBotones,
        text="Regresar",
        width=16,
        bg="red",
        fg="white",
        command=ventana.destroy
    ).grid(row=0, column=1, padx=10)


# =========================================================
# Prueba rapida de la ventana
if __name__ == "__main__":
    baseDeDatos.append([["Juan", "Perez", "Mora"], "1-1234-5678", 0, True, (15, 3, 1990), 75.0, "juan10@gmail.com", "8765-4321", 1, 0])
    baseDeDatos.append([["Ana", "Gomez", "Vega"], "1-2345-6789", 2, False, (20, 5, 1995), 60.0, "ana20@gmail.com", "6543-2109", 1, 0])
    baseDeDatos.append([["Luis", "Mora", "Arias"], "2-3456-7890", 1, True, (10, 8, 1988), 80.0, "luis30@gmail.com", "7654-3210", 1, 0])
    raiz = tk.Tk()
    raiz.withdraw()
    generarReporteDonanteProvincia(raiz)
    raiz.mainloop()
