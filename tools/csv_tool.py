import pandas as pd

class CSVTool:
    def load(self, filepath):
        df = pd.read_csv(filepath)
        print("[LOG] CSV Loaded")
        return df
