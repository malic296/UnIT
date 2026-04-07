from services.satellite_data_service import SatelliteDataService

def main():
    satellite = SatelliteDataService()
    ndvi_matrix, shape = satellite.get_ndvi_matrix()

    lst_matrix = satellite.get_lst_matrix(target_shape=shape)

    print("hi")

if __name__ == '__main__':
    main()