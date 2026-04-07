import numpy as np

class AnalysisService:
    def identify_heat_islands(self, lst, percentile=95):
        valid = lst[~np.isnan(lst)]
        if valid.size == 0: return np.zeros_like(lst, dtype=bool)
        return lst > np.percentile(valid, percentile)

    def analyze_cooling_effect(self, lst, veg_mask, water_mask):
        valid_data = ~np.isnan(lst)

        urban_mask = valid_data & ~veg_mask & ~water_mask

        v_temps = lst[veg_mask & valid_data]
        u_temps = lst[urban_mask]

        avg_v = np.mean(v_temps) if v_temps.size > 0 else 0
        avg_u = np.mean(u_temps) if u_temps.size > 0 else 0

        return {
            "avg_veg": round(float(avg_v), 2),
            "avg_urban": round(float(avg_u), 2),
            "cooling_effect": round(float(avg_u - avg_v), 2)
        }

    def get_correlation_coefficient(self, ndvi, lst):
        n_flat, l_flat = ndvi.flatten(), lst.flatten()
        mask = ~np.isnan(n_flat) & ~np.isnan(l_flat)
        if not np.any(mask): return 0
        return np.corrcoef(n_flat[mask], l_flat[mask])[0, 1]

    def get_land_cover_stats(self, ndvi, lst):
        cats = {
            "Voda": ndvi < -0.1,
            "Beton/Zástavba": (ndvi >= -0.1) & (ndvi < 0.2),
            "Nízká zeleň": (ndvi >= 0.2) & (ndvi < 0.5),
            "Hustá vegetace": ndvi >= 0.5
        }

        stats = {}
        for name, mask in cats.items():
            valid_mask = mask & ~np.isnan(lst)
            temps = lst[valid_mask]
            stats[name] = round(float(np.mean(temps)), 2) if temps.size > 0 else 0

        return stats