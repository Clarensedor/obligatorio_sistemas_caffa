import threading
import time

readers = 0
write_mutex = threading.Semaphore(1)
read_mutex = threading.Semaphore(1)
resource = 0

def reader():
    global readers
    while True:
        read_mutex.acquire()
        readers += 1
        if readers == 1:
            write_mutex.acquire()
        read_mutex.release()

        # Leer el recurso compartido
        print(f"Lector leyó: {resource}")

        read_mutex.acquire()
        readers -= 1
        if readers == 0:
            write_mutex.release()
        read_mutex.release()
        time.sleep(1)

def writer():
    while True:
        write_mutex.acquire()

        # Escribir en el recurso compartido
        global resource
        resource += 1
        print(f"Escritor escribió: {resource}")

        write_mutex.release()
        time.sleep(1)

# Crear hilos de lectores y escritores
reader_threads = [threading.Thread(target=reader) for _ in range(3)]
writer_thread = threading.Thread(target=writer)

# Iniciar los hilos
for thread in reader_threads:
    thread.start()
writer_thread.start()

# Esperar a que todos los hilos terminen
for thread in reader_threads:
    thread.join()
writer_thread.join()