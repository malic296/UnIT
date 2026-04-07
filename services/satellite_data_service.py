import rasterio
import numpy as np
from scipy.ndimage import zoom
from pathlib import Path
import xarray as xr
from scipy.ndimage import zoom


class SatelliteDataService:
    def __init__(self):
        self.path = Path(__file__).parent.parent / "data"

    def _read_tiff(self, filename):
        with rasterio.open(self.path / filename) as src:
            return src.read(1).astype('float32'), src.shape

    def get_ndvi_matrix(self):
        red, shape = self._read_tiff("B4.tiff")
        nir, _ = self._read_tiff("B8.tiff")

        ndvi = (nir - red) / (nir + red + 1e-10)
        return ndvi, shape

    def get_lst_matrix(self, target_shape):
        lst_raw, current_shape = self._read_tiff("LST.tiff")

        # if np.nanmax(lst_raw) > 200:
        #     lst_raw -= 273.15


        print(f"Teploty načteny. Rozsah: {np.nanmin(lst_raw):.1f}°C až {np.nanmax(lst_raw):.1f}°C")

        zoom_factor = (target_shape[0] / current_shape[0],
                       target_shape[1] / current_shape[1])

        lst_resampled = zoom(lst_raw, zoom_factor, order=1)

        return lst_resampled