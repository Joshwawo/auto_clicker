import time
import threading
import random
import pynput.mouse
import pynput.keyboard
import pyautogui

# Variables globales
target_x = 0
target_y = 0
target_coords_set = threading.Event()
autoclick_running = True
click_interval = 0.5

# Función para capturar las coordenadas cuando se hace clic en la pantalla
def on_click(x, y, button, pressed):
    global target_x, target_y, target_coords_set
    if pressed:
        target_x = x
        target_y = y
        print(f"Clic en coordenadas: ({x}, {y}) - Intervalo: {click_interval:.2f} segundos")
        target_coords_set.set()

# Función para reactivar el autoclicker
def reactivate_autoclick():
    global autoclick_running
    autoclick_running = True
    autoclick_thread = threading.Thread(target=autoclicker, args=(click_interval,))
    autoclick_thread.start()

# Función para detener el autoclicker
def stop_autoclick():
    print("Deteniendo autoclicker...")
    global autoclick_running
    autoclick_running = False
# Funcion para cambiar el intervalo de tiempo
def change_interval(key):
    if key == pynput.keyboard.Key.esc:
        stop_autoclick()
    elif key == pynput.keyboard.KeyCode.from_char('1'):
        stop_autoclick()
        print("Cambiando intervalo de tiempo...")
        global click_interval
        click_interval = get_click_interval()
        print(f"Nuevo intervalo de tiempo: {click_interval:.2f} segundos")
        reactivate_autoclick()

# Función para capturar la tecla presionada
def on_key_press(key):
    if key == pynput.keyboard.Key.esc:
        stop_autoclick()
    elif key == pynput.keyboard.KeyCode.from_char('0'):
        reactivate_autoclick()
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

# Función para obtener el tiempo de intervalo desde el usuario
def get_click_interval():
    while True:
        try:
            interval = float(input("Introduce el tiempo de intervalo (en segundos): "))
            if interval > 0:
                return interval
            else:
                print("Por favor, introduce un valor positivo.")
        except ValueError:
            print("Por favor, introduce un valor numérico válido.")

# Obtén el tiempo de intervalo del usuario
click_interval = get_click_interval()

# Crea y comienza un hilo para el autoclicker
autoclick_thread = threading.Thread(target=autoclicker, args=(click_interval,))
autoclick_thread.start()

# Configura el detector de clics del mouse
mouse_listener = pynput.mouse.Listener(on_click=on_click)
mouse_listener.start()

# Configura el detector de teclado
keyboard_listener = pynput.keyboard.Listener(on_press=on_key_press)
keyboard_listener.start()

# Configura el detector de teclado para cambiar el intervalo de tiempo
keyboard_listener = pynput.keyboard.Listener(on_press=change_interval)
keyboard_listener.start()

# Función para superponer coordenadas en la pantalla
def show_coordinates():
    while True:
        if target_coords_set.is_set():
            x, y = pyautogui.position()
            pyautogui.alert(f"Coordenadas: ({x}, {y})")
            target_coords_set.clear()

# Crea y comienza un hilo para superponer coordenadas
show_coordinates_thread = threading.Thread(target=show_coordinates)
show_coordinates_thread.start()

# Espera a que el usuario presione Esc para detener el autoclicker
print("Presione Esc para detener el autoclicker...")
keyboard_listener.join()
mouse_listener.stop()
autoclick_thread.join()
show_coordinates_thread.join()


# Path: main.py
# Requieremnts
# pip install pynput
# pip install pyautogui

# Run
# python main.py
