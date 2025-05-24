import turtle
import random
import time
from abc import ABC, abstractmethod

# --- Interfaz Abstract Factory ---
class FabricaComida(ABC):
    @abstractmethod
    def crear_comida(self):
        pass

# --- Clases concretas de comida ---
class Comida(turtle.Turtle):
    def __init__(self, color):
        super().__init__()
        self.shape("circle")
        self.color(color)
        self.penup()
        self.speed(0)
        self.goto(random.randint(-280, 280), random.randint(-280, 280))

class ComidaVenenosa(Comida):
    def __init__(self):
        super().__init__("purple")

class ComidaFit(Comida):
    def __init__(self):
        super().__init__("green")

class ComidaGrasa(Comida):
    def __init__(self):
        super().__init__("yellow")

class ComidaRey(Comida):
    def __init__(self):
        super().__init__("orange")

# --- Fábricas concretas ---
class FabricaComidaVenenosa(FabricaComida):
    def crear_comida(self):
        return ComidaVenenosa()

class FabricaComidaFit(FabricaComida):
    def crear_comida(self):
        return ComidaFit()

class FabricaComidaGrasa(FabricaComida):
    def crear_comida(self):
        return ComidaGrasa()

class FabricaComidaRey(FabricaComida):
    def crear_comida(self):
        return ComidaRey()

# --- Juego Principal ---
class JuegoSnake:
    def __init__(self):
        self.ventana = turtle.Screen()
        self.ventana.title("Snake con Abstract Factory")
        self.ventana.bgcolor("black")
        self.ventana.setup(width=600, height=600)
        self.ventana.tracer(0)

        self.segmentos = []
        self.crear_serpiente()

        self.direccion = "stop"
        self.puntaje = 0
        self.retraso = 0.1

        self.texto = turtle.Turtle()
        self.texto.hideturtle()
        self.texto.penup()
        self.texto.color("white")
        self.texto.goto(0, 260)
        self.actualizar_puntaje()

        self.ventana.listen()
        self.ventana.onkey(lambda: self.cambiar_direccion("up"), "Up")
        self.ventana.onkey(lambda: self.cambiar_direccion("down"), "Down")
        self.ventana.onkey(lambda: self.cambiar_direccion("left"), "Left")
        self.ventana.onkey(lambda: self.cambiar_direccion("right"), "Right")

        self.factories = [
            FabricaComidaVenenosa(),
            FabricaComidaFit(),
            FabricaComidaGrasa(),
            FabricaComidaRey()
        ]
        self.comida_actual = self.generar_comida()

        self.bucle_juego()

    def crear_serpiente(self):
        for i in range(3):
            segmento = turtle.Turtle("square")
            segmento.color("white")
            segmento.penup()
            segmento.goto(-20 * i, 0)
            self.segmentos.append(segmento)

    def cambiar_direccion(self, nueva_direccion):
        opuestos = {"up": "down", "down": "up", "left": "right", "right": "left"}
        if self.direccion != opuestos.get(nueva_direccion):
            self.direccion = nueva_direccion

    def mover(self):
        for i in range(len(self.segmentos)-1, 0, -1):
            x = self.segmentos[i-1].xcor()
            y = self.segmentos[i-1].ycor()
            self.segmentos[i].goto(x, y)

        cabeza = self.segmentos[0]
        if self.direccion == "up":
            cabeza.sety(cabeza.ycor() + 20)
        elif self.direccion == "down":
            cabeza.sety(cabeza.ycor() - 20)
        elif self.direccion == "left":
            cabeza.setx(cabeza.xcor() - 20)
        elif self.direccion == "right":
            cabeza.setx(cabeza.xcor() + 20)

    def generar_comida(self):
        factory = random.choice(self.factories)
        return factory.crear_comida()

    def verificar_colision_comida(self):
        cabeza = self.segmentos[0]
        if cabeza.distance(self.comida_actual) < 20:
            tipo = type(self.comida_actual)
            self.comida_actual.hideturtle()
            self.comida_actual = self.generar_comida()

            if tipo == ComidaVenenosa:
                if len(self.segmentos) > 3:
                    self.segmentos[-1].hideturtle()
                    self.segmentos.pop()
                self.puntaje = max(0, self.puntaje - 1)
            elif tipo == ComidaFit:
                self.añadir_segmento()
                self.puntaje += 1
            elif tipo == ComidaGrasa:
                self.añadir_segmento()
                self.añadir_segmento()
                self.puntaje += 3
                self.retraso += 0.05
            elif tipo == ComidaRey:
                self.añadir_segmento()
                self.añadir_segmento()
                self.añadir_segmento()
                self.puntaje += 5
                self.retraso = max(0.05, self.retraso - 0.02)

            self.actualizar_puntaje()

    def añadir_segmento(self):
        segmento = turtle.Turtle("square")
        segmento.color("white")
        segmento.penup()
        self.segmentos.append(segmento)

    def actualizar_puntaje(self):
        self.texto.clear()
        self.texto.write(f"Puntaje: {self.puntaje}", align="center", font=("Arial", 16, "normal"))

    def bucle_juego(self):
        while True:
            self.ventana.update()
            self.mover()
            self.verificar_colision_comida()
            time.sleep(self.retraso)

JuegoSnake()
