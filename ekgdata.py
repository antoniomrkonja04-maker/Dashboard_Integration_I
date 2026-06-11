import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.signal import find_peaks as scipy_find_peaks


class EKGdata:

    def __init__(self, ekg_dict):
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['Messwerte in mV', 'Zeit in ms'])
        self.df = self.df.reset_index(drop=True)
        self.peaks = []

    def find_peaks(self):
        values = self.df['Messwerte in mV'].to_numpy()
        times = self.df['Zeit in ms'].to_numpy()

        ms_per_sample = np.mean(np.diff(times))
        min_distance_samples = int(300 / ms_per_sample)
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
        # Ersten n_points Samples fuer den Plot
        plot_df = self.df.head(n_points)
        hr = self.estimate_hr()
        title = f'EKG Signal mit Peaks (HR: {hr} bpm)' if hr else 'EKG Signal mit Peaks'

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=plot_df['Zeit in ms'],
            y=plot_df['Messwerte in mV'],
            mode='lines',
            name='EKG'
        ))

        # Nur Peaks die innerhalb der ersten n_points Samples liegen
        visible_peaks = [p for p in self.peaks if p < n_points]
        if visible_peaks:
            fig.add_trace(go.Scatter(
                x=self.df.loc[visible_peaks, 'Zeit in ms'],
                y=self.df.loc[visible_peaks, 'Messwerte in mV'],
                mode='markers',
                marker=dict(color='red', size=8),
                name='Peaks'
            ))

        fig.update_layout(
            title=title,
            xaxis_title='Zeit in ms',
            yaxis_title='Messwerte in mV'
        )
        return fig
