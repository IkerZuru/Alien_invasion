import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from Ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """Clase general para gestionar los recursos y el comportamiento del juego"""

    def __init__(self):
        """Inicializa el juego y crea recursos"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        # Crea un marcador y una instancia para guardar estadisticas del juego
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Hace el boton play
        self.play_button = Button(self, "Play")


    def run_game(self):
        """Inicia el bucle principal para el juego"""
        while True:
            self._check_events()
            if  self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
        
    def _check_play_button(self, mouse_pos):
        """Inicia un juego nuevo cuando el jugador pulsa play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Restablece las estadisticas del juego
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            # Se deshace de los aliens y las balas
            self.aliens.empty()
            self.bullets.empty()

            #Crea una nueva flota y centra la nave
            self._create_fleet
            self.ship.center_ship
            #Oculta el raton
            pygame.mouse.set_visible(False)


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


    
    def _update_bullets(self):
        """Actualiza la posición de las balas y se deshace de las viejas"""
        # Actualiza las posiciones de las balas.
        self.bullets.update()

        # Se deshace de las balas que han desaparecido
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0 :
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        
        # Busca balas que hayan dado a aliens, si lo hay, se deshace de la bala y del alien
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points *len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            #Destruye las balas existentes y crea una nueva flota
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Aumenta el nivel
            self.stats.level += 1
            self.sb.prep_level()


    def _check_fleet_edges(self):
        """Responde si algun alien ha llegado a un borde"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Baja toda la flota y cambia su direccion"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    
    def _update_aliens(self):
        """Comprueba si la flota esta en un borde, despues actualiza las posiciones de los aliens"""
        self._check_fleet_edges()
        self.aliens.update()
        #Busca colisiones entre aliens y nave
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        # Si algun alien ha llegado al fondo de la pantalla
        self._check_aliens_bottom()

        
    def _create_fleet(self):
        """Crea la flota de aliens"""
        # Crea un alien y halla el numero de aliens en una fila
        # El espacio entre aliens es igual a la anchura de un alien
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        aviable_space_x = self.settings.screen_width - (2 * alien_width)
        numbre_aliens_x = aviable_space_x // (2 * alien_width)

        # Determina el numero de filas de aliens que caben  en la pantalla
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height - ship_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Crea la flota completa de aliens
        for row_number in range(number_rows):
            for alien_number in range(numbre_aliens_x):
                self._create_alien(alien_number, row_number)
 

    def _create_alien(self, alien_number, row_number):
        #Crea un alien y lo coloca en la fila
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien) 

    def _ship_hit(self):
        """Responde al impacto de un alien en la nave  y actualiza el marcador"""
        if self.stats.ships_left > 0:
            #Disminuye las naves que quedan
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            #Se deshace de los aliens y balas restantes
            self.aliens.empty()
            self.bullets.empty()

            # Crea una nueva flota y centra la nave
            self._create_fleet()
            self.ship.center_ship()

            #Pausa
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
    
    def _check_aliens_bottom(self):
        """Comprueba si algun alien ha llegado al fondo de la pantalla"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Hacer como si hubiese colisionado con la nave
                self._ship_hit()
                break
                    

    def _update_screen(self):
        """Actualiza las imagenes en la pantalla y cambia a la pantalla nueva"""
         # Redibuja la pantalla en cada paso por el bucle
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        
        self.aliens.draw(self.screen)

        # Dibuja la informacion de la puntuacion
        self.sb.show_score()

        # Dibuja el boton de play si esta inactivo
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Hace visible la última pantalla dibujada
        pygame.display.flip()
        

if __name__ == "__main__":
    # Hace una instancia del juego y lo ejecuta
    ai = AlienInvasion()
    ai.run_game()

