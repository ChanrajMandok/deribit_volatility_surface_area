from typing import Dict
import plotly.graph_objects as go

    ###########################################################################
    # Service Plots Live Volatility Surface Area from implied_volatilty_queue #
    ###########################################################################

class ServicePlotVolatilitySurfaceArea():
        
    def __init__(self):
        self.fig = go.Figure()
        self.surface_trace = go.Surface(
            x=[],
            y=[],
            z=[],
            colorscale='Viridis',
            showscale=True
        )
        self.fig.add_trace(self.surface_trace)

        self.fig.update_layout(
            scene=dict(
                xaxis=dict(title='Strike Price'),
                yaxis=dict(title='Days to Expiry'),
                zaxis=dict(title='Implied Volatilty'),
                aspectmode='manual',  # Ensure consistent scaling of axes
                aspectratio=dict(x=1, y=1, z=0.5),  # Adjust aspect ratio as needed
                camera=dict(
                    eye=dict(x=1.2, y=-1.2, z=0.8),  # Adjust camera position for optimal viewing
                    up=dict(x=0, y=0, z=1)
                )
            ),
            title='Deribit Volatility Surface Area',
            font=dict(size=12)
        )

        self.fig.update_coloraxes(colorbar=dict(
            title='Colorbar Title',
            len=0.5,  # Adjust length of colorbar
            y=0.5  # Adjust position of colorbar
        ))
        
    def plot(self, poo:Dict):
        print(poo)
        
