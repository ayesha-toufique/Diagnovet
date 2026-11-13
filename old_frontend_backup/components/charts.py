"""Shared Plotly Chart Helper for Diagnovet.

Ensures all charts strictly adhere to the Lagoon theme colorway,
transparent background, clean typography, and responsive margins.
"""

from typing import List, Dict, Any
import plotly.graph_objects as go
import streamlit as st
from components.theme import PLOTLY_COLORWAY, LAGOON_TEXT, LAGOON_LINE, LAGOON_MUTED


def apply_lagoon_layout(
    fig: go.Figure, title: str = "", height: int = 340
) -> go.Figure:
    """Applies uniform Lagoon theme styling to any Plotly figure."""
    fig.update_layout(
        title={
            "text": title,
            "font": {"family": "Inter, sans-serif", "size": 16, "color": LAGOON_TEXT},
            "x": 0.02,
            "xanchor": "left",
        },
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        colorway=PLOTLY_COLORWAY,
        font={"family": "Inter, sans-serif", "color": LAGOON_TEXT, "size": 12},
        margin={"l": 40, "r": 30, "t": 50, "b": 40},
        height=height,
        xaxis={
            "gridcolor": LAGOON_LINE,
            "zerolinecolor": LAGOON_LINE,
            "tickfont": {"color": LAGOON_MUTED},
        },
        yaxis={
            "gridcolor": LAGOON_LINE,
            "zerolinecolor": LAGOON_LINE,
            "tickfont": {"color": LAGOON_MUTED},
        },
        legend={"font": {"color": LAGOON_TEXT}, "bgcolor": "rgba(255,255,255,0.4)"},
    )
    return fig


def render_confidence_bar_chart(
    conditions: List[str],
    confidences: List[int],
    title: str = "Condition Likelihood Match (%)",
):
    """Horizontal bar chart comparing condition confidence scores."""
    # Reverse order so top item appears at top
    rev_conditions = list(reversed(conditions))
    rev_confidences = list(reversed(confidences))

    fig = go.Figure(
        go.Bar(
            x=rev_confidences,
            y=rev_conditions,
            orientation="h",
            marker={
                "color": rev_confidences,
                "colorscale": [[0.0, "#2E7DFF"], [0.5, "#00C9A7"], [1.0, "#8A5CFF"]],
                "line": {"width": 0},
            },
            text=[f"{c}%" for c in rev_confidences],
            textposition="inside",
            insidetextanchor="middle",
            textfont={"color": "#FFFFFF", "size": 12, "family": "Inter, sans-serif"},
        )
    )

    fig = apply_lagoon_layout(fig, title=title, height=260)
    fig.update_xaxes(range=[0, 100], title="Concordance Score (%)")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def render_criteria_comparison_chart(
    criteria: List[Dict[str, Any]], title: str = "Decision Evaluation Matrix"
):
    """Grouped bar chart for DSS criteria weights vs actual matched scores."""
    labels = [c["Criterion"] for c in criteria]
    weights = [c["Weight"] for c in criteria]
    scores = [c["Score"] for c in criteria]

    fig = go.Figure()
    fig.add_trace(
        go.Bar(name="Criterion Weight (%)", x=labels, y=weights, marker_color="#2E7DFF")
    )
    fig.add_trace(
        go.Bar(
            name="Evaluated Score (0-100)", x=labels, y=scores, marker_color="#00C9A7"
        )
    )

    fig = apply_lagoon_layout(fig, title=title, height=320)
    fig.update_layout(barmode="group")
    fig.update_yaxes(range=[0, 100])
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
