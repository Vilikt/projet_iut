from src.entities.states import EntityStateName
from src.entities.states.state import EntityState


class EntityStateStand(EntityState):
    def __init__(self, entity, available_next_states=()):
        super().__init__(EntityStateName.STAND, entity, available_next_states)
