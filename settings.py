class Settings:
    """Una clase para guardar toda la configuracion del juego"""

    def __init__(self):
        """Inicializa la configuracion del juego"""
        # Configuración de la pantalla
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (255, 255, 255)

        #Configuración de la nave:

        self.ship_limit = 3

        # Configuración de las balas
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        #Configuraciones del alien
        self.fleet_drop_speed = 10

        # Rapidez con la que se acelera el juego
        self.speedup_scale = 1.1

        # Lo rapido que aumenta el valor de los puntos de los aliens
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
            """Inicializa las configuraciones que cambian durante el juego"""
            self.ship_speed = 1.5
            self.bullet_speed = 1.0
            self.alien_speed = 0.5
            # fleet_direction de 1 representa derecha, -1 izquierda
            self.fleet_direction = 1
            # Puntuacion por matar aliens
            self.alien_points = 50
        
    def increase_speed(self):
        """Incrementa las configuraciones de velocidad y los valores de los puntos"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
