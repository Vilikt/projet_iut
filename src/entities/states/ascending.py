from src.entities.states import EntityStateName
from src.entities.states.state import EntityState


class EntityStateAscending(EntityState):
    def __init__(self, entity, available_next_states):
        super().__init__(EntityStateName.ASCENDING, entity, available_next_states)
