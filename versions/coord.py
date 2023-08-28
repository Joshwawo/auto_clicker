import time
import threading
import random
import pynput.mouse

# Define la función que simulará el clic
def click_mouse(x, y):
    mouse_controller = pynput.mouse.Controller()
    mouse_controller.position = (x, y)
    mouse_controller.click(pynput.mouse.Button.left)

# Define la función para hacer clic continuamente
def autoclicker(interval, x, y):
    while True:
        click_mouse(x, y)
        sleep_interval = interval + random.uniform(-0.1, 0.1)  # Introduce algo de variabilidad en el intervalo
        time.sleep(sleep_interval)

# Pide al usuario las coordenadas del clic y el intervalo de clic
target_x = int(input("Ingrese la coordenada X del clic: "))
target_y = int(input("Ingrese la coordenada Y del clic: "))
click_interval = float(input("Ingrese el intervalo de clic (segundos): "))

# Crea y comienza un hilo para el autoclicker
autoclick_thread = threading.Thread(target=autoclicker, args=(click_interval, target_x, target_y))
autoclick_thread.start()

# Espera a que el usuario presione Enter para detener el autoclicker
input("Presione Enter para detener el autoclicker...")
autoclick_thread.join()
