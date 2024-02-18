import pygame
import sys
from pygame.locals import *

# Definición de colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (6, 0, 191)

# Tamaño de la ventana y tamaño de celda
WINDOW_WIDTH = 440
WINDOW_HEIGHT = 440
CELL_SIZE = 40


# Función para dibujar el mapa y mostrar el mensaje
def draw_map(screen, obstacles, start, end, start_image, font, message):
    screen.fill(WHITE)

    # Dibujar las líneas verticales que separan las celdas
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (x, 0), (x, WINDOW_HEIGHT))

    # Dibujar las líneas horizontales que separan las celdas
    for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (WINDOW_WIDTH, y))

    for obstacle in obstacles:
        pygame.draw.rect(screen, BLACK, pygame.Rect(obstacle[0], obstacle[1], CELL_SIZE, CELL_SIZE))
    screen.blit(start_image, start)
    pygame.draw.rect(screen, GREEN, pygame.Rect(end[0], end[1], CELL_SIZE, CELL_SIZE))

    # Renderizar el mensaje en una superficie
    text_surface = font.render(message, True, BLUE)
    text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    screen.blit(text_surface, text_rect)

    pygame.display.update()


# Función para encontrar la ruta óptima utilizando BFS (Búsqueda por Anchura)
def find_path_bfs(start, end, obstacles):
    visited = set()
    queue = [[start]]
    while queue:
        path = queue.pop(0)
        current = path[-1]
        if current == end:
            return path
        if current not in visited:
            visited.add(current)
            for neighbor in get_neighbors(current, obstacles):
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)


# Función para obtener los vecinos válidos de una celda
def get_neighbors(cell, obstacles):
    neighbors = []
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Movimientos arriba, abajo, izquierda, derecha
    for dx, dy in directions:
        new_cell = (cell[0] + dx * CELL_SIZE, cell[1] + dy * CELL_SIZE)

        # Verificar si el nuevo movimiento está dentro de los límites de la ventana
        if 0 <= new_cell[0] < WINDOW_WIDTH and 0 <= new_cell[1] < WINDOW_HEIGHT:
            if new_cell not in obstacles:
                neighbors.append(new_cell)
        else:
            # Si el nuevo movimiento está fuera de los límites, ajustar a la columna más cercana
            adjusted_cell = (
                min(max(new_cell[0], 0), WINDOW_WIDTH - CELL_SIZE), min(max(new_cell[1], 0), WINDOW_HEIGHT - CELL_SIZE))
            if adjusted_cell not in obstacles:
                neighbors.append(adjusted_cell)
    return neighbors


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Fantasmita App')

    clock = pygame.time.Clock()

    obstacles = set()  # Conjunto de obstáculos

    start_image = pygame.image.load("resources/fantasma.png").convert_alpha()  # Imagen del fantasma
    start_image = pygame.transform.scale(start_image, (CELL_SIZE, CELL_SIZE))

    start = (40, 40)  # Punto A (Inicio)
    end = (360, 360)  # Punto B (Meta)
    path = find_path_bfs(start, end, obstacles)

    # Crear un objeto de fuente
    font = pygame.font.Font(None, 36)

    # Variable para almacenar el mensaje
    message = ""

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN:
                # Obtener las coordenadas del mouse y convertirlas a celdas
                mouse_x, mouse_y = pygame.mouse.get_pos()
                cell_x = (mouse_x // CELL_SIZE) * CELL_SIZE
                cell_y = (mouse_y // CELL_SIZE) * CELL_SIZE

                # Verificar si la posición del obstáculo bloquea todas las rutas válidas para el fantasma
                new_obstacles = obstacles.copy()
                new_obstacles.add((cell_x, cell_y))
                new_path = find_path_bfs(start, end, new_obstacles)
                if new_path:
                    obstacles.add((cell_x, cell_y))
                    path = new_path

        if path:
            next_cell = path.pop(0)
            start = next_cell
        else:
            # Mostrar el mensaje solo cuando el fantasma llega a la meta
            message = "El fantasma ha llegado a la meta"

        # Actualizar el mensaje y dibujar el mapa en cada iteración del bucle principal
        draw_map(screen, obstacles, start, end, start_image, font, message)

        # Salir del bucle si el fantasma ha llegado a la meta y se muestra el mensaje
        if message:
            pygame.time.delay(3000)  # Esperar 3 segundos antes de salir
            pygame.quit()
            sys.exit()

        clock.tick(3)


if __name__ == '__main__':
    main()
