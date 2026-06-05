import tkinter as tk
from tkinter import messagebox
import pickle
import re
import random
from datetime import date

def reportes(ventanaPadre):
    """
    Funcionalidad: Abre la ventana principal de reportes.
    Entradas:
    - ventanaPadre(tk.Tk): La ventana principal del programa.
    Salidas: Ninguna.
    """
    ventana = tk.Toplevel(ventanaPadre)
    ventana.title("Reportes del Banco de Sangre")
    ventana.geometry("750x500")
    ventana.resizable(False, False)

    tk.Label(ventana, text="Reportes del Banco de Sangre", font=("Arial", 14, "bold"), fg="red").grid(row=0, column=0, columnspan=2, pady=15)
    tk.Label(ventana, text="Explicación del reporte", font=("Arial", 12, "bold")).grid(row=1, column=0, padx=20, pady=5)
    tk.Label(ventana, text="Botón", font=("Arial", 12, "bold")).grid(row=1, column=1, padx=20, pady=5)


    columnaExpl = tk.Frame(ventana)
    columnaExpl.grid(row=2, column=0, padx=20, pady=5, sticky="n")
    marcoBotones = tk.Frame(ventana)
    marcoBotones.grid(row=2, column=1, padx=20, pady=5, sticky="n")


    tk.Label(columnaExpl, text="Muestra los donantes activos de una provincia seleccionada.", width=55, anchor="w", justify="left").grid(row=0, column=0, pady=6)
    tk.Button(marcoBotones, text="Donantes por provincia", width=30, command=None).grid(row=0, column=0, padx=10, pady=5)

    tk.Label(columnaExpl, text="Muestra los donantes activos según un rango de edad.", width=55, anchor="w", justify="left").grid(row=1, column=0, pady=6)
    tk.Button(marcoBotones, text="Por rango de edad", width=30, command=None).grid(row=1, column=0, padx=10, pady=5)

    tk.Label(columnaExpl, text="Muestra donantes activos por tipo de sangre y provincia.", width=55, anchor="w", justify="left").grid(row=2, column=0, pady=6)
    tk.Button(marcoBotones, text="Por tipo de sangre y provincia", width=30, command=None).grid(row=2, column=0, padx=10, pady=5)

    tk.Label(columnaExpl, text="Muestra la lista completa de donadores registrados.", width=55, anchor="w", justify="left").grid(row=3, column=0, pady=6)
    tk.Button(marcoBotones, text="Lista completa de donadores", width=30, command=None).grid(row=3, column=0, padx=10, pady=5)

    tk.Label(columnaExpl, text="Muestra mujeres donantes O- menores de 45 años.", width=55, anchor="w", justify="left").grid(row=4, column=0, pady=6)
    tk.Button(marcoBotones, text="Mujeres donantes O-", width=30, command=None).grid(row=4, column=0, padx=10, pady=5)

    tk.Label(columnaExpl, text="Muestra a quién puede donar según el tipo de sangre.", width=55, anchor="w", justify="left").grid(row=5, column=0, pady=6)
    tk.Button(marcoBotones, text="¿A quién puede donar?", width=30, command=None).grid(row=5, column=0, padx=10, pady=5)

    tk.Label(columnaExpl, text="Muestra de quién puede recibir según el tipo de sangre.", width=55, anchor="w", justify="left").grid(row=6, column=0, pady=6)
    tk.Button(marcoBotones, text="¿De quién puede recibir?", width=30, command=None).grid(row=6, column=0, padx=10, pady=5)

    tk.Label(columnaExpl, text="Muestra los donantes no activos con su justificación completa.", width=55, anchor="w", justify="left").grid(row=7, column=0, pady=6)
    tk.Button(marcoBotones, text="Donantes no activos", width=30, command=None).grid(row=7, column=0, padx=10, pady=5)

    tk.Label(columnaExpl, text="Muestra provincias, cantidad de donadores y lugares de donación.", width=55, anchor="w", justify="left").grid(row=8, column=0, pady=6)
    tk.Button(marcoBotones, text="Lugares de donación", width=30, command=None).grid(row=8, column=0, padx=10, pady=5)

    tk.Label(columnaExpl, text="Regresa al menú principal.", width=55, anchor="w", justify="left").grid(row=9, column=0, pady=6)
    tk.Button(marcoBotones, text="Regresar", width=30, bg="red", fg="white", command=ventana.destroy).grid(row=9, column=0, padx=10, pady=5)


ventanaPrincipal = tk.Tk()
ventanaPrincipal.title("Menú principal")
ventanaPrincipal.geometry("300x200")

tk.Button(
    ventanaPrincipal,
    text="Abrir reportes",
    width=20,
    command=lambda: reportes(ventanaPrincipal)
).pack(pady=60)

ventanaPrincipal.mainloop()
