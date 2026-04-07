from dataclasses import dataclass
from services import AnalysisService, MaskService, SatelliteDataService, VisualizationService

@dataclass
class ServiceContainer:
    analysis: AnalysisService
    mask: MaskService
    satellite_data: SatelliteDataService
    visualization: VisualizationService