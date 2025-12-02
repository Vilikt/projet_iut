import logging

level = logging.DEBUG

logging.basicConfig(level=level)

logger = logging.getLogger("mario_game")
logger.propagate = False

formatter = logging.Formatter('%(asctime)s - %(name)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s')

file_handler = logging.FileHandler("mario_game.log")
file_handler.setLevel(level)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(level)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
