# Importa las bibliotecas necesarias
import tkinter as tk
from threading import Thread, Semaphore
import random
import time

# Definición de la clase DiningPhilosophers
class DiningPhilosophers:
    def __init__(self, number_of_philosophers, meal_size=9):
        # Inicialización de variables para cada filósofo
        self.meals = [meal_size for _ in range(number_of_philosophers)]
        self.chopsticks = [Semaphore(value=1) for _ in range(number_of_philosophers)]
        self.status = [' Pensando ' for _ in range(number_of_philosophers)]
        self.chopstick_holders = ['     ' for _ in range(number_of_philosophers)]
        self.number_of_philosophers = number_of_philosophers

    def philosopher(self, i):
        # Lógica del filósofo mientras hay comidas disponibles
        j = (i + 1) % self.number_of_philosophers
        while self.meals[i] > 0:
            self.status[i] = ' Pensando '
            time.sleep(random.random())
            self.status[i] = '  Pensando  '
            if self.chopsticks[i].acquire(timeout=1):
                self.chopstick_holders[i] = ' /   '
                time.sleep(random.random())
                if self.chopsticks[j].acquire(timeout=1):
                    self.chopstick_holders[i] = ' / \\ '
                    self.status[i] = ' Comiendo '
                    time.sleep(random.random())
                    self.meals[i] -= 1
                    self.chopsticks[j].release()
                    self.chopstick_holders[i] = ' /   '
                self.chopsticks[i].release()
                self.chopstick_holders[i] = '     '
                self.status[i] = ' Pensando '

        # Método para crear una copia del estado actual
    def copy_state(self):
        new_state = DiningPhilosophers(self.number_of_philosophers)
        new_state.meals = self.meals.copy()
        new_state.status = self.status.copy()
        new_state.chopstick_holders = self.chopstick_holders.copy()
        return new_state

# Definición de la clase DiningPhilosophersGUI
class DiningPhilosophersGUI:
    def __init__(self, master, number_of_philosophers, meal_size=9):
        # Configuración de la interfaz gráfica y variables relacionadas
        self.master = master
        self.master.title("Problema de los filósofos comensales")
        self.dining_philosophers = DiningPhilosophers(number_of_philosophers, meal_size)
        self.paused = False
        self.pause_state = None
        self.canvas = tk.Canvas(master, width=500, height=300)
        self.canvas.pack()
        self.start_button = tk.Button(master, text="Inicio", command=self.start_simulation)
        self.start_button.pack(side=tk.LEFT, padx=10)
        self.pause_button = tk.Button(master, text="Pausa", command=self.pause_simulation)
        self.pause_button.pack(side=tk.LEFT, padx=10)
        self.stop_button = tk.Button(master, text="Fin", command=self.stop_simulation)
        self.stop_button.pack(side=tk.LEFT, padx=10)
        self.status_label = tk.Label(master, text="")
        self.status_label.pack(side=tk.LEFT, padx=10)
        self.update_gui()

    # Método para iniciar la simulación
    def start_simulation(self):
        if self.paused and self.pause_state is not None:
            self.dining_philosophers = self.pause_state
            self.paused = False
            self.pause_state = None
            self.update_gui()

        philosophers = [Thread(target=self.dining_philosophers.philosopher, args=(i,)) for i in range(self.dining_philosophers.number_of_philosophers)]
        for philosopher in philosophers:
            philosopher.start()

    # Método para pausar la simulación 
    # (se tiene que presionar dos veces el botón de inicio para que reanude por completo el programa)
    def pause_simulation(self):
        self.paused = True
        self.pause_state = self.dining_philosophers.copy_state()

        for chopstick in self.dining_philosophers.chopsticks:
            chopstick.acquire()

    # Método para detener la simulación y cerrar la interfaz
    def stop_simulation(self):
        self.master.destroy()

    # Método para actualizar la interfaz gráfica durante la simulación
    def update_gui(self):
        while sum(self.dining_philosophers.meals) > 0 and not self.paused:
            self.status_label.config(text="Comidas que quedan {}".format(sum(self.dining_philosophers.meals)))
            self.draw_philosophers()
            self.print_data()
            self.master.update()
            time.sleep(0.1)
        if not self.paused:
            self.print_data()
            self.master.destroy()

    # Método para dibujar los filósofos en la interfaz gráfica
    def draw_philosophers(self):
        self.canvas.delete("all")
        x = 50
        y = 150
        for i in range(self.dining_philosophers.number_of_philosophers):
            status = self.dining_philosophers.status[i]
            self.canvas.create_text(x, y, text=status, font=("Helvetica", 12))
            x += 80

    # Método para imprimir datos en la terminal durante la simulación
    def print_data(self):
        print("=" * (self.dining_philosophers.number_of_philosophers * 5))
        print("".join(map(str, self.dining_philosophers.status)), " : ",
              str(self.dining_philosophers.status.count(' Comiendo ')))
        print("".join(map(str, self.dining_philosophers.chopstick_holders)))
        print("".join("{:3d}  ".format(m) for m in self.dining_philosophers.meals), " : ",
              str(sum(self.dining_philosophers.meals)))

# Función principal para iniciar la simulación
def main():
    n = 5
    m = 7
    root = tk.Tk()
    gui = DiningPhilosophersGUI(root, n, m)
    root.mainloop()

# Verifica si el script se ejecuta directamente y llama a la función main en ese caso
if __name__ == "__main__":
    main()
