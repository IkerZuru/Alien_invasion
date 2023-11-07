import sys
import pygame
from settings import Settings
from Ship import Ship
from bullet import Bullet

class AlienInvasion:
    """Clase general para gestionar los recursos y el comportamiento del juego"""

    def __init__(self):
        """Inicializa el juego y crea recursos"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

    def run_game(self):
        """Inicia el bucle principal para el juego"""
        while True:
            self._check_events()
            self.ship.update()
            self.bullets.update()

            # Se deshace de las balas que han desaparecido
            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0 :
                    self.bullets.remove(bullet)

            self._update_screen()


    def _check_events(self):
        """Responde a pulsaciones de teclas y eventos de ratón"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)


    def _check_keydown_events(self, event):
        """Responde a pulsaciones de teclas"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()


    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Crea una bala nueva y la añade al grupo de balas"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
        
                   

    def _update_screen(self):
        """Actualiza las imagenes en la pantalla y cambia a la pantalla nueva"""
         # Redibuja la pantalla en cada paso por el bucle
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # Hace visible la última pantalla dibujada
        pygame.display.flip()
        

if __name__ == "__main__":
    # Hace una instancia del juego y lo ejecuta
    ai = AlienInvasion()
    ai.run_game()

