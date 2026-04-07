from dataclasses import dataclass
import numpy as np

@dataclass
class SatelliteData:
    ndvi: np.ndarray
    lst: np.ndarray

    vegetation_mask: np.ndarray
    concrete_mask: np.ndarray
    water_mask: np.ndarray
    heat_islands_mask: np.ndarray

    shape: tuple