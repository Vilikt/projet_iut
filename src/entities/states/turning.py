from src.entities.states import EntityStateName
from src.entities.states.state import EntityState


class EntityStateTurning(EntityState):
    def __init__(self, entity, available_next_states):
        super().__init__(EntityStateName.TURNING, entity, available_next_states)

    def is_in_air(self) -> bool:
        return False

    def on_enter(self):
        self.entity.can_jump = True

    def on_quit(self):
        pass
