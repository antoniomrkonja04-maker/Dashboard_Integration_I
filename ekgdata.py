import json
import numpy as np
import pandas as pd
import plotly.express as px
from scipy.signal import find_peaks as scipy_find_peaks


class EKGdata:

    def __init__(self, ekg_dict):
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['Messwerte in mV', 'Zeit in ms'])
        self.df = self.df.iloc[:5000].reset_index(drop=True)
        self.peaks = []

    def find_peaks(self):
        values = self.df['Messwerte in mV'].to_numpy()
        times = self.df['Zeit in ms'].to_numpy()

        # Zeitaufloesung berechnen: ms pro Sample
        ms_per_sample = np.mean(np.diff(times))
        # 300ms Mindestabstand zwischen Peaks
        min_distance_samples = int(300 / ms_per_sample)

        # Schwellenwert: Mittelwert + 1 Standardabweichung
        threshold = np.mean(values) + np.std(values)

        peaks, _ = scipy_find_peaks(values, height=threshold, distance=min_distance_samples)
        self.peaks = list(peaks)
        return self.peaks

    def estimate_hr(self):
        if len(self.peaks) < 2:
            return None
        peak_times = self.df.loc[self.peaks, 'Zeit in ms'].to_numpy()
        intervals = np.diff(peak_times)
        if len(intervals) == 0 or np.mean(intervals) <= 0:
            return None
        return round(60000.0 / np.mean(intervals), 1)

    def plot_time_series(self, n_points=2000):
        plot_df = self.df.head(n_points)
        hr = self.estimate_hr()
        title = f'EKG Signal mit Peaks (HR: {hr} bpm)' if hr else 'EKG Signal mit Peaks'

        fig = px.line(plot_df, x='Zeit in ms', y='Messwerte in mV', title=title)

        peak_points = self.df.loc[self.peaks]
        peak_points = peak_points[peak_points['Zeit in ms'] <= plot_df['Zeit in ms'].iloc[-1]]
        if len(peak_points):
            fig.add_scatter(
                x=peak_points['Zeit in ms'],
                y=peak_points['Messwerte in mV'],
                mode='markers',
                marker=dict(color='red', size=8),
                name='Peaks'
            )
        return fig
