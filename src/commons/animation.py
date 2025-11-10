from copy import deepcopy

import pygame
from pygame import Surface

from src.commons.timer import Timer


class Animation:
    def __init__(self, name: str, images: list[Surface], speed: float, loop: bool = True):
        """Initialise l'animation.

        Args:
            images: Liste des images (Surfaces) de l'animation.
            speed: Temps d'affichage de chaque image (en millisecondes).
            loop: Si True, l'animation boucle indéfiniment.
        """
        if not images:
            raise ValueError("La liste d'images ne peut pas être vide")
        if speed <= 0:
            raise ValueError("La vitesse doit être positive")

        self.__name = name

        self.__images = images
        self.__timer = Timer(speed, loop=loop)  # On passe le paramètre loop au Timer
        self.__image_index = 0
        self.__finished = False
        self.__loop = loop

    def __str__(self):
        return self.__name

    def __repr__(self):
        return f"{self.__name}-{self.__timer.time_to_wait}"

    def __deepcopy__(self, memo: dict[int, object]) -> "Animation":
        # 1. Crée une nouvelle instance de la classe
        copie = self.__class__.__new__(self.__class__)

        # 2. Stocke la copie dans le memo pour éviter les références circulaires
        memo[id(self)] = copie

        # 3. Copie chaque attribut
        copie.__name = self.__name  # str (immutable, pas besoin de deepcopy)
        copie.__images = [img.copy() for img in self.__images]  # Copie chaque Surface
        copie.__timer = deepcopy(self.__timer, memo)  # Le Timer doit implémenter __deepcopy__
        copie.__image_index = self.__image_index  # int (immutable)
        copie.__finished = self.__finished  # bool (immutable)
        copie.__loop = self.__loop  # bool (immutable)

        return copie

    def change_speed(self, speed: float):
        """Change la vitesse de l'animation (en millisecondes par image)."""
        if speed <= 0:
            raise ValueError("La vitesse doit être positive")
        self.__timer.time_to_wait = speed

    def change_name(self, name):
        self.__name = name

    @property
    def finished(self) -> bool:
        """Indique si l'animation a terminé une itération complète."""
        return self.__finished

    @property
    def current_image(self) -> Surface:
        """Retourne l'image actuelle sans modifier l'état."""
        return self.__images[self.__image_index]

    @property
    def speed(self) -> float:
        return self.__timer.time_to_wait

    def change_direction(self):
        """Change le sens de toutes les images de l'animation"""
        self.__images = [pygame.transform.flip(image, True, False) for image in self.__images]

    def restart(self):
        """Réinitialise l'animation à son état initial."""
        self.__image_index = 0
        self.__finished = False
        self.__timer.restart()

    def update(self, delta):
        """Met à jour l'animation.

        Args:
            delta: Temps écoulé depuis le dernier update (en millisecondes).
        """
        # En mode boucle, si l'animation est terminée, on la redémarre
        if self.__finished and self.__loop:
            self.restart()
            return  # On sort après le restart pour éviter le double update

        if not self.__finished:
            self.__timer.update(delta)

            if self.__timer.finished:
                # Mise à jour de l'index de l'image et remise à 0 si on les a toutes faites.
                self.__image_index = (self.__image_index + 1) % len(self.__images)
                self.__finished = not self.__loop
                self.__timer.restart()
