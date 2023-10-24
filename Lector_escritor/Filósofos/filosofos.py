import threading
import time
import tkinter as tk

NUM_PHILOSOPHERS = 5
Num_palillos=4

class Philosopher:
    def __init__(self, name, palillo_izq, palillo_der):
        self.name = name
        self.palillo_izq = palillo_izq
        self.palillo_der = palillo_der
        self.status = "Pensando"

    def pick_palillo_izq(self):
        self.status = "Tomando tenedor izquierdo"
        self.palillo_izq.acquire()

    def pick_palillo_der(self):
        self.status = "Tomando tenedor derecho"
        self.palillo_der.acquire()

    def eat(self):
        self.status = "Comiendo"
        time.sleep(2)  # Simula el tiempo que tarda en comer
        self.palillo_izq.release()
        self.palillo_der.release()

    def think(self):
        self.status = "Pensando"
        time.sleep(1)  # Simula el tiempo que pasa pensando

def philosopher_thread(philosopher, label):
    while True:
        philosopher.think()
        philosopher.pick_palillo_izq()
        philosopher.pick_palillo_der()
        philosopher.eat()
        label.config(text=f"Filósofo {philosopher.name}: {philosopher.status}")
        root.update()

# Crear una ventana de la interfaz gráfica
root = tk.Tk()
root.title("Filósofos Comelones")

# Crear etiquetas para mostrar el estado de los filósofos
philosopher_labels = []

forks = [threading.Semaphore(1) for _ in range(NUM_PHILOSOPHERS)]
philosophers = [Philosopher(i + 1, forks[i], forks[(i + 1) % NUM_PHILOSOPHERS]) for i in range(NUM_PHILOSOPHERS)]

for philosopher in philosophers:
    philosopher_label = tk.Label(root, text=f"Filósofo {philosopher.name}: {philosopher.status}")
    philosopher_label.pack()
    philosopher_labels.append(philosopher_label)

# Crear hilos para los filósofos
threads = [threading.Thread(target=philosopher_thread, args=(philosopher, label)) for philosopher, label in zip(philosophers, philosopher_labels)]

# Iniciar los hilos
for thread in threads:
    thread.start()

root.mainloop()
