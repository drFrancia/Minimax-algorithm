
class Tablero:
    def __init__(self, filas, columnas, posicion_raton, posicion_gato):
        self.filas = filas  # Número de filas del tablero
        self.columnas = columnas  # Número de columnas del tablero
        self.posicion_raton = posicion_raton  # Posición actual del ratón (fila, columna)
        self.posicion_gato = posicion_gato  # Posición actual del gato (fila, columna)

    def print_tablero(self):
        # Método para imprimir el tablero
        for i in range(self.filas):
            for j in range(self.columnas):
                if (i, j) == self.posicion_raton:
                    print("M", end=" ")  # Imprimir "M" en la posición del ratón
                elif (i, j) == self.posicion_gato:
                    print("C", end=" ")  # Imprimir "C" en la posición del gato
                else:
                    print(".", end=" ")  # Imprimir "." para las celdas vacías
            print()

    def movimiento_raton(self, direccion):
        # Método para mover el ratón en una dirección dada
        if direccion == "arriba" and self.posicion_raton[0] > 0:
            self.posicion_raton = (self.posicion_raton[0] - 1, self.posicion_raton[1])
        elif direccion == "abajo" and self.posicion_raton[0] < self.filas - 1:
            self.posicion_raton = (self.posicion_raton[0] + 1, self.posicion_raton[1])
        elif direccion == "izquierda" and self.posicion_raton[1] > 0:
            self.posicion_raton = (self.posicion_raton[0], self.posicion_raton[1] - 1)
        elif direccion == "derecha" and self.posicion_raton[1] < self.columnas - 1:
            self.posicion_raton = (self.posicion_raton[0], self.posicion_raton[1] + 1)

    def movimiento_gato(self, direccion):
        # Método para mover el gato en una dirección dada
        if direccion == "arriba" and self.posicion_gato[0] > 0:
            self.posicion_gato = (self.posicion_gato[0] - 1, self.posicion_gato[1])
        elif direccion == "abajo" and self.posicion_gato[0] < self.filas - 1:
            self.posicion_gato = (self.posicion_gato[0] + 1, self.posicion_gato[1])
        elif direccion == "izquierda" and self.posicion_gato[1] > 0:
            self.posicion_gato = (self.posicion_gato[0], self.posicion_gato[1] - 1)
        elif direccion == "derecha" and self.posicion_gato[1] < self.columnas - 1:
            self.posicion_gato = (self.posicion_gato[0], self.posicion_gato[1] + 1)


class Minimax:
    def __init__(self, profundidad):
        self.profundidad = profundidad  # Profundidad máxima para la búsqueda de Minimax

    def minimax(self, tablero, maximizing_player, profundidad): # Investigar diferencia entre una profundidad mayor o menor.
        # Algoritmo Minimax
        if profundidad == 0 or tablero.posicion_raton == tablero.posicion_gato:
            return self.evaluate(tablero)  # Evaluar la posición actual del tablero

        if maximizing_player:
            max_eval = float('-inf')#  Investigar que significa -inf
            for direccion in ["arriba", "abajo", "izquierda", "derecha"]:
                new_tablero = self.get_new_tablero(tablero, direccion, "mouse")
                eval = self.minimax(new_tablero, False, profundidad - 1)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for direccion in ["arriba", "abajo", "izquierda", "derecha"]:
                new_tablero = self.get_new_tablero(tablero, direccion, "cat")
                eval = self.minimax(new_tablero, True, profundidad - 1)
                min_eval = min(min_eval, eval)
            return min_eval

    def get_new_tablero(self, tablero, direccion, player):
        # Obtener un nuevo tablero después de realizar un movimiento
        new_tablero = Tablero(tablero.filas, tablero.columnas, tablero.posicion_raton, tablero.posicion_gato)
        if player == "mouse":
            new_tablero.movimiento_raton(direccion)
        else:
            new_tablero.movimiento_gato(direccion)
        return new_tablero

    def evaluate(self, tablero):
        # Función de evaluación heurística para la posición del tablero
        # Devuelve la distancia Manhattan entre el ratón y el gato
        return abs(tablero.posicion_raton[0] - tablero.posicion_gato[0]) + abs(tablero.posicion_raton[1] - tablero.posicion_gato[1])


