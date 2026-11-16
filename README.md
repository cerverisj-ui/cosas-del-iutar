import random
import sys
import pygame

# -----------------------------
# Inicialización
# -----------------------------
pygame.init()

ANCHO = 800
ALTO = 600
FPS = 60

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Carros - Diferentes Pistas")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
AZUL = (0, 100, 255)
AMARILLO = (255, 255, 0)
GRIS = (50, 50, 50)
VERDE = (34, 139, 34)
VERDE_CLARO = (0, 255, 127)

# Fuentes
fuente = pygame.font.SysFont("Arial", 28)
fuente_peq = pygame.font.SysFont("Arial", 20)

# -----------------------------
# Configuración de pistas
# -----------------------------
PISTAS = {
    "1": {
        "nombre": "Asfalto Urbano",
        "color_pista": (60, 60, 60),
        "color_borde": (255, 255, 255),
        "velocidad_max": 8,
        "agarre": 1.0,
    },
    "2": {
        "nombre": "Rally de Tierra",
        "color_pista": (139, 90, 43),
        "color_borde": (210, 180, 140),
        "velocidad_max": 6,
        "agarre": 0.65,
    },
    "3": {
        "nombre": "Pista de Hielo / Nieve",
        "color_pista": (220, 230, 242),
        "color_borde": (100, 149, 237),
        "velocidad_max": 9,
        "agarre": 0.35,
    },
}

