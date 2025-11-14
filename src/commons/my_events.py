import pygame

MARIO_DEATH = pygame.USEREVENT + 1
SCORE_CHANGED = pygame.USEREVENT + 2
COINS_CHANGED = pygame.USEREVENT + 3
QUESTION_BLOCK_HIT = pygame.USEREVENT + 4


def post_event(event_name: int, datas: dict = None, delay: int = None):
    if datas is not None:
        my_event = pygame.event.Event(event_name, datas)
    else:
        my_event = pygame.event.Event(event_name)

    for event in pygame.event.get(event_name):
        return

    if delay is not None:
        pygame.time.set_timer(my_event, delay, False)
    else:
        pygame.event.post(my_event)
