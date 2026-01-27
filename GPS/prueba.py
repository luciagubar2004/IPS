import pywifi
from pywifi import const
import joblib
import pandas as pd
import time
import threading
import tkinter as tk
from interfaz import InterfazIPS

# Cargamos el cerebro y el mapa de columnas
modelo = joblib.load('modelo_wifi.pkl')
columnas_entrenamiento = joblib.load('columnas_wifi.pkl')

def predecir(lectura_wifi):
    df_input = pd.DataFrame([-100] * len(columnas_entrenamiento)).T
    df_input.columns = columnas_entrenamiento

    # 2. Rellenamos con lo que la tarjeta de red ve ahora mismo
    for mac, señal in lectura_wifi.items():
        if mac in df_input.columns:
            df_input[mac] = señal

    # 3. Le pedimos a la IA que nos diga dónde estamos
    prediccion = modelo.predict(df_input)
    return prediccion[0]
      
def prueba(interfaz_grafica):
    wifi = pywifi.PyWiFi() #inicializamos el sistema de control WIFI
    iface = wifi.interfaces()[0] # Cogemos tarjeta de red

    print("Leyendo redes wifi...")

    try:
            while True:
                iface.scan()
                time.sleep(10)
                network = iface.scan_results()
                lectura_actual = {}
               
                for red in network:
                    # en X habiamos puesto solo el bssid y la señal
                    lectura_actual[red.bssid] = red.signal
                    # en lectura actual almacenamos todas las MACs que la tarjeta detecta ahora mismo
                
                #crea una lista solo con las macs que la IA conoce
                coincidencias = [mac for mac in lectura_actual if mac in columnas_entrenamiento] 
        
                if len(coincidencias) < 3:
                    print("AVISO: Pocas redes conocidas. Acércate a un punto de captura previo.")
                else:
                    donde_estoy = predecir(lectura_actual)
                    print(f"ESTÁS EN: {donde_estoy.upper()}")
                    # Usamos after(0, ...) para que Tkinter mueva la personita de forma segura
                    # para usar tkinter solo el hilo principal puede mover los dibujos
                    interfaz_grafica.root.after(0, interfaz_grafica.actualizar_posicion, donde_estoy)
              
                # Ahora hay que pasarle los datos a la funcion
                
    except KeyboardInterrupt:
         print("\nCaptura finalizada correctamente.")

if __name__ == "__main__":
    # Creamos la ventana principal
    root = tk.Tk() #crea la ventana vacía
    mi_interfaz = InterfazIPS(root) 
    
    # Lanzamos el escaneo en segundo plano para que la ventana no se congele
    # threading.Thread crea un hilo de ejecución en paralelo: uno para la ventana y otro para escanear el wifi
    hilo_wifi = threading.Thread(target=prueba, args=(mi_interfaz,), daemon=True)
    hilo_wifi.start()
    
    # Arrancamos la interfaz
    # bucle infinito que mantiene la ventana abierta
    root.mainloop()