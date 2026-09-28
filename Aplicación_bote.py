import json
import os 
import tkinter as tk # Libreria para el tema de las ventanas y las pestañas
from tkinter import ttk

ARCHIVO_EMPLEADOS = "empleados.json"

# Función para buscar el archivo json con los empleados guardados

def cargar_empleados():
    if not os.path.exists(ARCHIVO_EMPLEADOS):
        with open(ARCHIVO_EMPLEADOS, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=4)
    with open(ARCHIVO_EMPLEADOS, "r", encoding="utf-8") as f:
        return json.load(f)

# Permite guardar los empleados usados anteriormente

def guardar_empleados():
    with open(ARCHIVO_EMPLEADOS, "w", encoding="utf-8") as f:
        json.dump(empleados, f, ensure_ascii=False, indent=4)

# Define la ventana y las pestañas

ventana = tk.Tk() # Recuerda cerrar esta al final.
ventana.title("Gestión del bote")

notebook = ttk.Notebook(ventana)
notebook.pack(padx=10, pady=10, fill="both", expand=True)

frame_bote = ttk.Frame(notebook)
frame_empleados = ttk.Frame(notebook)
frame_reparto = ttk.Frame(notebook)

notebook.add(frame_bote, text="Contar Bote")
notebook.add(frame_empleados, text="Empleados")
notebook.add(frame_reparto, text="Reparto")

############################################################################ Contar Bote

tk.Label(frame_bote, text="Billetes y Monedas", font=("Arial", 12, "bold")).grid(row=0, columnspan=2, pady=5)

# Se permite agregar valores de dos manera. Por conteno manual de cada tipo de moneda/billetes y por contante total. Es muy común en los negocios
# hosteleros que el bote se reciba principalmente en metálico y más concretamente en monedas, por lo que es muy común que los empleados hagan las
# cuentas del bote, contando el número de monedas y luego haciendo las operaciones necesarias para conseguir los resultados.
# Este apartado pretenda facilitar esa dinámica habitual, parecida a la apertura o cierre de una caja.
# Así mismo, se permite añadir manualmente valores, por si la empresa quiere sumar o restar en un momento dado un montante.


valores = {
    "Billetes de 50€": 50,
    "Billetes de 20€": 20,
    "Billetes de 10€": 10,
    "Billetes de 5€": 5,
    "Monedas de 2€": 2,
    "Monedas de 1€": 1,
    "Monedas de 50c": 0.50,
    "Monedas de 20c": 0.20,
    "Monedas de 10c": 0.10,
    "Monedas de 5c": 0.05,
    "Monedas de 2c": 0.02,
    "Monedas de 1c": 0.01
}

entradas = {}


fila = 1
for texto, valor in valores.items():
    etiqueta = tk.Label(frame_bote, text=texto)
    etiqueta.grid(row=fila, column=0, padx=10, pady=5, sticky="w")
    entrada = tk.Entry(frame_bote, width=10)
    entrada.grid(row=fila, column=1, padx=10, pady=5)
    entradas[valor] = entrada
    fila += 1

resultado_label = tk.Label(frame_bote, text="Total: 0.00 €", font=("Arial", 14))
resultado_label.grid(row=fila+1, columnspan=2)

# Coje los valores de la tabla y los convierte en datos, hace la operación matemática para calcular el montante al pulsar el botón.

def calcular_total():
    total = 0
    for valor, entrada in entradas.items():
        cantidad = entrada.get()
        if cantidad:
            try:
                total += int(cantidad) * valor
            except ValueError:
                resultado_label.config(text="Error: solo se permiten números")
    resultado_label.config(text=f"Total: {total:.2f} €")

boton = tk.Button(frame_bote, text="Calcular Total", command=calcular_total)
boton.grid(row=fila, columnspan=2, pady=20)

############################################################################ Empleados

tk.Label(frame_empleados, text="Gestión de Empleados", font=("Arial", 12, "bold")).grid(row=0, columnspan=2, pady=5)

empleados = cargar_empleados()

tk.Label(frame_empleados, text="Nombre del empleado:").grid(row=1, column=0, sticky="w", padx=10)
entry_nombre = tk.Entry(frame_empleados)
entry_nombre.grid(row=1, column=1)

tk.Label(frame_empleados, text="Horas de contrato:").grid(row=2, column=0, sticky="w", padx=10)
entry_horas = tk.Entry(frame_empleados)
entry_horas.grid(row=2, column=1)

resultado_empleados = tk.Label(frame_empleados, text="", justify="left", font=("Arial", 10))
resultado_empleados.grid(row=5, columnspan=2, padx=10)

# Función para mostrar empleados y botones de eliminación

def mostrar_empleados():
    for widget in frame_empleados.grid_slaves():
        if int(widget.grid_info()["row"]) > 5:
            widget.destroy()

    texto = "Empleados registrados:\n"
    for i, emp in enumerate(empleados):
        texto_fila = f"- {emp['nombre']}: {emp['horas']} h/mes"
        tk.Label(frame_empleados, text=texto_fila).grid(row=6+i, column=0, sticky="w", padx=10)
        tk.Button(frame_empleados, text="Eliminar", command=lambda idx=i: eliminar_empleado(idx)).grid(row=6+i, column=1)

    resultado_empleados.config(text=texto)

# Función para agregar nuevos empleados 

def agregar_empleado():
    nombre = entry_nombre.get().strip()
    horas = entry_horas.get().strip()

    if not nombre or not horas:
        resultado_empleados.config(text="Faltan datos")
        return

    try:
        horas = int(horas)
        empleados.append({"nombre": nombre, "horas": horas})
        guardar_empleados()
        mostrar_empleados()
        entry_nombre.delete(0, tk.END)
        entry_horas.delete(0, tk.END)
    except ValueError:
        resultado_empleados.config(text="Horas debe ser un número")

# Función para eliminar empleados

def eliminar_empleado(indice):
    del empleados[indice]
    guardar_empleados()
    mostrar_empleados()

btn_agregar = tk.Button(frame_empleados, text="Agregar Empleado", command=agregar_empleado)
btn_agregar.grid(row=3, columnspan=2, pady=10)

mostrar_empleados()

############################################################################ Reparto

tk.Label(frame_reparto, text="Reparto del Bote", font=("Arial", 12, "bold")).grid(row=0, columnspan=2, pady=5)

reparto_label = tk.Label(frame_reparto, text="", justify="left", font=("Arial", 10))
reparto_label.grid(row=2, columnspan=2, padx=10)

# Función de calculo del reparto

def calcular_reparto():
    if not empleados:
        reparto_label.config(text="No hay empleados registrados.")
        return

    texto_total = resultado_label.cget("text")
    if not texto_total.startswith("Total:"):
        reparto_label.config(text="El bote no ha sido contado.")
        return

    try:
        total = float(texto_total.replace("Total:", "").replace("€", "").strip())
    except ValueError:
        reparto_label.config(text="Error leyendo el total del bote.")
        return

    total_horas = sum(emp["horas"] for emp in empleados)
    if total_horas == 0:
        reparto_label.config(text="Total de horas es 0. No se puede repartir.")
        return

    valor_hora = total / total_horas

    resultado = f"Valor de la hora de bote: {valor_hora:.2f} €\n\nReparto:\n"
    for emp in empleados:
        reparto = emp["horas"] * valor_hora
        resultado += f"- {emp['nombre']}: {reparto:.2f} €\n"

    reparto_label.config(text=resultado)

tk.Button(frame_reparto, text="Calcular Reparto", command=calcular_reparto).grid(row=1, columnspan=2, pady=5)

ventana.mainloop()