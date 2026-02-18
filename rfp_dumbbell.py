import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Jacobs Foundation palette ──────────────────────────────────────────────────
JF_NAVY   = "#003865"   # RfP1 dots  (established round)
JF_ORANGE = "#E87722"   # RfP2 dots  (new round)
JF_GREEN  = "#5C9E31"   # line: value grew   RfP1 → RfP2
JF_RED    = "#C0392B"   # line: value shrank RfP1 → RfP2
JF_GRAY   = "#BBBBBB"   # line: no change
JF_BG     = "#F8FAFC"   # panel background

# ── Categories ─────────────────────────────────────────────────────────────────
# Molecular & Genetics omitted (all zeros both rounds)
cats = [
    "Education & Learning",
    "Social & Cultural",
    "Neuroscience & Cog. Neuro",
    "Health & Clinical",
    "Communications",
    "Tech & Computational",
    "Policy & Public Health ★",   # ★ = new category in RfP2
]

stages  = ["Initial Application", "Extended Review", "Interview", "Awarded"]
regions = ["Global North", "Global South"]

# ── Data [cat_idx][stage_idx] ─────────────────────────────────────────────────
VALS = {
    "RfP1": {
        "Global North": [
            [24, 25, 18,  0],   # Education & Learning
            [53, 57, 64, 40],   # Social & Cultural
            [21, 18, 18, 60],   # Neuroscience & Cog. Neuro
            [ 1,  0,  0,  0],   # Health & Clinical
            [ 1,  0,  0,  0],   # Communications
            [ 0,  0,  0,  0],   # Tech & Computational
            [ 0,  0,  0,  0],   # Policy (not in RfP1)
        ],
        "Global South": [
            [53, 38, 50,  0],
            [34, 38, 50,100],
            [ 8, 13,  0,  0],
            [ 3, 13,  0,  0],
            [ 0,  0,  0,  0],
            [ 2,  0,  0,  0],
            [ 0,  0,  0,  0],   # Policy (not in RfP1)
        ],
    },
    "RfP2": {
        "Global North": [
            [26, 31, 25, 50],
            [53, 49, 60, 50],
            [14, 15,  0,  0],
            [ 0,  0,  0,  0],
            [ 3,  0,  0,  0],
            [ 1,  0,  0,  0],
            [ 3,  4, 15,  0],   # Policy
        ],
        "Global South": [
            [55, 46, 38, 50],
            [33, 41, 31, 25],
            [ 6, 11, 23,  0],
            [ 3,  0,  0,  0],
            [ 0,  0,  0,  0],
            [ 1,  0,  0,  0],
            [ 1,  3,  8, 25],   # Policy
        ],
    },
}

# ── Figure layout (2 rows = regions, 4 cols = stages) ─────────────────────────
fig = make_subplots(
    rows=2, cols=4,
    column_titles=[f"<b>{s}</b>" for s in stages],
    row_titles=[f"<b>{r}</b>" for r in regions],
    shared_xaxes=True,
    shared_yaxes=True,
    horizontal_spacing=0.04,
    vertical_spacing=0.18,
)

shown = {"RfP1": False, "RfP2": False}

for r_idx, region in enumerate(regions):
    for s_idx, stage in enumerate(stages):
        row, col = r_idx + 1, s_idx + 1

        for c_idx, cat in enumerate(cats):
            v1 = VALS["RfP1"][region][c_idx][s_idx]
            v2 = VALS["RfP2"][region][c_idx][s_idx]

            if v1 == 0 and v2 == 0:
                continue

            # Connecting line – color encodes direction of change
            lcolor = JF_GREEN if v2 > v1 else (JF_RED if v2 < v1 else JF_GRAY)

            fig.add_trace(go.Scatter(
                x=[v1, v2], y=[cat, cat],
                mode="lines",
                line=dict(color=lcolor, width=2.5),
                showlegend=False,
                hoverinfo="skip",
            ), row=row, col=col)

            # RfP1 dot
            fig.add_trace(go.Scatter(
                x=[v1], y=[cat],
                mode="markers",
                marker=dict(color=JF_NAVY, size=12, symbol="circle",
                            line=dict(color="white", width=1.5)),
                name="RfP1",
                legendgroup="rfp1",
                showlegend=not shown["RfP1"],
                hovertemplate=(
                    f"<b>RfP1</b> · {region}<br>"
                    f"{cat}<br>{stage}: <b>{v1}%</b><extra></extra>"
                ),
            ), row=row, col=col)
            shown["RfP1"] = True

            # RfP2 dot
            fig.add_trace(go.Scatter(
                x=[v2], y=[cat],
                mode="markers",
                marker=dict(color=JF_ORANGE, size=12, symbol="circle",
                            line=dict(color="white", width=1.5)),
                name="RfP2",
                legendgroup="rfp2",
                showlegend=not shown["RfP2"],
                hovertemplate=(
                    f"<b>RfP2</b> · {region}<br>"
                    f"{cat}<br>{stage}: <b>{v2}%</b><extra></extra>"
                ),
            ), row=row, col=col)
            shown["RfP2"] = True

# Invisible dummy traces to add line-colour legend entries
for lc, ln in [
    (JF_GREEN, "Increased RfP1 → RfP2"),
    (JF_RED,   "Decreased RfP1 → RfP2"),
    (JF_GRAY,  "No change"),
]:
    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode="lines",
        line=dict(color=lc, width=2.5),
        name=ln,
        showlegend=True,
    ), row=1, col=1)

# ── Axes ───────────────────────────────────────────────────────────────────────
fig.update_xaxes(
    range=[-3, 105],
    ticksuffix="%",
    gridcolor="#E5E5E5",
    zeroline=False,
    tickfont=dict(size=9),
)
fig.update_yaxes(
    gridcolor="#E5E5E5",
    zeroline=False,
    tickfont=dict(size=10),
    categoryorder="array",
    categoryarray=list(reversed(cats)),  # puts Education at top
)

# ── Colour-code the column (stage) title annotations ──────────────────────────
# Column titles appear as the first 4 annotations in make_subplots output
STAGE_COLORS = ["#003865", "#0077C8", "#E87722", "#5C9E31"]
for i, color in enumerate(STAGE_COLORS):
    fig.layout.annotations[i].font.color = color
    fig.layout.annotations[i].font.size  = 13

# Row title annotations come after column titles (indices 4 and 5)
for i in range(4, 6):
    fig.layout.annotations[i].font.color = JF_NAVY
    fig.layout.annotations[i].font.size  = 13

# ── Overall layout ─────────────────────────────────────────────────────────────
fig.update_layout(
    title=dict(
        text=(
            "<b>RfP1 vs RfP2</b> – Category Share Across the Selection Funnel"
            "<br><sup>★ Policy & Public Health is a new category introduced in RfP2</sup>"
        ),
        x=0.5, xanchor="center",
        font=dict(size=16, color=JF_NAVY, family="Arial"),
    ),
    height=700,
    legend=dict(
        orientation="h",
        yanchor="bottom", y=-0.18,
        xanchor="center", x=0.5,
        font=dict(size=11, family="Arial"),
        traceorder="normal",
        itemsizing="constant",
    ),
    paper_bgcolor="white",
    plot_bgcolor=JF_BG,
    font=dict(family="Arial", color="#333"),
    margin=dict(t=110, b=140, l=190, r=100),
)

fig.show()
fig.write_html("rfp_dumbbell.html")
print("Saved: rfp_dumbbell.html")
