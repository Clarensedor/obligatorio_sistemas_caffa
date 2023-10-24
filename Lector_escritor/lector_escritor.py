import threading
import time
import tkinter as tk

readers = 0
write_mutex = threading.Semaphore(1)
read_mutex = threading.Semaphore(1)
resource = 0

def reader(reader_num):
    global readers
    while True:
        read_mutex.acquire()
        readers += 1
        if readers == 1:
            write_mutex.acquire()
        read_mutex.release()

        # Leer el recurso compartido
        print(f"Lector {reader_num} leyó: {resource}")

        resource_label.config(text=f"Lector leyó: {resource}")
        root.update()  # Actualiza la interfaz gráfica

        read_mutex.acquire()
        readers -= 1
        if readers == 0:
            write_mutex.release()
        read_mutex.release()
        time.sleep(1)

def writer(writer_num):
    while True:
        write_mutex.acquire()

        # Escribir en el recurso compartido
        global resource
        resource += 1
        print(f"Escritor {writer_num} escribió: {resource}")

        resource_label.config(text=f"Escritor escribió: {resource}")
        root.update()  # Actualiza la interfaz gráfica

        write_mutex.release()
        time.sleep(1)

# Crear una ventana de la interfaz gráfica
root = tk.Tk()
root.title("Lectores y Escritores")

# Crear etiquetas para mostrar la información
resource_label = tk.Label(root, text="")
resource_label.pack()

# Crear hilos de lectores y escritores
reader_threads = [threading.Thread(target=reader, args=(i + 1,)) for i in range(3)]
writer_thread = threading.Thread(target=writer, args=(1,))

# Iniciar los hilos
for thread in reader_threads:
    thread.start()
writer_thread.start()

root.mainloop()  # Inicia el bucle de la interfaz gráfica
