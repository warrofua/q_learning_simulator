import matplotlib.pyplot as plt
import pandas as pd
from IPython.display import display, clear_output

class StatePlot:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(6, 3))
        plt.ion()  # Enable interactive mode for real-time updates

    def update_plot(self, state_time_series):
        """Update the plot with a new frame of state time series data."""
        # Clearing the plot for each update
        self.ax.clear()

        # Setting titles and labels
        self.ax.set_title('State Changes Over Time')
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('State Values')
        self.ax.grid(True, linestyle='--', linewidth=0.5)

        # If state_time_series is empty, skip plotting
        if not state_time_series:
            return

        # Converting state_time_series to DataFrame for plotting
        df_states = pd.DataFrame(state_time_series)
        if 'Timestamp' not in df_states:
            df_states['Timestamp'] = pd.to_datetime(df_states.index)
        df_states.set_index('Timestamp', inplace=True)

        # Plotting each state
        for state in df_states.columns.difference(['Timestamp']):
            self.ax.plot(df_states.index, df_states[state], label=state)

        self.ax.legend()

        # Handling display updates
        clear_output(wait=True)  # Optionally clear previous outputs to manage display space
        display(self.fig)  # Display the updated figure
        plt.pause(0.01)  # Short pause to ensure the plot updates are visible

    def close(self):
        """Optional: Close the plot explicitly if needed."""
        plt.close(self.fig)