# global_vars.py

import threading

VICTORY = "Victory!",
DEFEAT = "Retry?",
RUNNING = ""


class UniqueIdGenerator:
    def __init__(self):
        self._lock = threading.Lock()
        self._counter = 0

    def get_unique_id(self):
        with self._lock:
            self._counter += 1
            return self._counter

class GameState:
    def __init__(self):
        self._lock = threading.Lock()
        self._currentGameState = RUNNING

    @property
    def currentGameState(self):
        return self._currentGameState

    @currentGameState.setter
    def currentGameState(self, value):
        self._currentGameState = value
