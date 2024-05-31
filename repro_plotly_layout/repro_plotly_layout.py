"""Welcome to Reflex! This file outlines the steps to create a basic app."""
from copy import deepcopy

import reflex as rx

from rxconfig import config

from .annotation import fig as annotation_fig
from .map import MapState, map
from .restyle import fig as restyle_fig
from .yahoo import fig as yahoo_fig


import plotly.express as px
data_canada = px.data.gapminder().query("country == 'Canada'")
fig = px.bar(data_canada, x='year', y='pop', title="Canada's Population Over Time")

long_df = px.data.medals_long()
fig2 = px.bar(long_df, x="nation", y="count", color="medal", title="Long-Form Input")


df = px.data.gapminder()
fig = px.scatter(df, x="gdpPercap", y="lifeExp", animation_frame="year", animation_group="country",
           size="pop", color="continent", hover_name="country",
           log_x=True, size_max=55, range_x=[100,100000], range_y=[25,90])

fig["layout"].pop("updatemenus") # optional, drop animation buttons
#fig.update_layout(autosize=True)


class State(rx.State):
    """The app state."""
    f2 = annotation_fig

    def on_event(self, event_name, event):
        return rx.console_log(f"{event_name} {event}")

    def on_points(self, event_name, event, points):
        return rx.console_log(f"{event_name} {event} {points}")

    def on_button_click(self, menu, button, active):
        return rx.console.log(f"button click: {menu} {button} {active}")

    def on_click(self, event, points):
        for point in points:
            self.f2.data[point["curveNumber"]]["marker"]["color"] = "yellow"
            self.f2 = self.f2
            return rx._x.toast.info(f"Clicked point {point['pointIndex']}")

    def on_double_click(self, event):
        print(event)
        self.reset()


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Welcome to Reflex!", size="9"),
            rx.link("Interactive Scatter Map", href="/map"),
            rx.hstack(
                rx.plotly(
                    data=fig,
                    use_resize_handler=True,
                    width="50%",
                    height="100%",
                ),
                rx.plotly(
                    data=fig,
                    use_resize_handler=True,
                    width="50%",
                    height="100%",
                ),
                width="100%"
            ),
            rx.plotly(
                data=State.f2,
                on_after_plot=State.on_event("on_after_plot"),
                on_animated=State.on_event("on_animated", ""),
                on_animating_frame=State.on_event("on_animating_frame", ""),
                on_animation_interrupted=State.on_event("on_animation_interrupted", ""),
                on_autosize=State.on_event("on_autosize"),
                # seems to fire every time the mouse moves
                # on_before_hover=State.on_event("on_before_hover"),
                on_button_clicked=State.on_button_click,
                #on_click=State.on_points("on_click"),
                on_click=State.on_click,
                on_deselect=State.on_event("on_deselect", ""),
                on_double_click=State.on_double_click,
                on_hover=State.on_points("on_hover"),
                on_relayout=State.on_event("on_relayout"),
                on_relayouting=State.on_event("on_relayouting"),
                on_restyle=State.on_event("on_restyle"),
                on_redraw=State.on_event("on_redraw"),
                on_selected=State.on_points("on_selected"),
                on_selecting=State.on_points("on_selecting"),
                on_transitioning=State.on_event("on_transitioning"),
                on_transition_interrupted=State.on_event("on_transition_interrupted"),
                on_unhover=State.on_points("on_unhover"),
                use_resize_handler=True,
                width="100%",
                height="100vh",
            ),
        ),
        rx.plotly(
            data=fig2,
            use_resize_handler=True,
            width="100%",
            height="100vh",
        ),
        rx.plotly(
            data=restyle_fig,
            use_resize_handler=True,
            width="100%",
            height="100vh",
        ),
        rx.logo(),
    )


app = rx.App()
app.add_page(index)
app.add_page(map, route="/map", on_load=MapState.load_map)