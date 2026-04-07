from handlers.base_handler import BaseHandler
from models import Request

class HotspotHandler(BaseHandler):
    def _do_logic(self, request: Request) -> bool:
        if request.hotspots:
            print("hotspots")
            return True

        return False
