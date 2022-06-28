import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Dashboard import Dashboard


class OutliersDashboard(Dashboard):
    def __init__(self, dataset):
        super().__init__(dataset)
