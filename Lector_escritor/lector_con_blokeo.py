import threading
import time
import queue

mutex = threading.Semaphore(1)  # controla el acceso a 'cl'
bd = threading.Semaphore(1)     # controla el acceso a la base de datos
cl = 0                           # número de procesos que leen o desean hacerlo

cola_lectores = queue.Queue()
cola_escritores = queue.Queue()

def leer_base_de_datos(identificador):
    # Lógica para acceder y leer la base de datos
    print(f"Lector {identificador} leyendo la base de datos")

def usar_lectura_datos(identificador):
    # Lógica para usar los datos leídos
    print(f"Lector {identificador} usando los datos leídos")

def escribir_base_de_datos(identificador):
    # Lógica para escribir en la base de datos
    print(f"Escritor {identificador} escribiendo en la base de datos")

def lector(identificador):
    global cl
    while True:
        with mutex:
            cl += 1
            if cl == 1:
                bd.acquire()
        mutex.release()

        leer_base_de_datos(identificador)

        with mutex:
            cl -= 1
            if cl == 0:
                bd.release()
                if not cola_lectores.empty():
                    siguiente_lector = cola_lectores.get()
                    siguiente_lector.release()

        usar_lectura_datos(identificador)
        time.sleep(1)

def escritor(identificador):
    while True:
        cola_escritores.put(threading.Semaphore(0))  # Agrega el escritor a la cola
        bd.acquire()

        if not cola_escritores.empty():
            siguiente_escritor = cola_escritores.get()
            siguiente_escritor.release()
        else:
            bd.release()

        escribir_base_de_datos(identificador)
        time.sleep(1)  # Simula un tiempo de procesamiento

# Crear hilos de lectores y escritores
lectores_threads = [threading.Thread(target=lector, args=(i,)) for i in range(5)]  # Cinco lectores
escritores_threads = [threading.Thread(target=escritor, args=(i,)) for i in range(5)]  # Cinco escritores

# Iniciar los hilos
for lector_thread in lectores_threads:
    lector_thread.start()

for escritor_thread in escritores_threads:
    escritor_thread.start()
