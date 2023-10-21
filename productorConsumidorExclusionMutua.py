import threading
import time
import random

# Número de lugares de almacenamiento disponibles
NUM_PLACES = 5

# Lista para representar el almacén
almacen = []

# Candado para garantizar exclusión mutua
mutex = threading.Lock()

# Función del productor (camión)
def productor(camion_id):
    while True:
        producto = f"Producto-{random.randint(1, 100)}"
        print(f"Camión-{camion_id} llega al almacén con {producto}")
        
        with mutex:
            if len(almacen) < NUM_PLACES:
                almacen.append(producto)
                print(f"Camión-{camion_id} ha cargado {producto} en el almacén")
            else:
                print(f"Camión-{camion_id} se va porque el almacén está lleno")
        
        time.sleep(random.uniform(0.1, 0.5))

# Función del consumidor (trabajador del almacén)
def consumidor(trabajador_id):
    while True:
        with mutex:
            if almacen:
                producto = almacen.pop(0)
                print(f"Trabajador-{trabajador_id} descarga {producto} del almacén")
            else:
                print(f"El almacén está vacío. Trabajador-{trabajador_id} espera")
        
        time.sleep(random.uniform(0.1, 0.5))

# Creamos camiones y trabajadores del almacén
num_camiones = 3
num_trabajadores = 2

for i in range(num_camiones):
    threading.Thread(target=productor, args=(i,)).start()

for j in range(num_trabajadores):
    threading.Thread(target=consumidor, args=(j,)).start()
