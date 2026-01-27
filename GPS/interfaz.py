import tkinter as tk
from PIL import Image, ImageTk
from collections import Counter

COORDENADAS_PB = {
    "cocina": (662, 122), 
    "salon": (219, 272),
    "comedor": (616, 310)
}
COORDENADAS_1 = {
    "habitacion 2": (161, 300), 
    "habitacion 1": (593, 301),
}

class InterfazIPS:
    def __init__(self, root):
        self.root = root
        self.root.title("Planta Baja")

        # 1. Cargar el mapa (tu dibujo)
        #self.bg_img = Image.open("planta_baja.png")
        self.img_pb = ImageTk.PhotoImage(Image.open("planta_baja.png"))
        self.img_p1 = ImageTk.PhotoImage(Image.open("primera_planta.png"))

        self.canvas = tk.Canvas(root, width=self.img_pb.width(), height=self.img_pb.height())
        self.canvas.pack()

        self.fondo= self.canvas.create_image(0, 0, anchor="nw", image=self.img_pb)

        # 2. Cargar tu PERSONITA
        self.pers_img = Image.open("user.png").resize((50, 50)) # Ajusta el tamaño aquí
        self.pers_tk = ImageTk.PhotoImage(self.pers_img)
        self.avatar = self.canvas.create_image(0, 0, image=self.pers_tk)

        self.historial = [] # Para el filtro de estabilidad
        self.planta_actual = "PB"

    def actualizar_posicion(self, habitacion_detectada):
        # Filtro de estabilidad: necesitamos 3 votos iguales para movernos
        self.historial.append(habitacion_detectada)
        if len(self.historial) > 5: self.historial.pop(0)
        
        # Tomamos la decisión final por mayoría
        posicion_estable = Counter(self.historial).most_common(1)[0][0]
        
        if posicion_estable in COORDENADAS_PB:
            if self.planta_actual != "PB":
                self.canvas.itemconfig(self.fondo, image=self.img_pb)
                self.planta_actual = "PB"               
            x, y = COORDENADAS_PB[posicion_estable]
            self.canvas.coords(self.avatar, x, y)
            
        else :
            if self.planta_actual != "P1":
                self.canvas.itemconfig(self.fondo, image=self.img_p1)
                self.planta_actual = "P1"  
            x, y = COORDENADAS_1[posicion_estable]
            self.canvas.coords(self.avatar, x, y)
        print(f"Personita movida a: {posicion_estable}")