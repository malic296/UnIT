import rasterio
import numpy as np
from scipy.ndimage import zoom
from pathlib import Path

class SatelliteDataService:
    def __init__(self):
        self.path = Path(__file__).parent.parent / "data"

    def _read_tiff(self, filename):
        with rasterio.open(self.path / filename) as src:
            data = src.read(1).astype('float32')
            data[data == 0] = np.nan
            return data, src.shape

    def get_ndvi_matrix(self):
        red, shape = self._read_tiff("B4.tiff")
        nir, _ = self._read_tiff("B8.tiff")

        ndvi = (nir - red) / (nir + red + 1e-10)

        ndvi = np.clip(ndvi, -1, 1)
        return ndvi, shape

    def get_lst_matrix(self, target_shape):
        lst_raw, current_shape = self._read_tiff("LST.tiff")
        lst_k = lst_raw / 200.0
        lst_c = lst_k - 273.15
        lst_c = np.clip(lst_c, -10, 60)

        zoom_factor = (target_shape[0] / current_shape[0],
                       target_shape[1] / current_shape[1])

        lst_resampled = zoom(lst_c, zoom_factor, order=1)

        return lst_resampled