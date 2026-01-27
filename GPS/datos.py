import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier as knn
from sklearn.metrics import accuracy_score
import joblib
from sklearn.ensemble import RandomForestClassifier

# 1. Cargamos los datos
df = pd.read_csv('dataset_networks.csv', names=['room', 'bssid', 'signal', 'ssid', 'frequency'])
# 2. El reto: Como no pusimos un "ID de escaneo", vamos a agrupar los datos 
# para que cada fila sea una habitación y sus señales.
df['scan_id']=((df.groupby(['room', 'bssid'])).cumcount())
# pivot_table tiene parametros como index, columns, y values 
df_pivot = df.pivot_table(index=['room', 'scan_id'],
                          columns='bssid',
                          values = 'signal')
# para poner un valor en los huecos
df_final= df_pivot.fillna(-100)

df_final= df_final.reset_index()


# y es la columna room
# x son las señales wifi
y = df_final['room']
print(y.head())
# quitamos las columnas room y scan_id con drop
X = df_final.drop(columns=['room', 'scan_id'])

print("Dimensiones de X (Pistas):", X.shape)
# 472 escaneos, 65 señales de routers
print("Dimensiones de y (Respuesta):", y.shape)
# 472 escaneos

# Dividimos: 80% para aprender, 20% para el examen final
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

modelo = RandomForestClassifier(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)

print("¡Modelo entrenado con éxito!")

predicciones = modelo.predict(X_test)
nota = accuracy_score(y_test, predicciones)
print(f"La precisión de mi IA es: {nota * 100}%")

#ahora vamos a congelar el modelo
# Guardamos el modelo entrenado
joblib.dump(modelo, 'modelo_wifi.pkl')

# Guardamos la lista de columnas (MACs) para que el orden sea siempre el mismo
joblib.dump(X.columns, 'columnas_wifi.pkl')

print("¡Modelo y columnas guardados en archivos .pkl!")