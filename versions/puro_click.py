import time
import threading
import random
import pynput.mouse
import pynput.keyboard

# Variables globales
target_x = 0
target_y = 0
target_coords_set = threading.Event()
autoclick_running = True

# Función para capturar las coordenadas cuando se hace clic en la pantalla
def on_click(x, y, button, pressed):
    global target_x, target_y, target_coords_set
    if pressed:
        target_x = x
        target_y = y
        target_coords_set.set()

# Función para detener el autoclicker
def stop_autoclick():
    global autoclick_running
    autoclick_running = False

# Función para capturar la tecla presionada
def on_key_press(key):
    if key == pynput.keyboard.Key.esc:
        stop_autoclick()

# Define la función que simulará el clic
def click_mouse(x, y):
    mouse_controller = pynput.mouse.Controller()
    mouse_controller.position = (x, y)
    mouse_controller.click(pynput.mouse.Button.left)

# Define la función para hacer clic continuamente
def autoclicker(interval):
    global target_x, target_y, target_coords_set, autoclick_running
    while autoclick_running:
        target_coords_set.wait()
        click_mouse(target_x, target_y)
        sleep_interval = interval + random.uniform(-0.1, 0.1)
        time.sleep(sleep_interval)

# Crea y comienza un hilo para el autoclicker
autoclick_thread = threading.Thread(target=autoclicker, args=(0.5,))
autoclick_thread.start()

# Configura el detector de clics del mouse
mouse_listener = pynput.mouse.Listener(on_click=on_click)
mouse_listener.start()

# Configura el detector de teclado
keyboard_listener = pynput.keyboard.Listener(on_press=on_key_press)
keyboard_listener.start()

# Espera a que el usuario presione Esc para detener el autoclicker
print("Presione Esc para detener el autoclicker...")
keyboard_listener.join()
mouse_listener.stop()
autoclick_thread.join()
