import random
import matplotlib.pyplot as plt
import pandas as pd
from IPython.display import display, clear_output
from datetime import datetime, timedelta
import simulation_gui
from organism_plot import OrganismPlot
from state_plot import StatePlot

# Initialize Q-table
behaviors = ["Feeding", "Exploring", "Socializing", "Resting"]
Q = {behavior: 0 for behavior in behaviors}

# Initial counts and time-series
behavior_counts = {behavior: 0 for behavior in behaviors}
state_time_series = []
behavior_time_series = []

# Time
start_time = datetime.now()
end_time = start_time + timedelta(weeks=.25)
time_increment = timedelta(hours=.5) 

# States and associated behaviors, "Q- table"
states = {'Hunger': random.random(), 'Boredom': random.random(), 'Loneliness': random.random(), 'Tiredness': random.random()}
stateObj = {
    'Hunger': {'Q': 0, 'rewardRange': (0, 1), 'behavior': 'Feeding'}, 
    'Boredom': {'Q': 0, 'rewardRange': (0, 1), 'behavior': 'Exploring'},
    'Loneliness': {'Q': 0, 'rewardRange': (0, 1), 'behavior': 'Socializing'},
    'Tiredness': {'Q': 0, 'rewardRange': (0, 1), 'behavior': 'Resting'}
}

# Refined Reward Function with states parameter
def get_reward(behavior, states):
    effectiveness = random.uniform(0.25, 0.75)  # Simulate effectiveness of behavior
    for state, attributes in stateObj.items():
        if attributes['behavior'] == behavior:
            return effectiveness * (1 - states[state])  # Higher reward if state is more negative
    return 0

# Update state function
def update_states(behavior, states):
    for state in states:
        states[state] += random.uniform(.01, 0.2)
        states[state] = max(0, states[state])

    if behavior == "Feeding":
        states['Hunger'] -= random.uniform(0.33, 0.99)
    elif behavior == "Exploring":
        states['Boredom'] -= random.uniform(0.33, 0.99)
    elif behavior == "Socializing":
        states['Loneliness'] -= random.uniform(0.33, 0.99)
    elif behavior == "Resting":
        states['Tiredness'] -= random.uniform(0.33, 0.99)  

    for state in states:
        states[state] = min(1, max(0, states[state]))

# Time slice length
time_increment = timedelta(days=.1)  

# Create a list to store the frames
frames = []

# Mapping behaviors to quadrants
behavior_positions = {
    "Feeding": (-0.5, 0.5),  # Top-left quadrant
    "Exploring": (0.5, 0.5),  # Top-right quadrant
    "Socializing": (-0.5, -0.5),  # Bottom-left quadrant
    "Resting": (0.5, -0.5)  # Bottom-right quadrant
}

def run_simulation(alpha, gamma, epsilon, start_time, end_time, time_increment):
    organism_plotter = OrganismPlot(behavior_positions)
    state_plotter = StatePlot()

    organism_positions = []  # Track organism positions
    state_time_series = []   # Resetting here for a fresh simulation

    current_time = start_time
    while current_time <= end_time:

        # Behavior selection logic
        if random.random() < epsilon:
            behavior = random.choice(behaviors)
        else:
            # Choose the behavior with the highest Q-value
            max_state = max(stateObj, key=lambda k: stateObj[k]['Q'])
            behavior = stateObj[max_state]['behavior']

        organism_position = behavior_positions[behavior]  # Get the position for the selected behavior
        organism_positions.append(organism_position)  # Append position to the list

        # Reward calculation
        reward = get_reward(behavior, states)
        
        # Update states based on the chosen behavior
        update_states(behavior, states)
        
        # Q-value update
        for state, attributes in stateObj.items():
            if attributes['behavior'] == behavior:
                # Calculate the maximum Q-value for the next state
                max_future_q = max([s['Q'] for s in stateObj.values()])
                # Update the Q-value using the Q-learning formula
                attributes['Q'] = (1 - alpha) * attributes['Q'] + alpha * (reward + gamma * max_future_q)
        
        # Update behavior counts
        behavior_counts[behavior] += 1
        total_counts = sum(behavior_counts.values())
        normalized_behavior_counts = {k: v / total_counts for k, v in behavior_counts.items()}
        
        # Append current state and behavior to time series
        state_time_series.append({
            "Timestamp": current_time,
            **states  # Consider using normalized states if necessary
        })

        behavior_time_series.append({
            "Timestamp": current_time,
            **normalized_behavior_counts
        })

        # Prepare data for plotting
        df_states = pd.DataFrame(state_time_series)
        df_states['Timestamp'] = pd.to_datetime(df_states['Timestamp'])
        df_states.set_index('Timestamp', inplace=True)

        df_behaviors = pd.DataFrame(behavior_time_series)
        df_behaviors['Timestamp'] = pd.to_datetime(df_behaviors['Timestamp'])
        df_behaviors.set_index('Timestamp', inplace=True)

        # Update plots
        organism_plotter.update_plot(organism_positions)
        state_plotter.update_plot(state_time_series)

        plt.pause(0.01)  # Pause for update visibility

        # Increment time and continue the loop
        current_time += time_increment
    
# Function to handle button click event
def on_run_button_clicked(b):
    global state_time_series  # If you plan to use or modify it globally
    alpha = alpha_slider.value
    gamma = gamma_slider.value
    epsilon = epsilon_slider.value

    # Setup the simulation time frame
    start_time = datetime.now()
    end_time = start_time + timedelta(weeks=1)
    time_increment = timedelta(hours=1)

    # Reset necessary variables for a fresh simulation
    state_time_series = []  # Reinitialize if these are to be cleared before each run
    # No need to clear organism_positions here since it's handled within run_simulation

    # Run simulation with current slider values
    run_simulation(alpha, gamma, epsilon, start_time, end_time, time_increment)

alpha_slider, gamma_slider, epsilon_slider = simulation_gui.create_sliders()
run_button = simulation_gui.create_run_button()
run_button.on_click(on_run_button_clicked)
simulation_gui.display_gui(alpha_slider, gamma_slider, epsilon_slider, run_button)        