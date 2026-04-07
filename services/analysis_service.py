import numpy as np


class AnalysisService:
    def __init__(self):
        pass

    def identify_heat_islands(self, lst_matrix, percentile=90):
        clean_data = lst_matrix[~np.isnan(lst_matrix)]
        threshold = np.percentile(clean_data, percentile)

        return lst_matrix > threshold

    def analyze_cooling_effect(self, lst_matrix, vegetation_mask):
        veg_temps = lst_matrix[vegetation_mask]
        urban_temps = lst_matrix[~vegetation_mask]

        avg_veg = np.mean(veg_temps) if veg_temps.size > 0 else 0
        avg_urban = np.mean(urban_temps) if urban_temps.size > 0 else 0

        return {
            "avg_vegetation": avg_veg,
            "avg_urban": avg_urban,
            "difference": avg_urban - avg_veg
        }

    def get_correlation_coefficient(self, ndvi_matrix, lst_matrix):
        ndvi_flat = ndvi_matrix.flatten()
        lst_flat = lst_matrix.flatten()

        mask = ~np.isnan(ndvi_flat) & ~np.isnan(lst_flat)

        correlation_matrix = np.corrcoef(ndvi_flat[mask], lst_flat[mask])
        return correlation_matrix[0, 1]

    def get_land_cover_stats(self, ndvi_matrix, lst_matrix):
        categories = {
            "Water/Other": (ndvi_matrix < 0),
            "Built-up": (ndvi_matrix >= 0) & (ndvi_matrix < 0.2),
            "Sparse Veg": (ndvi_matrix >= 0.2) & (ndvi_matrix < 0.5),
            "Dense Veg": (ndvi_matrix >= 0.5)
        }

        stats = {}
        for name, mask in categories.items():
            temps = lst_matrix[mask]
            stats[name] = np.mean(temps) if temps.size > 0 else 0

        return stats