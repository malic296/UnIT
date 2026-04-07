from services import SatelliteDataService, VisualizationService, MaskService, AnalysisService

def main():
    satellite = SatelliteDataService()
    visualization = VisualizationService()
    mask = MaskService()
    analysis = AnalysisService()

    ndvi_matrix, shape = satellite.get_ndvi_matrix()
    lst_matrix = satellite.get_lst_matrix(target_shape=shape)

    veg_mask = mask.get_vegetation_mask(ndvi_matrix)
    concrete_mask = mask.get_concrete_mask(ndvi_matrix)

    heat_island_mask = analysis.identify_heat_islands(lst_matrix, percentile=90)

    cooling_report = analysis.analyze_cooling_effect(lst_matrix, veg_mask)
    correlation = analysis.get_correlation_coefficient(ndvi_matrix, lst_matrix)
    land_stats = analysis.get_land_cover_stats(ndvi_matrix, lst_matrix)

    visualization.plot_vegetation_vs_heat(ndvi_matrix, lst_matrix)
    visualization.plot_heat_islands_on_map(lst_matrix, heat_island_mask)
    visualization.plot_correlation_scatter(ndvi_matrix, lst_matrix)

    print("hi")

if __name__ == '__main__':
    main()