# -----------------------------
# Funciones auxiliares
# -----------------------------
def dibujar_texto_central(texto, color, tamaño, y):
    fuente_local = pygame.font.SysFont("Arial", tamaño)
    txt = fuente_local.render(texto, True, color)
    pantalla.blit(txt, (ANCHO // 2 - txt.get_width() // 2, y))


def seleccionar_pista():
    seleccionada = None
    reloj = pygame.time.Clock()

    while seleccionada is None:
        reloj.tick(FPS)
        pantalla.fill(NEGRO)

        titulo = fuente.render("SELECCIONA UNA PISTA", True, AMARILLO)
        pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 100))

        y_pos = 200
        for key, pista in PISTAS.items():
            txt = fuente_peq.render(f"[{key}] {pista['nombre']}", True, BLANCO)
            pantalla.blit(txt, (ANCHO // 2 - 120, y_pos))
            y_pos += 50

        instrucciones = fuente_peq.render(
            "Presiona 1, 2 o 3 para elegir la pista", True, AZUL
        )
        pantalla.blit(
            instrucciones,
            (ANCHO // 2 - instrucciones.get_width() // 2, 450),
        )

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key in (pygame.K_1, pygame.K_KP1):
                    seleccionada = "1"
                elif evento.key in (pygame.K_2, pygame.K_KP2):
                    seleccionada = "2"
                elif evento.key in (pygame.K_3, pygame.K_KP3):
                    seleccionada = "3"

    return PISTAS[seleccionada]


def mostrar_game_over(puntaje):
    pantalla.fill(NEGRO)
    g_text = fuente.render("¡CHOQUE! JUEGO TERMINADO", True, ROJO)
    s_text = fuente_peq.render(f"Puntaje final: {puntaje}", True, BLANCO)
    r_text = fuente_peq.render(
        "Presiona R para jugar otra vez o ESC para salir", True, AMARILLO
    )

    pantalla.blit(
        g_text,
        (ANCHO // 2 - g_text.get_width() // 2, ALTO // 2 - 60)
    )
    pantalla.blit(
        s_text,
        (ANCHO // 2 - s_text.get_width() // 2, ALTO // 2 - 10)
    )
    pantalla.blit(
        r_text,
        (ANCHO // 2 - r_text.get_width() // 2, ALTO // 2 + 40)
    )
    pygame.display.flip()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif evento.key == pygame.K_r:
                    return


# -----------------------------
# Juego principal
# -----------------------------
def juego():
    while True:
        pista_actual = seleccionar_pista()

        # Configuración del carro
        carro_ancho = 40
        carro_alto = 70
        carro_x = float(ANCHO // 2 - carro_ancho // 2)
        carro_y = ALTO - 100
        velocidad_x = 0.0
        velocidad_lateral_max = 6.5

        # Límites de la carretera
        ancho_carretera = 400
        borde_izq = (ANCHO - ancho_carretera) // 2
        borde_der = borde_izq + ancho_carretera

        # Enemigos
        enemigos = []
        puntaje = 0
        ultimo_spawn = pygame.time.get_ticks()
        reloj = pygame.time.Clock()

        corriendo = True

        while corriendo:
            dt = reloj.tick(FPS) / 1000.0

            # Eventos
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Entrada
            teclas = pygame.key.get_pressed()
            agarre = pista_actual["agarre"]
            aceleracion = 0.8 * agarre
            friccion = 1.0 - (0.15 * agarre)

            if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
                velocidad_x -= aceleracion
            elif teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
                velocidad_x += aceleracion
            else:
                velocidad_x *= friccion

            # Limitar velocidad lateral
            velocidad_x = max(-velocidad_lateral_max, min(velocidad_x, velocidad_lateral_max))

            # Mover carro
            carro_x += velocidad_x * 60 * dt
            carro_x = max(borde_izq + 10, min(carro_x, borde_der - carro_ancho - 10))
            velocidad_x *= 0.98 if not (teclas[pygame.K_LEFT] or teclas[pygame.K_a] or teclas[pygame.K_RIGHT] or teclas[pygame.K_d]) else 1.0

            # Spawnear enemigos
            ahora = pygame.time.get_ticks()
            if ahora - ultimo_spawn >= 900:
                ultimo_spawn = ahora
                enem_x = random.randint(borde_izq + 10, borde_der - carro_ancho - 10)
                nuevo_rect = pygame.Rect(enem_x, -100, carro_ancho, carro_alto)

                # Evitar que aparezcan encima de otro enemigo
                if not any(
                    nuevo_rect.colliderect(pygame.Rect(e["x"], e["y"], carro_ancho, carro_alto))
                    for e in enemigos
                ):
                    enemigos.append({
                        "x": enem_x,
                        "y": -100,
                        "color": random.choice([ROJO, AZUL, AMARILLO]),
                    })

            # Mover enemigos
            vel_enemigo = pista_actual["velocidad_max"] * 60 * dt
            for enem in enemigos:
                enem["y"] += vel_enemigo

            # Quitar enemigos fuera de pantalla y sumar puntos
            enemigos = [
                enem for enem in enemigos
                if enem["y"] <= ALTO + 100
            ]

            puntaje += sum(1 for enem in enemigos if enem["y"] > ALTO)
            enemigos = [enem for enem in enemigos if enem["y"] <= ALTO]

            # Rectángulo del jugador
            rect_jugador = pygame.Rect(int(carro_x), carro_y, carro_ancho, carro_alto)

            # Colisiones
            for enem in enemigos:
                rect_enemigo = pygame.Rect(enem["x"], enem["y"], carro_ancho, carro_alto)
                if rect_jugador.colliderect(rect_enemigo):
                    corriendo = False
                    break

            # Render
            pantalla.fill(VERDE)  # pasto

            # Pista
            pygame.draw.rect(pantalla, pista_actual["color_pista"], (borde_izq, 0, ancho_carretera, ALTO))
            pygame.draw.rect(pantalla, pista_actual["color_borde"], (borde_izq - 10, 0, 10, ALTO))
            pygame.draw.rect(pantalla, pista_actual["color_borde"], (borde_der, 0, 10, ALTO))

            # Jugador
            pygame.draw.rect(pantalla, VERDE_CLARO, rect_jugador, border_radius=8)

            # Enemigos
            for enem in enemigos:
                pygame.draw.rect(
                    pantalla,
                    enem["color"],
                    (enem["x"], enem["y"], carro_ancho, carro_alto),
                    border_radius=8
                )

            # HUD
            pygame.draw.rect(pantalla, NEGRO, (10, 10, 420, 40), border_radius=5)
            texto_p = fuente_peq.render(
                f"Puntaje: {puntaje} | Pista: {pista_actual['nombre']}",
                True,
                BLANCO,
            )
            pantalla.blit(texto_p, (20, 18))

            pygame.display.flip()

        mostrar_game_over(puntaje)


if __name__ == "__main__":
    juego()
