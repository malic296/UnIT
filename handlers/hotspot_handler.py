from handlers.base_handler import BaseHandler
from models import Request

class HotspotHandler(BaseHandler):
    def _do_logic(self, request: Request) -> bool:
        if request.hotspots:
            self._services.visualization.plot_heat_islands_on_map(self._data.lst, self._data.heat_islands_mask)
            return True

        return False
