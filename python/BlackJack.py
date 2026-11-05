# Importamos la librería tkinter para crear la interfaz gráfica (ventanas, botones, etiquetas)
import tkinter as tk
# Importamos messagebox para mostrar avisos emergentes (al ganar, perder o empatar)
from tkinter import messagebox
# Importamos la librería random para barajar el mazo de cartas de forma aleatoria
import random

# Definimos los palos de la baraja
PALOS = ['♠', '♥', '♦', '♣']
# Definimos los valores posibles de las cartas (2 al 10, J, Q, K, A)
VALORES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

# Definimos la clase principal que controlará la lógica del juego y la interfaz
class BlackjackApp:
    # Método constructor que se ejecuta automáticamente al instanciar la clase
    def __init__(self, ventana):
        # Guardamos la ventana principal creada por Tkinter en la variable de instancia self.ventana
        self.ventana = ventana
        # Establecemos el título de la ventana
        self.ventana.title("Blackjack - Juego de Cartas")
        # Definimos las dimensiones de la ventana en píxeles (ancho x alto)
        self.ventana.geometry("700x550")
        # Establecemos un color de fondo verde oscuro (típico de mesa de casino)
        self.ventana.configure(bg="#076324")

        # Inicializamos el mazo de cartas como una lista vacía
        self.mazo = []
        # Inicializamos la mano del jugador como una lista vacía
        self.mano_jugador = []
        # Inicializamos la mano de la banca (crupier) como una lista vacía
        self.mano_banca = []

        # Creamos los elementos visuales de la interfaz llamando a su función dedicada
        self.crear_widgets()
        # Iniciamos una nueva partida configurando el mazo y las manos iniciales
        self.iniciar_partida()

    # Método encargado de crear todos los componentes gráficos (textos, paneles y botones)
    def crear_widgets(self):
        # Creamos el título superior del juego con estilo tipográfico y fondo verde
        self.label_titulo = tk.Label(self.ventana, text="♣ BLACKJACK 21 ♠", font=("Helvetica", 20, "bold"), bg="#076324", fg="gold")
        # Empaquetamos (colocamos) el título en la parte superior con un margen vertical
        self.label_titulo.pack(pady=10)

        # Creamos un marco (contenedor) visual para la zona de la Banca
        self.frame_banca = tk.LabelFrame(self.ventana, text=" Banca ", font=("Helvetica", 12, "bold"), bg="#076324", fg="white", bd=2)
        # Empaquetamos el marco de la banca expandiéndolo horizontalmente
        self.frame_banca.pack(fill="both", expand="yes", padx=20, pady=5)

        # Etiqueta para mostrar las cartas físicas que tiene la Banca
        self.label_cartas_banca = tk.Label(self.frame_banca, text="", font=("Courier", 16, "bold"), bg="#076324", fg="white")
        # La colocamos dentro del marco de la banca
        self.label_cartas_banca.pack(pady=5)

        # Etiqueta para mostrar la puntuación acumulada de la Banca
        self.label_puntos_banca = tk.Label(self.frame_banca, text="Puntos: ?", font=("Helvetica", 11), bg="#076324", fg="lightgray")
        # La colocamos debajo de las cartas de la banca
        self.label_puntos_banca.pack(pady=5)

        # Creamos un marco (contenedor) visual para la zona del Jugador
        self.frame_jugador = tk.LabelFrame(self.ventana, text=" Jugador ", font=("Helvetica", 12, "bold"), bg="#076324", fg="white", bd=2)
        # Empaquetamos el marco del jugador expandiéndolo horizontalmente
        self.frame_jugador.pack(fill="both", expand="yes", padx=20, pady=5)

        # Etiqueta para mostrar las cartas físicas que tiene el Jugador
        self.label_cartas_jugador = tk.Label(self.frame_jugador, text="", font=("Courier", 16, "bold"), bg="#076324", fg="white")
        # La colocamos dentro del marco del jugador
        self.label_cartas_jugador.pack(pady=5)

        # Etiqueta para mostrar la puntuación acumulada del Jugador
        self.label_puntos_jugador = tk.Label(self.frame_jugador, text="Puntos: 0", font=("Helvetica", 11), bg="#076324", fg="lightgray")
        # La colocamos debajo de las cartas del jugador
        self.label_puntos_jugador.pack(pady=5)

        # Creamos un marco sin bordes para agrupar horizontalmente los botones de acción
        self.frame_botones = tk.Frame(self.ventana, bg="#076324")
        # Empaquetamos el marco de botones en la parte inferior de la ventana
        self.frame_botones.pack(pady=15)

        # Botón 'Pedir Carta': al pulsar ejecuta el método self.pedir_carta
        self.btn_pedir = tk.Button(self.frame_botones, text="Pedir Carta", font=("Helvetica", 11, "bold"), bg="#2196F3", fg="white", width=12, command=self.pedir_carta)
        # Colocamos el botón en la rejilla interna a la izquierda
        self.btn_pedir.grid(row=0, column=0, padx=10)

        # Botón 'Plantarse': al pulsar ejecuta el método self.plantarse
        self.btn_plantar = tk.Button(self.frame_botones, text="Plantarse", font=("Helvetica", 11, "bold"), bg="#f44336", fg="white", width=12, command=self.plantarse)
        # Colocamos el botón en la rejilla interna al centro
        self.btn_plantar.grid(row=0, column=1, padx=10)

        # Botón 'Nueva Partida': al pulsar ejecuta el método self.iniciar_partida
        self.btn_reiniciar = tk.Button(self.frame_botones, text="Nueva Partida", font=("Helvetica", 11, "bold"), bg="#4CAF50", fg="white", width=12, command=self.iniciar_partida)
        # Colocamos el botón en la rejilla interna a la derecha
        self.btn_reiniciar.grid(row=0, column=2, padx=10)

    # Método encargado de reiniciar las variables y comenzar un juego nuevo
    def iniciar_partida(self):
        # Creamos una lista de diccionarios representando las 52 cartas posibles mezclando valores y palos
        self.mazo = [{'valor': v, 'palo': p} for p in PALOS for v in VALORES]
        # Barajamos las cartas aleatoriamente
        random.shuffle(self.mazo)

        # Repartimos 2 cartas al jugador extrayéndolas del mazo con pop()
        self.mano_jugador = [self.mazo.pop(), self.mazo.pop()]
        # Repartimos 2 cartas a la banca extrayéndolas del mazo con pop()
        self.mano_banca = [self.mazo.pop(), self.mazo.pop()]

        # Habilitamos el botón de Pedir Carta por si estaba deshabilitado
        self.btn_pedir.config(state=tk.NORMAL)
        # Habilitamos el botón de Plantarse por si estaba deshabilitado
        self.btn_plantar.config(state=tk.NORMAL)

        # Actualizamos la pantalla indicando que aún es el turno activo del jugador (ocultando 1 carta de la banca)
        self.actualizar_interfaz(ocultar_banca=True)

        # Comprobamos si el jugador ha obtenido Blackjack directo (21 puntos) en el primer reparto
        if self.calcular_puntos(self.mano_jugador) == 21:
            # Notificamos al jugador que ha obtenido Blackjack
            messagebox.showinfo("¡Blackjack!", "¡Conseguiste 21 puntos en el reparto inicial!")
            # Automáticamente ejecutamos el turno de la banca
            self.plantarse()

    # Método para calcular los puntos totales de cualquier mano de cartas
    def calcular_puntos(self, mano):
        # Inicializamos los puntos totales en 0
        puntos = 0
        # Contador para registrar cuántos Ases hay en la mano (ya que pueden valer 11 o 1)
        ases = 0

        # Recorremos cada carta dentro de la mano proporcionada
        for carta in mano:
            # Guardamos el valor de la carta actual
            v = carta['valor']
            # Si la carta es J, Q o K suma 10 puntos
            if v in ['J', 'Q', 'K']:
                puntos += 10
            # Si la carta es un As (A), suma temporalmente 11 puntos e incrementamos el contador de ases
            elif v == 'A':
                puntos += 11
                ases += 1
            # Si la carta es numérica (2 al 10), la convertimos a entero y la sumamos
            else:
                puntos += int(v)

        # Si superamos los 21 puntos y tenemos Ases contados como 11, ajustamos reduciendo cada As a 1 punto (-10)
        while puntos > 21 and ases > 0:
            puntos -= 10
            ases -= 1

        # Retornamos el total final calculado de puntos
        return puntos

    # Método para refrescar y renderizar visualmente las cartas y puntuaciones
    def actualizar_interfaz(self, ocultar_banca=True):
        # Dibuja visualmente las cartas del jugador concatenándolas en un string
        str_jugador = "  ".join([f"[{c['valor']}{c['palo']}]" for c in self.mano_jugador])
        # Asigna el string con las cartas al texto del elemento visual del jugador
        self.label_cartas_jugador.config(text=str_jugador)
        # Calcula y muestra los puntos actuales acumulados por el jugador
        self.label_puntos_jugador.config(text=f"Puntos: {self.calcular_puntos(self.mano_jugador)}")

        # Si estamos en el turno del jugador (ocultar_banca es True)
        if ocultar_banca:
            # Mostramos únicamente la primera carta de la banca y ocultamos la segunda con [ ? ]
            str_banca = f"[{self.mano_banca[0]['valor']}{self.mano_banca[0]['palo']}]  [ ? ]"
            # Actualizamos el elemento visual de las cartas de la banca
            self.label_cartas_banca.config(text=str_banca)
            # Ocultamos la puntuación real de la banca mostrando un signo de interrogación
            self.label_puntos_banca.config(text="Puntos: ?")
        # Si la banca está jugando o se ha terminado la partida (ocultar_banca es False)
        else:
            # Dibuja visualmente TODAS las cartas de la banca de manera visible
            str_banca = "  ".join([f"[{c['valor']}{c['palo']}]" for c in self.mano_banca])
            # Actualizamos el elemento visual con la mano completa descubierta
            self.label_cartas_banca.config(text=str_banca)
            # Calcula y muestra la puntuación real completa acumulada por la banca
            self.label_puntos_banca.config(text=f"Puntos: {self.calcular_puntos(self.mano_banca)}")

    # Método que se activa al presionar el botón 'Pedir Carta'
    def pedir_carta(self):
        # Sacamos la carta superior del mazo y se la añadimos a la mano del jugador
        self.mano_jugador.append(self.mazo.pop())
        # Refrescamos la pantalla mostrando la nueva carta del jugador
        self.actualizar_interfaz(ocultar_banca=True)

        # Comprobamos si el jugador se ha pasado de 21 puntos al pedir la carta
        if self.calcular_puntos(self.mano_jugador) > 21:
            # Desvelamos la mano completa de la banca
            self.actualizar_interfaz(ocultar_banca=False)
            # Deshabilitamos el botón de pedir carta
            self.btn_pedir.config(state=tk.DISABLED)
            # Deshabilitamos el botón de plantarse
            self.btn_plantar.config(state=tk.DISABLED)
            # Lanzamos una ventana emergente avisando que el jugador ha perdido
            messagebox.showerror("¡Te has pasado!", "Has superado los 21 puntos. ¡Gana la banca!")

    # Método que se activa al presionar el botón 'Plantarse'
    def plantarse(self):
        # Deshabilitamos los botones de pedir y plantarse para evitar más acciones en la ronda
        self.btn_pedir.config(state=tk.DISABLED)
        self.btn_plantar.config(state=tk.DISABLED)

        # Regla del crupier: La banca está obligada a pedir carta mientras tenga menos de 17 puntos
        while self.calcular_puntos(self.mano_banca) < 17:
            # Extraemos una carta del mazo y se la asignamos a la banca
            self.mano_banca.append(self.mazo.pop())

        # Revelamos en la interfaz todas las cartas y puntuaciones finales sin ocultar nada
        self.actualizar_interfaz(ocultar_banca=False)
        # Evaluamos el resultado final comparando puntos de ambas manos
        self.determinar_ganador()

    # Método que evalúa las puntuaciones finales y determina el resultado del juego
    def determinar_ganador(self):
        # Obtenemos el total de puntos obtenidos por el jugador
        puntos_j = self.calcular_puntos(self.mano_jugador)
        # Obtenemos el total de puntos obtenidos por la banca
        puntos_b = self.calcular_puntos(self.mano_banca)

        # Caso 1: La banca supera los 21 puntos (se pasa)
        if puntos_b > 21:
            messagebox.showinfo("¡Ganaste!", "La banca se ha pasado de 21. ¡Tú ganas!")
        # Caso 2: El jugador tiene más puntos que la banca (sin haberse pasado ninguno)
        elif puntos_j > puntos_b:
            messagebox.showinfo("¡Ganaste!", f"¡Has ganado! {puntos_j} puntos frente a {puntos_b} de la banca.")
        # Caso 3: La banca tiene más puntos que el jugador
        elif puntos_b > puntos_j:
            messagebox.showerror("Perdiste", f"La banca gana con {puntos_b} puntos frente a tus {puntos_j} puntos.")
        # Caso 4: Empate técnico de puntos
        else:
            messagebox.showwarning("Empate", f"Empate a {puntos_j} puntos. Se devuelve la apuesta.")

# Comprobamos que el archivo se está ejecutando directamente y no importando como módulo
if __name__ == "__main__":
    # Creamos la ventana principal del sistema operativo mediante Tkinter
    root = tk.Tk()
    # Inicializamos nuestra aplicación pasando la ventana como argumento
    app = BlackjackApp(root)
    # Ejecutamos el bucle principal de eventos para mantener la ventana abierta y escuchando clics
    root.mainloop()