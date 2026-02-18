import plotly.graph_objects as go

# ── Colors ─────────────────────────────────────────────────────────────────────
GN_COLOR = "#156082"          # Global North node color
GS_COLOR = "#FFDC33"          # Global South node color
GN_LINK  = "rgba(21, 96, 130, 0.35)"
GS_LINK  = "rgba(255, 220, 51, 0.50)"

# ── Categories & Stages ────────────────────────────────────────────────────────
cats = [
    "Education & Learning",
    "Social & Cultural",
    "Neuroscience & Cog. Neuro",
    "Health & Clinical",
    "Communications",
    "Tech & Computational",
]

stages = ["Initial Application", "Extended Review", "Interview", "Awarded"]

# ── Data (percentages) ─────────────────────────────────────────────────────────
# Order matches cats list above
data_vals = [
    {"GN": [24, 53, 21,  1, 1, 0], "GS": [28, 18,  5,  2, 0, 1]},  # Initial Application
    {"GN": [25, 57, 18,  0, 0, 0], "GS": [38, 38, 13, 13, 0, 0]},  # Extended Review
    {"GN": [18, 64, 18,  0, 0, 0], "GS": [50, 50,  0,  0, 0, 0]},  # Interview
    {"GN": [ 0, 40, 60,  0, 0, 0], "GS": [ 0,100,  0,  0, 0, 0]},  # Awarded
]

# ── Node layout ────────────────────────────────────────────────────────────────
# Index formula: stage_idx * 12 + region_idx * 6 + cat_idx
# region 0 = GN (first 6 slots per stage), region 1 = GS (next 6 slots)

labels       = []
node_colors  = []

for s_idx, stage in enumerate(stages):
    for c_idx, cat in enumerate(cats):
        labels.append(f"<b>{cat}</b><br>Global North – {stage}")
        node_colors.append(GN_COLOR)
    for c_idx, cat in enumerate(cats):
        labels.append(f"<b>{cat}</b><br>Global South – {stage}")
        node_colors.append(GS_COLOR)

# ── Links ──────────────────────────────────────────────────────────────────────
src_list, tgt_list, val_list, col_list = [], [], [], []

for s_idx in range(len(stages) - 1):
    for r_idx, (region, lc) in enumerate([("GN", GN_LINK), ("GS", GS_LINK)]):
        for c_idx in range(len(cats)):
            s_node = s_idx * 12 + r_idx * 6 + c_idx
            t_node = (s_idx + 1) * 12 + r_idx * 6 + c_idx
            v = data_vals[s_idx + 1][region][c_idx]
            if v > 0:
                src_list.append(s_node)
                tgt_list.append(t_node)
                val_list.append(v)
                col_list.append(lc)

# ── Stage labels via annotations ───────────────────────────────────────────────
stage_x = [0.01, 0.34, 0.67, 0.99]
annotations = [
    dict(x=sx, y=1.06, xref="paper", yref="paper",
         text=f"<b>{stage}</b>", showarrow=False,
         font=dict(size=13, color="#333"), xanchor="center")
    for sx, stage in zip(stage_x, stages)
]

# ── Figure ─────────────────────────────────────────────────────────────────────
fig = go.Figure(go.Sankey(
    arrangement="snap",
    node=dict(
        pad=12,
        thickness=18,
        label=labels,
        color=node_colors,
        line=dict(color="white", width=0.5),
    ),
    link=dict(
        source=src_list,
        target=tgt_list,
        value=val_list,
        color=col_list,
    ),
))

fig.update_layout(
    title=dict(
        text="RfP1 – Application Flow by Stage & Region",
        font=dict(size=18, color="#222"),
        x=0.5,
        xanchor="center",
    ),
    annotations=annotations,
    height=720,
    margin=dict(t=100, b=20, l=20, r=20),
    font=dict(size=11, family="Arial"),
    paper_bgcolor="white",
)

fig.show()
fig.write_html("rfp1_sankey.html")
print("Saved: rfp1_sankey.html")
