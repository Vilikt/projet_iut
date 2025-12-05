from src.entities.states import EntityStateName
from src.entities.states.state import EntityState


class EntityStateDescending(EntityState):
    def __init__(self, entity, available_next_states):
        super().__init__(EntityStateName.DESCENDING, entity, available_next_states)

    def is_in_air(self) -> bool:
        return True

    def on_enter(self):
        self.entity.can_jump = False

    def on_quit(self):
        pass
