import matplotlib.pyplot as plt
from IPython.display import clear_output, display

class OrganismPlot:
    def __init__(self, behavior_positions):
        self.behavior_positions = behavior_positions
        # Creating a figure and axis for plotting
        self.fig, self.ax = plt.subplots(figsize=(4, 4))
        plt.ion()  # Enable interactive mode

    def update_plot(self, organism_positions):
        # Assuming interactive mode is on, we clear the figure to prevent overlay issues
        self.ax.clear()  # Clear the axis to redraw

        # Unpack organism_positions into x and y coordinates
        if organism_positions:  # Check if the list is not empty
            x_positions, y_positions = zip(*organism_positions)
            self.ax.plot(x_positions, y_positions, marker='o', linestyle='-', color='grey', alpha=0.5)
            self.ax.scatter([x_positions[-1]], [y_positions[-1]], color='red', zorder=5)
        else:  # Handle the case where organism_positions is empty
            x_positions, y_positions = [], []

        # Plot behavior positions
        for behavior, position in self.behavior_positions.items():
            self.ax.scatter(*position, label=behavior, zorder=5)

        # Set plot limits and labels
        self.ax.set_xlim(-1, 1)
        self.ax.set_ylim(-1, 1)
        self.ax.axhline(0, color='black', linewidth=0.5)
        self.ax.axvline(0, color='black', linewidth=0.5)
        self.ax.grid(True, linestyle='--', linewidth=0.5)
        self.ax.legend()

        # Adjustments for real-time display
        clear_output(wait=True)  # Optionally clear previous outputs to manage display space
        display(self.fig)  # Display the updated figure
        plt.pause(0.05)  # Short pause to ensure the plot updates are rendered