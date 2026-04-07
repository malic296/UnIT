from handlers.base_handler import BaseHandler
from models import Request

class VegeCoolingHandler(BaseHandler):
    def _do_logic(self, request: Request) -> bool:
        if request.vegetation:
            stats = self._services.analysis.analyze_cooling_effect(self._data.lst, self._data.vegetation_mask, self._data.water_mask)
            print(f"Average Urban Temp: {stats['avg_urban']:.2f}°C")
            print(f"Average Veg Temp: {stats['avg_veg']:.2f}°C")
            print(f"Cooling Effect: {stats['cooling_effect']:.2f}°C")
            return True

        return False
