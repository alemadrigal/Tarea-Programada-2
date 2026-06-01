# Elaborado por: Alejandro Madrigal y Brandon Meza
# Fecha de creacion: 30/05/2026
# Ultima modificacion: 30/05/2026
# Version de Python: 3.11

import tkinter as tk
from tkinter import messagebox
import random

# =========================================================
# Tupla global con los tipos de sangre
tiposDeSangre = ("O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-")

# Lista global que funciona como matriz de donadores
baseDeDatos = []
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


def generarFechaAleatoria(esDonador):
    """
    Funcionalidad: Genera una fecha de nacimiento aleatoria. Si es donador
                   genera una fecha que resulte en mayor de edad (18-65 anos),
                   si no es donador puede ser menor de edad.
    Entradas:
        - esDonador(bool): True si debe ser mayor de edad, False si puede ser menor.
    Salidas:
        - fecha(tuple): Tupla con (dia, mes, anio) de la fecha generada.
    """
    if esDonador:
        anio = random.randint(1960, 2006)
    else:
        anio = random.randint(2010, 2020)

    mes = random.randint(1, 12)
    dia = random.randint(1, 28)
    return (dia, mes, anio)


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


# =========================================================
# Prueba rapida de la ventana
if __name__ == "__main__":
    raiz = tk.Tk()
    raiz.withdraw()
    generarDonadores(raiz)
    raiz.mainloop()
