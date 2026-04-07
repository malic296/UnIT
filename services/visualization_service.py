import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import matplotlib
import matplotlib.image as mpimg
from pathlib import Path
matplotlib.use('Qt5Agg')

class VisualizationService:
    def __init__(self):
        plt.style.use('dark_background')
        self.picture_path = Path(__file__).parent.parent / "data" / "prague.png"
        self._bg_image = mpimg.imread(str(self.picture_path)) if self.picture_path.exists() else None

    def _get_extent(self, matrix):
        h, w = matrix.shape[:2]
        return [0, w, h, 0]

    def _setup_interaction(self, fig, layers, title_obj, main_title):
        def on_key(event):
            if event.key == ' ':
                visible = not layers[0].get_visible()
                for layer in layers:
                    layer.set_visible(visible)

                mode = "ANALÝZA" if visible else "MAPA"
                title_obj.set_text(f"{main_title} | Režim: {mode} (Mezerník pro změnu)")
                fig.canvas.draw_idle()

        fig.canvas.mpl_connect('key_press_event', on_key)

    def plot_heat_islands_on_map(self, lst_matrix, heat_island_mask):
        fig, ax = plt.subplots(figsize=(12, 8))
        ext = self._get_extent(lst_matrix)

        if self._bg_image is not None:
            ax.imshow(self._bg_image, extent=ext)

        l1 = ax.imshow(lst_matrix, cmap='inferno', alpha=1.0, extent=ext)

        islands = np.where(heat_island_mask, 1.0, np.nan)
        l2 = ax.imshow(islands, cmap='Reds', vmin=0, vmax=1, extent=ext)

        plt.colorbar(l1, ax=ax, label='Teplota povrchu [°C]', fraction=0.046, pad=0.04)

        t = ax.set_title(f"DETEKCE TEPELNÝCH OSTROVŮ | Režim: ANALÝZA (Mezerník pro změnu)")
        ax.axis('off')

        self._setup_interaction(fig, [l1, l2], t, "DETEKCE TEPELNÝCH OSTROVŮ")
        plt.show()

    def plot_vegetation_vs_heat(self, ndvi_matrix, lst_matrix):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        ext = self._get_extent(ndvi_matrix)

        h, w = ndvi_matrix.shape
        rgb = np.zeros((h, w, 3))
        rgb[ndvi_matrix < -0.06] = [0, 0.4, 0.9]
        rgb[(ndvi_matrix >= -0.06) & (ndvi_matrix < 0.2)] = [0.8, 0.7, 0.3]
        rgb[ndvi_matrix >= 0.2] = [0.1, 0.7, 0.1]

        layers = []
        for ax, img, cmap, title in zip([ax1, ax2], [rgb, lst_matrix], [None, 'magma'], ["VEGETACE", "TEPLOTA"]):
            if self._bg_image is not None:
                ax.imshow(self._bg_image, extent=ext)

            im = ax.imshow(img, cmap=cmap, alpha=1.0, extent=ext)
            layers.append(im)
            ax.axis('off')

        leg_cfg = [([0, 0.4, 0.9], 'Voda'), ([0.8, 0.7, 0.3], 'Zástavba/Beton'), ([0.1, 0.7, 0.1], 'Vegetace')]
        items = [Line2D([0], [0], color=c, lw=8, label=l) for c, l in leg_cfg]
        ax1.legend(handles=items, loc='lower left', title="Povrchy")

        plt.colorbar(layers[1], ax=ax2, label="Teplota [°C]", fraction=0.046, pad=0.04)

        main_t = fig.suptitle("SROVNÁNÍ VEGETACE A TEPLOTY | Režim: ANALÝZA (Mezerník pro změnu)", fontsize=14)

        def on_key(event):
            if event.key == ' ':
                vis = not layers[0].get_visible()
                for l in layers: l.set_visible(vis)
                mode = "ANALÝZA" if vis else "MAPA"
                main_t.set_text(f"SROVNÁNÍ VEGETACE A TEPLOTY | Režim: {mode} (Mezerník pro změnu)")
                fig.canvas.draw_idle()

        fig.canvas.mpl_connect('key_press_event', on_key)
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.show()

    def plot_correlation_scatter(self, ndvi_matrix, lst_matrix):
        x, y = ndvi_matrix.flatten()[::50], lst_matrix.flatten()[::50]
        mask = ~np.isnan(x) & ~np.isnan(y)
        x, y = x[mask], y[mask]

        plt.figure(figsize=(10, 6))
        plt.scatter(x, y, alpha=0.2, s=8, c=y, cmap='coolwarm')

        m, b = np.polyfit(x, y, 1)
        plt.plot(x, m * x + b, color='white', linestyle='--', linewidth=2, label=f'Ochlazovací trend')

        plt.xlabel("Míra zeleně (NDVI)")
        plt.ylabel("Povrchová teplota [°C]")
        plt.title("DŮKAZ: Jak zeleň snižuje teplotu v Praze")
        plt.legend()
        plt.grid(alpha=0.1)
        plt.show()