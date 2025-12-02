from abc import ABC

from src.entities.states import EntityStateName
from src.mylogging import logger


class EntityState(ABC):
    def __init__(self, name: EntityStateName, entity: "Entity", available_next_states: list[EntityStateName]):
        self.__entity = entity
        self.__name: EntityStateName = name
        self.__available_next_states = available_next_states

    def __repr__(self):
        return self.name

    @property
    def entity(self) -> "Entity":
        return self.__entity

    @property
    def name(self) -> EntityStateName:
        return self.__name

    @property
    def available_next_states(self) -> list[EntityStateName]:
        return self.__available_next_states

    def __is_state_available(self, state_name: EntityStateName) -> bool:
        return state_name in self.__available_next_states

    def get_next_state(self, state_name: EntityStateName) -> EntityStateName:
        if not self.__is_state_available(state_name):
            logger.debug(f"L'état {state_name.name} n'est pas accessible depuis {self.name}, on garde donc l'état courant")
            return self.name

        logger.debug(f"L'état {state_name.name} est accessible depuis {self.name}")
        return state_name
