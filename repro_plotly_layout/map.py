from typing import List

import reflex as rx
import plotly.graph_objects as go

import numpy as np
np.random.seed(1)

class MapState(rx.State):
    fig: go.Figure = go.Figure()
    colors: List[str] = ['#a3a7e4'] * 100
    size: List[int] = [10] * 100
    selected_points: List[tuple[int, int]] = []

    def load_map(self):
        x = np.random.rand(100)
        y = np.random.rand(100)
        self.fig = go.Figure([go.Scatter(x=x, y=y, mode='markers')])

        scatter = self.fig.data[0]
        scatter.marker.color = self.colors
        scatter.marker.size = self.size
        self.fig.layout.hovermode = 'closest'
        self.selected_points = []

    def update_point(self, event, points):
        # Get a reference to the scatter plot in the figure.
        scatter = self.fig.data[0]

        # Get mutable color and size lists for each point.
        c = list(scatter.marker.color)
        s = list(scatter.marker.size)

        # Update the point values.
        for point in points:
            print(f"Updating point {point['pointIndex']}")
            c[point["pointIndex"]] = '#bae2be'
            s[point["pointIndex"]] = 20
            self.selected_points.append((point["x"], point["y"]))

        # Assign the updated lists back to the plot.
        scatter.marker.color = c
        scatter.marker.size = s

        # Reassign the figure to the state trigger a frontend update.
        self.fig = self.fig


def map():
    return rx.container(
        rx.vstack(
            rx.heading("Map"),
            rx.link("< Back", href="/"),
            rx.plotly(
                data=MapState.fig,
                width="100%",
                height="100%",
                use_resize_handler=True,
                on_click=MapState.update_point,
            ),
            rx.hstack(
                rx.foreach(
                    MapState.selected_points,
                    lambda point: rx.badge(point.to_string()),
                ),
                flex_wrap="wrap",
            ),
            rx.button("Reload Map", on_click=MapState.load_map),
            # Here you can see what the browser gets to render the figure using react-plotly
            rx.code_block(MapState.fig.to_string(), wrap_long_lines=True, width="100%"),
        ),
        stack_children_full_width=True,
    )