class Game:
    def __init__(self, filas, columnas, posicion_raton, posicion_gato, profundidad):
        # Inicialización del juego con el tablero, Minimax y posiciones iniciales del ratón y el gato
        self.filas = filas
        self.columnas = columnas
        self.posicion_inicial_raton = posicion_raton
        self.posicion_inicial_gato = posicion_gato
        self.profundidad = profundidad
        self.reset_game()

    def reset_game(self):
        # Método para reiniciar el juego a las posiciones iniciales
        self.tablero = Tablero(self.filas, self.columnas, self.posicion_inicial_raton, self.posicion_inicial_gato)
        self.minimax = Minimax(self.profundidad)

    def play(self):
        # Método para jugar el juego
        while True:
            print("Turno del ratón:")
            self.tablero.print_tablero()  # Imprimir el tablero actual
            self.get_user_move()  # Obtener el movimiento del usuario (ratón)

            if self.check_winner("mouse"):
                print("¡El ratón escapó! ¡Victoria del ratón!")
                break

            print("Turno del gato:")
            self.tablero.print_tablero()
            best_movimiento_gato = self.get_best_move("cat")  # Obtener el mejor movimiento para el gato
            self.tablero.movimiento_gato(best_movimiento_gato)  # Mover al gato automáticamente

            if self.check_winner("cat"):
                print("¡El gato atrapó al ratón! ¡Victoria del gato!")
                break

        self.ask_reset()  # Preguntar si se quiere reiniciar el juego

    def get_user_move(self):
        # Método para obtener el movimiento del usuario (ratón)
        while True:
            move = input("Ingresa tu movimiento (arriba, abajo, izquierda, derecha): ").lower()
            if move in ["arriba", "abajo", "izquierda", "derecha"]:
                self.tablero.movimiento_raton(move)  # Mover el ratón según el input del usuario
                break
            else:
                print("Movimiento inválido. Intenta de nuevo.")

    def get_best_move(self, player):
        # Método para obtener el mejor movimiento para el gato (controlado por Minimax)
        best_move = None
        best_eval = float('-inf') if player == "mouse" else float('inf')
        direcciones = ["arriba", "abajo", "izquierda", "derecha"]
        for direccion in direcciones:
            new_tablero = self.get_new_tablero(player, direccion)  # Obtener un nuevo tablero después de mover el gato
            eval = self.minimax.minimax(new_tablero, player == "mouse", self.minimax.profundidad)  # Ejecutar Minimax
            if (player == "mouse" and eval > best_eval) or (player == "cat" and eval < best_eval):
                best_eval = eval
                best_move = direccion
        return best_move

    def get_new_tablero(self, player, direccion):
        # Obtener un nuevo tablero después de mover el gato
        new_tablero = Tablero(self.tablero.filas, self.tablero.columnas, self.tablero.posicion_raton, self.tablero.posicion_gato)
        if player == "mouse":
            new_tablero.movimiento_raton(direccion)
        else:
            new_tablero.movimiento_gato(direccion)
        return new_tablero

    def check_winner(self, player):
        # Verificar si hay un ganador
        if player == "mouse":
            return self.tablero.posicion_raton == (self.tablero.filas - 1, self.tablero.columnas - 1)
        else:
            return self.tablero.posicion_raton == self.tablero.posicion_gato

    def ask_reset(self):
        # Método para preguntar si se quiere reiniciar el juego
        while True:
            reset = input("¿Quieres reiniciar el juego? (s/n): ").lower()
            if reset == "s":
                self.reset_game()
                self.play()
                break
            elif reset == "n":
                print("Fin del juego.")
                break
            else:
                print("Entrada inválida. Intenta de nuevo.")

# Crear un juego 5x5 con el ratón en (0, 0) y el gato en (4, 4) y profundidad 3
game = Game(5, 5, (0, 0), (4, 4), 3)
game.play()
