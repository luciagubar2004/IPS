import pywifi
from pywifi import const
import time
import csv
from datetime import datetime

def guardar_datos_csv():
    wifi = pywifi.PyWiFi() #inicializamos el sistema de control WIFI
    iface = wifi.interfaces()[0] # Cogemos tarjeta de red

    # Nombre del archivo donde guardaremos la "inteligencia"
    archivo_csv = "dataset_networks.csv"
    
    print("¿En qué habitación estás?:")
    label = input()
    print("Leyendo redes wifi...")

    with open(archivo_csv, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Si el archivo está vacío, escribimos las cabeceras
        if f.tell() == 0:
            writer.writerow(["Target","BSSID", "Signal_dBm", "SSID", "Frecuencia_MHz"])

        try:
            for i in range(50):
                iface.scan()
                time.sleep(2)
                network = iface.scan_results()
                
                for red in network:
                    # Guardamos la fila de datos
                    writer.writerow([label, red.bssid, red.signal, red.ssid, red.freq])
                
                f.flush() # Asegura que se escribe en el disco
                time.sleep(2) # Escaneamos cada 5 segundos
                print(f"\nEscaneo {i}")
        except KeyboardInterrupt:
            print("\nCaptura finalizada correctamente.")

if __name__ == "__main__":
    guardar_datos_csv()