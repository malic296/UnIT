from handlers.base_handler import BaseHandler
from models import Request

class MapsHandler(BaseHandler):
    def _do_logic(self, request: Request) -> bool:
        if request.maps:
            self._services.visualization.plot_vegetation_vs_heat(self._data.ndvi, self._data.lst)
            return True

        return False
