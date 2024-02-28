import ipywidgets as widgets
from IPython.display import display

def create_sliders():
    alpha_slider = widgets.FloatSlider(value=0.9, min=0.0, max=1.0, step=0.01, description='Alpha:')
    gamma_slider = widgets.FloatSlider(value=0.5, min=0.0, max=1.0, step=0.01, description='Gamma:')
    epsilon_slider = widgets.FloatSlider(value=0.75, min=0.0, max=1.0, step=0.01, description='Epsilon:')
    return alpha_slider, gamma_slider, epsilon_slider

def create_run_button():
    run_button = widgets.Button(description='Run Simulation')
    return run_button

def display_gui(alpha_slider, gamma_slider, epsilon_slider, run_button):
    display(alpha_slider, gamma_slider, epsilon_slider, run_button)