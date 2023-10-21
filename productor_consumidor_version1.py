import threading
import time
import random

N = 5  # Tamaño del búfer
mutex = threading.Semaphore(1)  # Semáforo para controlar el acceso a la región crítica
vacias = threading.Semaphore(N)  # Semáforo para contar ranuras vacías en el búfer
llenas = threading.Semaphore(0)  # Semáforo para contar ranuras llenas en el búfer

buffer = []  # Búfer compartido

def productor():
    while True:
        elemento = producir_elemento()  # Genera un elemento para colocar en el búfer
        vacias.acquire()  # Disminuye la cuenta de ranuras vacías
        mutex.acquire()  # Entra a la región crítica
        insertar_elemento(elemento)  # Coloca el nuevo elemento en el búfer
        mutex.release()  # Sale de la región crítica
        llenas.release()  # Incrementa la cuenta de ranuras llenas

def consumidor():
    while True:
        llenas.acquire()  # Disminuye la cuenta de ranuras llenas
        mutex.acquire()  # Entra a la región crítica
        elemento = quitar_elemento()  # Saca un elemento del búfer
        mutex.release()  # Sale de la región crítica
        vacias.release()  # Incrementa la cuenta de ranuras vacías
        consumir_elemento(elemento)  # Realiza alguna operación con el elemento

def producir_elemento():
    # Genera un elemento
    return "Elementito"

def insertar_elemento(elemento):
    # Inserta un elemento en el búfer
    buffer.append(elemento)

def quitar_elemento():
    # Saca un elemento del búfer
    return buffer.pop(0)

def consumir_elemento(elemento):
    # Realiza alguna operación con el elemento
    print(f"Consumidor consume {elemento}")

# Creamos productores y consumidores
num_productores = 2
num_consumidores = 3

for _ in range(num_productores):
    threading.Thread(target=productor).start()

for _ in range(num_consumidores):
    threading.Thread(target=consumidor).start()