class Settings:
    """Una clase para guardar toda la configuracion del juego"""

    def __init__(self):
        """Inicializa la configuracion del juego"""
        # Configuración de la pantalla
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (255, 255, 255)

        #Configuración de la nave:
        self.ship_speed = 1.5

        # Configuración de las balas
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)