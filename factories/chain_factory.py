from handlers.base_handler import BaseHandler
from models import SatelliteData
from models.service_container import ServiceContainer
from services import AnalysisService, SatelliteDataService, MaskService, VisualizationService
from handlers import CorelationHandler, VegeCoolingHandler, HotspotHandler, MapsHandler

class ChainFactory:
    @staticmethod
    def _get_services_container() -> ServiceContainer:
        return ServiceContainer(
            analysis=AnalysisService(),
            satellite_data=SatelliteDataService(),
            mask=MaskService(),
            visualization=VisualizationService()
        )

    @staticmethod
    def _get_data(services: ServiceContainer) -> SatelliteData:
        ndvi, shape = services.satellite_data.get_ndvi_matrix()
        lst = services.satellite_data.get_lst_matrix(target_shape=shape)

        vege_mask= services.mask.get_vegetation_mask(ndvi)
        concrete_mask = services.mask.get_concrete_mask(ndvi)
        water_mask = services.mask.get_water_mask(ndvi)
        heat_islands_mask = services.analysis.identify_heat_islands(lst, percentile=90)

        return SatelliteData(
            ndvi=ndvi,
            lst=lst,
            vegetation_mask=vege_mask,
            concrete_mask=concrete_mask,
            water_mask=water_mask,
            heat_islands_mask=heat_islands_mask,
            shape=shape

        )

    @staticmethod
    def get_chained_handler() -> BaseHandler:
        services: ServiceContainer = ChainFactory._get_services_container()
        data = ChainFactory._get_data(services)

        maps = MapsHandler(services=services, data=data)
        corelation = CorelationHandler(services=services, data=data)
        vege_cooling = VegeCoolingHandler(services=services, data=data)
        hotspots = HotspotHandler(services=services, data=data)

        maps.set_next(corelation).set_next(vege_cooling).set_next(hotspots)
        return maps


