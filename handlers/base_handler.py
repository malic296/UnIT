from __future__ import annotations
from abc import ABC, abstractmethod
from models import SatelliteData, Request
from models.service_container import ServiceContainer

class BaseHandler(ABC):
    @abstractmethod
    def _do_logic(self, request) -> bool:
        pass

    def __init__(self, services: ServiceContainer, data: SatelliteData):
        self._services = services
        self._data = data
        self._next_handler = None

    def set_next(self, handler: BaseHandler):
        self._next_handler = handler
        return handler

    def handle(self, request: Request):
        try:
            handled = self._do_logic(request)
            if handled:
                return
        except Exception as e:
            raise Exception(f"{self.__class__.__name__} handler failed because: {e}")

        if self._next_handler:
            self._next_handler.handle(request)

        else:
            raise Exception(f"Request was not handled.")

