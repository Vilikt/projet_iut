from copy import deepcopy
from pathlib import Path

import pytmx
from pygame import Surface, Rect
from pygame._sprite import Group
from pygame.event import Event
from pytmx import load_pygame

from src.commons import SCREEN_WIDTH, COLOR_BLACK, SCREEN_HEIGHT
from src.commons.animation import Animation
from src.commons.my_events import QUESTION_BLOCK_HIT
from src.entities.tiles.brick_block_sprite import BrickBlockSprite
from src.entities.tiles.question_block_sprite import QuestionBlockSprite
from src.entities.tiles.solid_sprite import SolidSprite
from src.entities.tiles.tile_sprite import TileSprite
from src.game.gameloop_interface import GameLoopInterface


class Level(GameLoopInterface):
    def __init__(self, map_path: Path):
        self.__tmx_data = load_pygame(map_path)
        self.__tile_width =  self.__tmx_data.tilewidth
        self.__tile_height =  self.__tmx_data.tileheight
        self.__width = self.__tmx_data.width * self.__tile_width
        self.__height = self.__tmx_data.height * self.__tile_height
        self.__surface = Surface((self.__width, self.__height))

        # 1. Groupes Pygame classiques pour la logique (collisions, mises à jour)
        self.all_sprites = Group()  # Tous les sprites
        self.collidable_sprites = Group()  # Sprites solides (blocs, sol)
        self.question_block_sprites = Group()  # Blocs "?"
        self.brick_block_sprites = Group()  # Blocs de briques cassable
        self.enemy_sprites = Group()  # Ennemis (Goombas, Koopas)
        self.block_sprites = Group()  # briques
        self.player_sprite = Group()

        self.__animations: dict[int, Animation] = {}

        self.__start_point = None

        # Charge les couches
        self.__load_layers()

        self.__shift = 0
        self.center_at = None

    @property
    def name(self) -> str:
        return self.__tmx_data.properties["name"]

    @property
    def time(self) -> str:
        return self.__tmx_data.properties["time"]

    @property
    def type(self) -> str:
        return self.__tmx_data.properties["type"]

    @property
    def player_start_point(self) -> tuple[int, int]:
        if self.__start_point is None:
            raise ValueError("Le point de départ du joueur n'est pas défini dans la map")

        return self.__start_point

    def __load_layers(self):
        """Charge les couches du niveau et crée les sprites."""
        for layer in self.__tmx_data.layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                self.__load_tile_layer(layer)

        for layer in self.__tmx_data.layers:
            if isinstance(layer, pytmx.TiledObjectGroup):
                self.__load_object_layer(layer)

    def __load_object_layer(self, layer: pytmx.TiledObjectGroup):
        """Charge une couche d'objets (pièces, ennemis, etc.)."""
        for obj in layer:
            if obj.type == "SpawnPoint":
                if obj.name == "PlayerStart":
                    self.__start_point = (obj.x, obj.y)
            elif obj.type == "QuestionBlock":
                # On cherche le Sprite se trouvant au même endroit que l'objet pour y ajouter les propriétés.
                for question_block_sprite in self.question_block_sprites:
                    if question_block_sprite.x == obj.x and question_block_sprite.y == obj.y:
                        question_block_sprite.properties |= obj.properties

    def __load_tile_layer(self, layer: pytmx.TiledTileLayer):
        """Charge une couche de tuiles (Terrain, Décors, etc.)."""
        for x, y, gid in layer:
            x *= self.__tile_width
            y *= self.__tile_height

            if gid != 0:
                properties = self.__tmx_data.get_tile_properties_by_gid(gid)
                image = self.__tmx_data.get_tile_image_by_gid(gid)

                if layer.name == "QuestionBlocks":
                    animation = self.__get_animation(x, y, gid, properties)
                    sprite = QuestionBlockSprite(x, y, animation, properties)
                    self.question_block_sprites.add(sprite)
                    self.collidable_sprites.add(sprite)
                elif layer.name == "BrickBlocks":
                    sprite = BrickBlockSprite(x, y, image, properties)
                    self.brick_block_sprites.add(sprite)
                    self.collidable_sprites.add(sprite)
                elif properties["solid"]:
                    sprite = SolidSprite(x, y, image, properties)
                    self.collidable_sprites.add(sprite)
                else:
                    sprite = TileSprite(x, y, image, properties)

                self.all_sprites.add(sprite)

    def __get_animation(self, x, y, gid, props) -> Animation | None:
        """Crée et retourne une Animation à partir des frames d'un tile"""

        # Si l'Animation a déjà été créée, on renvoie une copie.
        if gid in self.__animations.keys():
            return deepcopy(self.__animations[gid])

        # Si pas de frames, on supprime la clé inutile et on renvoie None
        if not props["frames"]:
            del props["frames"]
            return None

        frame_duration = props["frames"][0].duration
        images = [self.__tmx_data.get_tile_image_by_gid(frame.gid) for frame in props["frames"]]
        del props["frames"]  # On supprime la List devenue inutile.

        animation = Animation(str(f"{gid}-({x}, {y})"), images, frame_duration, True)
        self.__animations[gid] = animation

        return animation

    def handle_events(self, event: Event):
        if event.type not in [QUESTION_BLOCK_HIT]:
            return

        for sprite in self.collidable_sprites:
            sprite.handle_events(event)

    def update_dt(self, delta):
        self.all_sprites.update(delta)
        self.player_sprite.update(delta)

        if self.center_at is not None:
            self.__shift = self.center_at.x - SCREEN_WIDTH / 2
            if self.__shift < 0:
                self.__shift = 0
            if self.__shift > self.__width - SCREEN_WIDTH:
                self.__shift = self.__width - SCREEN_WIDTH

    def render(self):
        """Affiche le niveau sur une surface."""
        self.__surface.fill(COLOR_BLACK)

        # Dessine l'ensemble des tuiles du niveau
        self.all_sprites.draw(self.__surface)
        self.player_sprite.draw(self.__surface)

    def get_surface(self) -> Surface:
        """Renvoie une Surface de la taille de l'écran en fonction du décallage du scrolling"""
        rect = Rect(self.__shift, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        surface = self.__surface.subsurface(rect)

        return surface
