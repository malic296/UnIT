from handlers.base_handler import BaseHandler
from models import Request

class VegeCoolingHandler(BaseHandler):
    def _do_logic(self, request: Request) -> bool:
        if request.vegetation:
            stats = self._services.analysis.analyze_cooling_effect(self._data.lst, self._data.vegetation_mask)
            print(f"Average Urban Temp: {stats['avg_urban']:.2f}°C")
            print(f"Average Veg Temp: {stats['avg_vegetation']:.2f}°C")
            print(f"Cooling Effect: {stats['difference']:.2f}°C")
            return True

        return False
