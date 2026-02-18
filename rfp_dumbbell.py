import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import numpy as np

# ── Jacobs Foundation palette ──────────────────────────────────────────────────
JF_BLUE   = "#156082"
JF_YELLOW = "#FFDC33"
JF_TEAL   = "#91CFC4"
JF_RED    = "#C0392B"
JF_GRAY   = "#BBBBBB"
JF_BG     = "#F5FAFA"

# ── Categories & stages ────────────────────────────────────────────────────────
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

# ── Figure ────────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(
    2, 4, figsize=(24, 9),
    sharey=True, sharex=True,
    gridspec_kw={"hspace": 0.38, "wspace": 0.08},
)
fig.patch.set_facecolor("white")

y_pos = np.arange(len(cats))

for r_idx, region in enumerate(regions):
    for s_idx, stage in enumerate(stages):
        ax = axes[r_idx, s_idx]
        ax.set_facecolor(JF_BG)
        ax.spines[["top", "right", "left"]].set_visible(False)
        ax.spines["bottom"].set_color("#ddd")
        ax.tick_params(left=False)
        ax.grid(axis="x", color="#ddd", linewidth=0.7, zorder=0)
        ax.set_xlim(-3, 108)

        for c_idx in range(len(cats)):
            v1 = VALS["RfP1"][region][c_idx][s_idx]
            v2 = VALS["RfP2"][region][c_idx][s_idx]
            y  = y_pos[c_idx]

            if v1 == 0 and v2 == 0:
                continue

            is_policy_new = (c_idx == 6 and v1 == 0)

            # ── Connecting line ───────────────────────────────────────────────
            delta  = v2 - v1
            lcolor = JF_TEAL if delta > 0 else (JF_RED if delta < 0 else JF_GRAY)
            lstyle = "--" if is_policy_new else "-"

            ax.plot([v1, v2], [y, y],
                    color=lcolor, linewidth=2.4,
                    linestyle=lstyle, zorder=1, solid_capstyle="round")

            # ── Line caption: Δ pp label at midpoint ─────────────────────────
            mid_x = (v1 + v2) / 2
            if is_policy_new:
                caption = "new"
                cap_color = "#888"
            elif delta == 0:
                caption = "="
                cap_color = JF_GRAY
            else:
                sign    = "+" if delta > 0 else ""
                caption = f"{sign}{delta} pp"
                cap_color = lcolor

            # place caption above the line; nudge left if near right edge
            ha = "center"
            ax.text(mid_x, y + 0.30, caption,
                    ha=ha, va="bottom",
                    fontsize=7.5, color=cap_color, fontweight="bold",
                    zorder=5)

            # ── RfP1 dot ─────────────────────────────────────────────────────
            if v1 > 0:
                ax.scatter(v1, y, color=JF_BLUE, s=90, zorder=3,
                           edgecolors="white", linewidths=1.5)
                ax.text(v1, y - 0.30, f"{v1}%",
                        ha="center", va="top",
                        fontsize=7, color=JF_BLUE, fontweight="bold")

            # ── RfP2 dot ─────────────────────────────────────────────────────
            if v2 > 0:
                ax.scatter(v2, y, color=JF_YELLOW, s=90, zorder=4,
                           edgecolors="#999", linewidths=0.8)
                ax.text(v2, y - 0.30, f"{v2}%",
                        ha="center", va="top",
                        fontsize=7, color="#7a6000", fontweight="bold")

        # ── Y-axis labels only on left column ────────────────────────────────
        ax.set_yticks(y_pos)
        if s_idx == 0:
            ax.set_yticklabels(cats, fontsize=9.5)
        else:
            ax.set_yticklabels([])

        # ── Column headers ────────────────────────────────────────────────────
        if r_idx == 0:
            ax.set_title(stage, fontsize=11.5, fontweight="bold",
                         color=JF_BLUE, pad=10)

        # ── Row labels ────────────────────────────────────────────────────────
        if s_idx == 0:
            ax.set_ylabel(region, fontsize=11, fontweight="bold",
                          color=JF_BLUE, labelpad=10)

        # ── X-axis label on bottom row only ──────────────────────────────────
        if r_idx == 1:
            ax.set_xlabel("share (%)", fontsize=9, color="#555")

# ── Legend ────────────────────────────────────────────────────────────────────
legend_elements = [
    mpatches.Patch(facecolor=JF_BLUE,   edgecolor="white",  label="RfP1"),
    mpatches.Patch(facecolor=JF_YELLOW, edgecolor="#999",   label="RfP2"),
    mlines.Line2D([], [], color=JF_TEAL, linewidth=2,             label="Increased (RfP1 → RfP2)"),
    mlines.Line2D([], [], color=JF_RED,  linewidth=2,             label="Decreased (RfP1 → RfP2)"),
    mlines.Line2D([], [], color=JF_GRAY, linewidth=2,             label="No change"),
    mlines.Line2D([], [], color="#888",  linewidth=2, linestyle="--", label="New in RfP2 (no baseline)"),
]
fig.legend(handles=legend_elements, loc="lower center", ncol=6,
           fontsize=9.5, bbox_to_anchor=(0.5, -0.07), frameon=False)

# ── Title ─────────────────────────────────────────────────────────────────────
fig.suptitle(
    "RfP1 vs RfP2 – Category Share Across the Selection Funnel\n"
    "★ Policy & Public Health is a new category introduced in RfP2  |  "
    "Line labels show change in percentage points (pp)",
    fontsize=13, fontweight="bold", color=JF_BLUE, y=1.02,
)

plt.savefig("rfp_dumbbell.png", dpi=150, bbox_inches="tight")
plt.show()
print("Saved: rfp_dumbbell.png")
