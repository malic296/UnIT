from handlers.base_handler import BaseHandler
from models import Request

class VegeCoolingHandler(BaseHandler):
    def _do_logic(self, request: Request) -> bool:
        if request.vegetation:
            print("vege cooling")
            return True

        return False
