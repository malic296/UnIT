from handlers.base_handler import BaseHandler
from models import Request

class CorelationHandler(BaseHandler):
    def _do_logic(self, request: Request) -> bool:
        if request.corelation:
            print("corelation")
            return True

        return False
