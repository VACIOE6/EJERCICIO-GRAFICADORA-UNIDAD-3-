import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib import pyplot
from matplotlib.animation import FuncAnimation
from random import randrange
import numpy as np
from tkinter import *
from tkinter import ttk, messagebox
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

root = Tk()
root.title("Grafica de funciones")
root.geometry("900x800")
root.config(bd=15)

fig, ax = plt.subplots()

# Función para evaluar la expresión matemática ingresada
def evaluate(expression, x):
    return eval(expression)

# Función para graficar la función ingresada
def plot_function(expression):
    x = np.linspace(-10, 10, 1000)
    y = evaluate(expression, x)
    ax.plot(x, y, color='blue')

# Función para resolver la ecuación ingresada mediante el método de bisección
def solve_equation(expression, a, b, tolera):
    fx = lambda x: evaluate(expression, x)
    tramo = b-a
    fa = fx(a)
    fb = fx(b)
    i = 1
    tabla = []
    while (tramo>tolera):
        c = (a+b)/2
        fc = fx(c)
        tabla.append([i,a,c,b,fa,fc,fb,tramo])
        i = i + 1
        cambia = np.sign(fa)*np.sign(fc)
        if (cambia<0):
            b = c
            fb = fc
        else:
            a=c
            fa = fc
        tramo = b-a
    c = (a+b)/2
    fc = fx(c)
    tabla.append([i,a,c,b,fa,fc,fb,tramo])
    tabla = np.array(tabla)
    raiz = c
    return raiz, tabla

# Función para graficar la tabla de bisección
def plot_table(tabla):
    xi = tabla[:,2]
    yi = tabla[:,5]
    orden = np.argsort(xi)
    xi = xi[orden]
    yi = yi[orden]
    plt.plot(xi,yi)
    plt.plot(xi,yi,'o')
    plt.axhline(0, color="black")

# Función para graficar la función, resolver la ecuación y mostrar la tabla de bisección
def plot(expression, a, b, tolera):
    ax.clear()
    plot_function(expression)
    raiz, tabla = solve_equation(expression, a, b, tolera)
    plot_table(tabla)
    canvas.draw()
    return raiz, tabla

# Crear los widgets de la interfaz gráfica
Label(root, text="Función").place(x=10, y=550)
funcion = Entry(root, justify="center")
funcion.place(x=70, y=550)
Label(root, text="Límite inferior").place(x=10, y=580)
a = Entry(root, justify="center")
a.place(x=105, y=580)
Label(root, text="Límite superior").place(x=10, y=610)
b = Entry(root, justify="center")
b.place(x=105, y=610)
Label(root, text="Tolerancia").place(x=10, y=640)
tolera = Entry(root, justify="center")
tolera.place(x=80, y=640)

def handle_plot_button1():
    expression = funcion.get()
    a_value = float(a.get())
    b_value = float(b.get())
    tolera_value = float(tolera.get())
    raiz, tabla = plot(expression, a_value, b_value, tolera_value)
    messagebox.showinfo("Resultado", f"La raiz es: {raiz}")

def handle_clear_button():
    funcion.delete(0, END)
    a.delete(0, END)
    b.delete(0, END)
    tolera.delete(0, END)
    ax.clear()
    canvas.draw()

plot_button = Button(root, text="Graficar", command=handle_plot_button1)
plot_button.place(x=10, y=670)

clear_button = Button(root, text="Borrar", command=handle_clear_button)
clear_button.place(x=100, y=670)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().place(x=200, y=10, width=680, height=500)

toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas.get_tk_widget().pack()

root.mainloop()
