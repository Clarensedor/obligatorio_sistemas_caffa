import threading
import time
import random
import tkinter as tk
import keyboard

N = 5  # Tamaño del búfer
mutex = threading.Semaphore(1)  # Semáforo para controlar el acceso a la región crítica
vacias = threading.Semaphore(N)  # Semáforo para contar ranuras vacías en el búfer
llenas = threading.Semaphore(0)  # Semáforo para contar ranuras llenas en el búfer

buffer = []  # Búfer compartido

# Variable para indicar si se debe detener el programa
detener_programa = False

def productor():
    while not detener_programa:
        elemento = producir_elemento()  # Genera un número del 1 al 5 para colocar en el búfer
        vacias.acquire()  # Disminuye la cuenta de ranuras vacías
        mutex.acquire()  # Entra a la región crítica
        insertar_elemento(elemento)  # Coloca el nuevo elemento en el búfer
        print(f"Productor inserta {elemento} en el búfer. Búfer: {buffer}")
        mutex.release()  # Sale de la región crítica
        llenas.release()  # Incrementa la cuenta de ranuras llenas

def consumidor():
    while not detener_programa:
        llenas.acquire()  # Disminuye la cuenta de ranuras llenas
        mutex.acquire()  # Entra a la región crítica
        elemento = quitar_elemento()  # Saca un elemento del búfer
        print(f"Consumidor quita {elemento} del búfer. Búfer: {buffer}")
        mutex.release()  # Sale de la región crítica
        vacias.release()  # Incrementa la cuenta de ranuras vacías
        consumir_elemento(elemento)  # Realiza alguna operación con el elemento

def producir_elemento():
    # Genera un número aleatorio del 1 al 5
    return random.randint(1, 5)

def insertar_elemento(elemento):
    # Inserta un elemento en el búfer
    buffer.append(elemento)

def quitar_elemento():
    # Saca un elemento del búfer
    return buffer.pop(0)

def consumir_elemento(elemento):
    # Realiza alguna operación con el elemento
    pass

# Crear y configurar la ventana de la interfaz gráfica
root = tk.Tk()
root.title("Productor-Consumidor")

def iniciar_programa():
    global detener_programa
    detener_programa = False
    # Crear hilos para productores y consumidores
    num_productores = 2
    num_consumidores = 3

    for _ in range(num_productores):
        threading.Thread(target=productor).start()

    for _ in range(num_consumidores):
        threading.Thread(target=consumidor).start()

    # Configuramos la función para detener el programa con la tecla "y"
    keyboard.on_press_key('y', detener_programa_con_tecla)

def detener_programa_con_tecla(e):
    global detener_programa
    if e.event_type == keyboard.KEY_DOWN:
        if e.name == 'y':
            detener_programa = True

start_button = tk.Button(root, text="Iniciar Programa", command=iniciar_programa)
start_button.pack()

stop_button = tk.Button(root, text="Detener Programa", command=detener_programa_con_tecla)
stop_button.pack()

output_text = tk.Text(root, height=10, width=50)
output_text.pack()

def actualizar_interfaz():
    while not detener_programa:
        time.sleep(1)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Búfer: {}\n".format(buffer))
        output_text.see(tk.END)

# Crear un hilo para actualizar la interfaz
threading.Thread(target=actualizar_interfaz).start()

root.mainloop()
