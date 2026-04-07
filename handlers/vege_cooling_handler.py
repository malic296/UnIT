from handlers.base_handler import BaseHandler
from models import Request

class VegeCoolingHandler(BaseHandler):
    def _do_logic(self, request: Request) -> bool:
        if request.vegetation:
            self._services.analysis.analyze_cooling_effect(self._data.lst, self._data.vegetation_mask)
            return True

        return False
