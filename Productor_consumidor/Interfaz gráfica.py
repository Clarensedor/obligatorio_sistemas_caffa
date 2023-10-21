import tkinter as tk
import threading
import queue
import time

class ProducerConsumerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Productor-Consumidor")

        self.buffer = queue.Queue(maxsize=10)
        self.stop_threads = False

        self.producer_thread = threading.Thread(target=self.producer)
        self.consumer_thread = threading.Thread(target=self.consumer)

        self.create_widgets()
    
    def create_widgets(self):
        self.start_button = tk.Button(self.root, text="Iniciar", command=self.start_threads)
        self.start_button.pack()

        self.stop_button = tk.Button(self.root, text="Detener", command=self.stop_threads)
        self.stop_button.pack()
    
        self.status_label = tk.Label(self.root, text="Esperando para iniciar...")
        self.status_label.pack()
    
    def producer(self):
        while not self.stop_threads:
            if not self.buffer.full():
                item = f"Item-{time.time()}"
                self.buffer.put(item)
                time.sleep(1)
    
    def consumer(self):
        while not self.stop_threads:
            if not self.buffer.empty():
                item = self.buffer.get()
                self.status_label["text"] = f"Consumiendo: {item}"
                self.root.update()
                time.sleep(1)
    
    def start_threads(self):
        self.producer_thread.start()
        self.consumer_thread.start()
        self.status_label["text"] = "Ejecutando productor y consumidor..."
    
    def stop_threads(self):
        self.stop_threads = True
        self.status_label["text"] = "Deteniendo..."
        self.root.update()
        self.producer_thread.join()
        self.consumer_thread.join()
        self.status_label["text"] = "Hilos detenidos."

if __name__ == "__main__":
    root = tk.Tk()
    app = ProducerConsumerApp(root)
    root.mainloop()
