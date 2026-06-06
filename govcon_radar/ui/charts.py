from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


CHART_TEMPLATE = "plotly_dark"
TEAL = "#2dd4bf"
BLUE = "#60a5fa"
AMBER = "#f59e0b"
ROSE = "#fb7185"
VIOLET = "#a78bfa"


def agency_obligation_bar(df: pd.DataFrame) -> go.Figure:
    fig = px.bar(
        df,
        x="obligations",
        y="agency",
        orientation="h",
        color="small_business_obligations",
        color_continuous_scale=[BLUE, TEAL],
        template=CHART_TEMPLATE,
        labels={
            "agency": "Agency",
            "obligations": "Obligations",
            "small_business_obligations": "Small Business",
        },
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"}, height=380)
    return fig


def vehicle_donut(df: pd.DataFrame) -> go.Figure:
    fig = px.pie(
        df,
        names="contract_vehicle",
        values="obligations",
        hole=0.55,
        template=CHART_TEMPLATE,
        color_discrete_sequence=[TEAL, BLUE, AMBER, ROSE, VIOLET],
    )
    fig.update_layout(height=360, showlegend=True)
    return fig


def contractor_score_scatter(df: pd.DataFrame) -> go.Figure:
    fig = px.scatter(
        df,
        x="total_obligations",
        y="composite_score",
        size="award_count",
        color="primary_agency",
        hover_name="contractor",
        hover_data=["core_capability", "small_business_partnering_rate"],
        template=CHART_TEMPLATE,
        labels={
            "total_obligations": "Total Obligations",
            "composite_score": "Partner Score",
            "primary_agency": "Primary Agency",
        },
    )
    fig.update_layout(height=420)
    return fig


def capability_pipeline_bar(df: pd.DataFrame) -> go.Figure:
    fig = px.bar(
        df,
        x="estimated_pipeline",
        y="capability",
        orientation="h",
        color="small_business_pull",
        template=CHART_TEMPLATE,
        color_discrete_sequence=[TEAL, BLUE, AMBER],
        labels={
            "estimated_pipeline": "Estimated Pipeline",
            "capability": "Capability",
            "small_business_pull": "Small Business Pull",
        },
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"}, height=360)
    return fig
