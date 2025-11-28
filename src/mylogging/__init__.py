import logging

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger("mario_game")

# Vider le fichier au démarrage
with open("mario_game.log", 'w'):
    pass  # Le fichier est maintenant vide

handler = logging.FileHandler("mario_game.log")
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
