import numpy as np

class MaskService:
    def __init__(self, vegetation_threshold=0.4, concrete_threshold=0.4):
        self.veg_threshold = vegetation_threshold
        self.con_threshold = concrete_threshold

    def get_vegetation_mask(self, ndvi_matrix):
        return ndvi_matrix >= self.veg_threshold

    def get_concrete_mask(self, ndvi_matrix):
        return (ndvi_matrix >= 0) & (ndvi_matrix < self.con_threshold)

    def get_water_mask(self, ndvi_matrix):
        return ndvi_matrix < 0