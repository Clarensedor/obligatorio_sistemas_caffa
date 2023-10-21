import threading
import time
import random
from queue import Queue

# Número de lugares de almacenamiento disponibles
NUM_PLACES = 5

# Creamos una cola compartida para representar los lugares de almacenamiento
almacen = Queue(NUM_PLACES)

# Función del productor (camión)
def productor(camion_id):
    while True:
        producto = f"Producto-{random.randint(1, 100)}"
        print(f"Camión-{camion_id} llega al almacén con {producto}")
        almacen.put(producto)
        print(f"Camión-{camion_id} ha cargado {producto} en el almacén")
        time.sleep(random.uniform(0.1, 0.5))

# Función del consumidor (trabajador del almacén)
def consumidor(trabajador_id):
    while True:
        producto = almacen.get()
        print(f"Trabajador-{trabajador_id} descarga {producto} del almacén")
        almacen.task_done()
        time.sleep(random.uniform(0.1, 0.5))

# Creamos camiones y trabajadores del almacén
num_camiones = 3
num_trabajadores = 2

for i in range(num_camiones):
    threading.Thread(target=productor, args=(i,)).start()

for j in range(num_trabajadores):
    threading.Thread(target=consumidor, args=(j,)).start()
