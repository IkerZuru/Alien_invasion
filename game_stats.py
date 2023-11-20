class GameStats:
    """Sigue las estadisticas del juego"""
    def __init__(self, ai_game):
        """Inicializa las estadisticas"""
        self.settings = ai_game.settings
        self.reset_stats()
        # Inicia AI en estado activo
        self.game_active = False
        # Puntuacion mas alta
        self.high_score = 0

    
    def reset_stats(self):
        """Inicializa las estadisticas que pueden cambiar durante el juego"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 0
        