from argparse import ArgumentParser, Namespace
from models import Request

class ContextFactory:
    @staticmethod
    def _parse_args() -> Namespace:
        parser = ArgumentParser(description="UnIT Hackathon")

        parser.add_argument("-m", "--maps", action="store_true", help="Zobrazí mapy NDVI a LST vedle sebe.")
        parser.add_argument("-i", "--hotspots", action="store_true", help="Zobrazí mapu tepelných ostrovů")
        parser.add_argument("-v", '--vegetation', action='store_true', help='Vypíše statistiky ochlazování do konzole')
        parser.add_argument("-c", '--corelation', action='store_true', help='Zobrazí vědecký korelační graf')

        return parser.parse_args()

    @staticmethod
    def get_request():
        args = ContextFactory._parse_args()
        request: Request = Request(**{k: v for k, v in vars(args).items()})
        return request