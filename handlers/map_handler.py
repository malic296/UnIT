from handlers.base_handler import BaseHandler
from models import Request

class MapsHandler(BaseHandler):
    def _do_logic(self, request: Request) -> bool:
        if request.maps:
            print("maps")
            return True

        return False
