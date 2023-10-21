import threading
import time
import random
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
    print(f"Consumidor consume {elemento}")

def detener_con_tecla():
    global detener_programa
    keyboard.read_event(suppress=True)  # Suprimir eventos anteriores
    keyboard.add_hotkey('y', lambda: setattr(detener_programa, True))

# Creamos productores y consumidores
num_productores = 2
num_consumidores = 3

for _ in range(num_productores):
    threading.Thread(target=productor).start()

for _ in range(num_consumidores):
    threading.Thread(target=consumidor).start()

# Configuramos la función para detener el programa con la tecla "y"
detener_con_tecla()

# Esperamos a que se presione la tecla "y" para detener el programa
while not detener_programa:
    time.sleep(1)

print("Programa detenido.")
