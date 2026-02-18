import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ── Color palette ──────────────────────────────────────────────────────────────
GLOBAL_NORTH = "#156082"
GLOBAL_SOUTH = "#FFDC33"

# ── Data ───────────────────────────────────────────────────────────────────────
categories = ["Education", "Social &\nCommunity", "Neuroscience", "Health &\nCare", "Communications", "Tech &\nComputing"]

data = {
    "Initial Application": {
        "Global North": [24, 53, 21, 1, 1, 0],
        "Global South": [28, 18,  5, 2, 0, 1],
    },
    "Extended": {
        "Global North": [25, 57, 18, 0, 0, 0],
        "Global South": [38, 38, 13, 13, 0, 0],
    },
    "Interview": {
        "Global North": [18, 64, 18, 0, 0, 0],
        "Global South": [50, 50,  0, 0, 0, 0],
    },
    "Awarded": {
        "Global North": [0, 40, 60, 0, 0, 0],
        "Global South": [0, 100, 0, 0, 0, 0],
    },
}

stages = list(data.keys())
n_cats = len(categories)
x = np.arange(n_cats)
bar_w = 0.35

# ── Plot ───────────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 4, figsize=(20, 6), sharey=True)
fig.suptitle("RfP1 – Application Breakdown by Stage & Region", fontsize=15, fontweight="bold", y=1.02)

for ax, stage in zip(axes, stages):
    gn = data[stage]["Global North"]
    gs = data[stage]["Global South"]

    bars_gn = ax.bar(x - bar_w / 2, gn, bar_w, label="Global North", color=GLOBAL_NORTH, edgecolor="white", linewidth=0.5)
    bars_gs = ax.bar(x + bar_w / 2, gs, bar_w, label="Global South", color=GLOBAL_SOUTH, edgecolor="white", linewidth=0.5)

    # Value labels on bars
    for bar in bars_gn:
        h = bar.get_height()
        if h > 0:
            ax.text(bar.get_x() + bar.get_width() / 2, h + 1, f"{int(h)}%",
                    ha="center", va="bottom", fontsize=8, color=GLOBAL_NORTH, fontweight="bold")
    for bar in bars_gs:
        h = bar.get_height()
        if h > 0:
            ax.text(bar.get_x() + bar.get_width() / 2, h + 1, f"{int(h)}%",
                    ha="center", va="bottom", fontsize=8, color="#b8960a", fontweight="bold")

    ax.set_title(stage, fontsize=12, fontweight="bold", pad=8)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=8, ha="center")
    ax.set_ylim(0, 115)
    ax.spines[["top", "right"]].set_visible(False)
    ax.yaxis.set_tick_params(labelleft=True)
    ax.set_ylabel("Percentage (%)" if ax == axes[0] else "")
    ax.grid(axis="y", linestyle="--", alpha=0.4)

# ── Legend ─────────────────────────────────────────────────────────────────────
legend_handles = [
    mpatches.Patch(color=GLOBAL_NORTH, label="Global North"),
    mpatches.Patch(color=GLOBAL_SOUTH, label="Global South"),
]
fig.legend(handles=legend_handles, loc="lower center", ncol=2, fontsize=11,
           bbox_to_anchor=(0.5, -0.06), frameon=False)

plt.tight_layout()
plt.savefig("rfp1_global_visualization.png", dpi=150, bbox_inches="tight")
plt.show()
print("Saved: rfp1_global_visualization.png")
