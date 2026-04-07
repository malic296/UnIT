from handlers.base_handler import BaseHandler
from models import Request

class CorelationHandler(BaseHandler):
    def _do_logic(self, request: Request) -> bool:
        if request.corelation:
            self._services.visualization.plot_correlation_scatter(self._data.ndvi, self._data.lst)
            return True

        return False
