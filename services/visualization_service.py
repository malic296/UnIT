import matplotlib.pyplot as plt
import numpy as np


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

    def plot_vegetation_vs_heat(self, ndvi_matrix, lst_matrix, mask_service=None):
        # fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        #
        # im1 = ax1.imshow(ndvi_matrix, cmap='RdYlGn')
        # ax1.set_title("Mapa vegetace (NDVI)")
        # fig.colorbar(im1, ax=ax1, label="Index zeleně")
        #
        # im2 = ax2.imshow(lst_matrix, cmap='coolwarm')
        # ax2.set_title("Teplotní mapa (LST)")
        # fig.colorbar(im2, ax=ax2, label="Teplota [°C]")
        #
        # plt.tight_layout()
        # plt.show()

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

        im1 = ax1.imshow(ndvi_matrix, cmap='RdYlGn')
        ax1.set_title("Mapa vegetace (NDVI)")
        fig.colorbar(im1, ax=ax1, label="Index zeleně")

        if mask_service is not None:
            water_mask = mask_service.get_water_mask(ndvi_matrix)
            ax1.imshow(water_mask, cmap='Blues', alpha=0.5)

        im2 = ax2.imshow(lst_matrix, cmap='coolwarm')
        ax2.set_title("Teplotní mapa (LST)")
        fig.colorbar(im2, ax=ax2, label="Teplota [°C]")

        if mask_service is not None:
            water_mask = mask_service.get_water_mask(ndvi_matrix)
            ax2.imshow(water_mask, cmap='Blues', alpha=0.5)

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