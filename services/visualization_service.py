import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')

class VisualizationService:
    def __init__(self):
        plt.style.use('ggplot')

    def plot_heat_islands_on_map(self, lst_matrix, heat_island_mask):
        plt.figure(figsize=(12, 8))

        plt.imshow(lst_matrix, cmap='inferno', alpha=0.8)
        plt.colorbar(label='Teplota povrchu [°C]')

        islands_display = np.where(heat_island_mask, 1.0, np.nan)

        plt.imshow(islands_display, cmap='Reds', vmin=0, vmax=1)

        plt.title("Detekce městských tepelných ostrovů (Hotspots)")
        plt.show()

    def plot_vegetation_vs_heat(self, ndvi_matrix, lst_matrix):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

        h, w = ndvi_matrix.shape
        rgb_map = np.zeros((h, w, 3))

        water_mask = ndvi_matrix < 0
        land_mask = (ndvi_matrix >= 0) & (ndvi_matrix < 0.2)
        veg_mask = ndvi_matrix >= 0.2

        rgb_map[water_mask] = [0, 0.3, 0.8]
        rgb_map[land_mask] = [0.9, 0.8, 0.4]
        rgb_map[veg_mask] = [0.1, 0.6, 0.1]

        ax1.imshow(rgb_map)
        ax1.set_title("Klasifikace povrchu (NDVI)")

        legend_elements = [
            Line2D([0], [0], color=[0, 0.3, 0.8], lw=4, label='Voda'),
            Line2D([0], [0], color=[0.9, 0.8, 0.4], lw=4, label='Země/Beton'),
            Line2D([0], [0], color=[0.1, 0.6, 0.1], lw=4, label='Vegetace')
        ]
        ax1.legend(handles=legend_elements, loc='upper right')

        im2 = ax2.imshow(lst_matrix, cmap='magma')
        ax2.set_title("Teplotní mapa (LST)")
        fig.colorbar(im2, ax=ax2, label="Teplota [°C]")

        water_overlay = np.where(water_mask, 1.0, np.nan)
        ax2.imshow(water_overlay, cmap='Blues_r', alpha=0.5)

        plt.tight_layout()
        plt.show()



    def plot_correlation_scatter(self, ndvi_matrix, lst_matrix):
        x = ndvi_matrix.flatten()[::50]
        y = lst_matrix.flatten()[::50]

        mask = ~np.isnan(x) & ~np.isnan(y)
        x, y = x[mask], y[mask]

        plt.figure(figsize=(10, 6))
        plt.scatter(x, y, alpha=0.3, s=10, c=y, cmap='coolwarm')

        m, b = np.polyfit(x, y, 1)
        plt.plot(x, m * x + b, color='black', label=f'Trend (ochlazování)')

        plt.xlabel("NDVI (Míra zeleně)")
        plt.ylabel("LST (Teplota povrchu [°C])")
        plt.title("Důkaz: Jak zeleň snižuje teplotu ve městě")
        plt.legend()
        plt.show()