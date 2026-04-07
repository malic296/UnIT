import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import matplotlib
import matplotlib.image as mpimg
from pathlib import Path

matplotlib.use('Qt5Agg')


class VisualizationService:
    def __init__(self):
        plt.style.use('ggplot')
        # Cesta k podkladovému screenshotu z Copernicus Browseru [cite: 22]
        self.picture_path = Path(__file__).parent.parent / "data" / "prague.png"
        self._bg_image = None

        if self.picture_path.exists():
            self._bg_image = mpimg.imread(str(self.picture_path))

    def _get_extent(self, matrix):
        """Vytvoří souřadný systém pro zarovnání vrstev (pixel-to-pixel)."""
        h, w = matrix.shape[:2]
        return [0, w, h, 0]

    def plot_heat_islands_on_map(self, lst_matrix, heat_island_mask):
        fig, ax = plt.subplots(figsize=(12, 8))
        extent = self._get_extent(lst_matrix)

        # 1. Vrstva: Pozadí (vždy vespod)
        if self._bg_image is not None:
            ax.imshow(self._bg_image, extent=extent)

        # 2. Vrstva: LST (poloprůhledná) [cite: 18]
        im_lst = ax.imshow(lst_matrix, cmap='inferno', alpha=0.6, extent=extent)
        plt.colorbar(im_lst, label='Teplota povrchu [°C]')

        # 3. Vrstva: Hotspots (červená) [cite: 12]
        islands_display = np.where(heat_island_mask, 1.0, np.nan)
        im_hot = ax.imshow(islands_display, cmap='Reds', vmin=0, vmax=1, extent=extent)

        ax.set_title("Hotspots (Mezerník = přepnout mapu)")
        layers = [im_lst, im_hot]

        # Logika přepínání klávesou
        def on_key(event):
            if event.key == ' ':
                for layer in layers:
                    layer.set_visible(not layer.get_visible())
                fig.canvas.draw()

        fig.canvas.mpl_connect('key_press_event', on_key)
        plt.show()

    def plot_vegetation_vs_heat(self, ndvi_matrix, lst_matrix):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        extent = self._get_extent(ndvi_matrix)
        layers = []

        # Příprava klasifikace povrchu (NDVI) [cite: 13, 19]
        h, w = ndvi_matrix.shape
        rgb_map = np.zeros((h, w, 3))
        water_mask = ndvi_matrix < -0.1
        land_mask = (ndvi_matrix >= -0.1) & (ndvi_matrix < 0.2)
        veg_mask = ndvi_matrix >= 0.2

        rgb_map[water_mask] = [0, 0.3, 0.8]
        rgb_map[land_mask] = [0.9, 0.8, 0.4]
        rgb_map[veg_mask] = [0.1, 0.6, 0.1]

        for ax, data_img, title in zip([ax1, ax2], [rgb_map, lst_matrix], ["NDVI", "LST"]):
            if self._bg_image is not None:
                ax.imshow(self._bg_image, extent=extent)

            # Vykreslení datové vrstvy
            cmap = None if title == "NDVI" else 'magma'
            alpha = 0.7 if self._bg_image is not None else 1.0

            im = ax.imshow(data_img, cmap=cmap, alpha=alpha, extent=extent)
            layers.append(im)
            ax.set_title(f"{title} (Mezerník = přepnout)")

        def on_key(event):
            if event.key == ' ':
                for layer in layers:
                    layer.set_visible(not layer.get_visible())
                fig.canvas.draw()

        fig.canvas.mpl_connect('key_press_event', on_key)
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