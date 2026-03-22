#!/usr/bin/env python3
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

file_dir = "ares"
os.makedirs(f"plots/{file_dir}", exist_ok=True)

df = pd.read_csv(f"./results/{file_dir}/raw_all.csv")
df["time"] = pd.to_numeric(df["time"], errors="coerce")
df = df.dropna(subset=["time"])

agg = df.groupby(["scaling", "n_points", "procs"])["time"].mean().reset_index()

for scaling in ["strong", "weak"]:
    sub = agg[agg["scaling"] == scaling].sort_values("procs")

    if scaling == "weak":
        sub = sub.copy()
        sub["n_per_proc"] = sub["n_points"] / sub["procs"]
        group_col = "n_per_proc"
    else:
        group_col = "n_points"

    procs_vals = sorted(sub["procs"].unique())
    sizes = sorted(sub[group_col].unique())

    # --- time: 3 subploty obok siebie ---
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle(f"{scaling.capitalize()} scaling - execution time")
    for ax, size in zip(axes, sizes):
        
        grp = sub[sub[group_col] == size].sort_values("procs")
        ax.plot(grp["procs"], grp["time"],
                marker="o", linestyle="--", linewidth=1, color="#185FA5")
        ax.set_title(f"{group_col}={int(size):,}")
        ax.set_xlabel("Number of processes")
        ax.set_ylabel("Time [s]")
        ax.set_ylim(bottom=0, top=grp["time"].max()*1.1)
        ax.xaxis.set_major_locator(ticker.FixedLocator(procs_vals))
        ax.grid(alpha=0.35)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    plt.tight_layout()
    plt.savefig(f"plots/{file_dir}/{scaling}_time.png", dpi=150)
    plt.close()

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle(f"{scaling.capitalize()} scaling - speedup")
    for ax, size in zip(axes, sizes):
        ax.set_ylim(bottom=0)
        grp = sub[sub[group_col] == size].sort_values("procs")
        t1 = grp[grp["procs"] == 1]["time"].values
        if len(t1) == 0:
            continue
        speedup = t1[0] / grp["time"]
        ax.plot(grp["procs"], speedup,
                marker="o", linestyle="--", linewidth=1, color="#185FA5")
        ax.set_title(f"{group_col}={int(size):,}")
        ax.set_xlabel("Number of processes")
        ax.set_ylabel("Speedup S(p)")
        ax.set_ylim(bottom=0)
        if scaling == "weak":
            ax.set_ylim(top=1.2)
        else:
            ax.set_ylim(top=12)
        ax.xaxis.set_major_locator(ticker.FixedLocator(procs_vals))
        ax.grid(alpha=0.35)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        if scaling == "strong":
            ax.plot(procs_vals, procs_vals, color="black",
                    linestyle="-", linewidth=0.8, alpha=0.4, label="Ideal S = p")
            ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
        else:
            ax.axhline(1.0, color="black", linestyle="-",
                       linewidth=0.8, alpha=0.4, label="Ideal S = 1")
            ax.yaxis.set_major_locator(ticker.MultipleLocator(0.2))
        ax.legend()
    plt.tight_layout()
    plt.savefig(f"plots/{file_dir}/{scaling}_speedup.png", dpi=150)
    plt.close()

print(f"Done. Plots saved to plots/{file_dir}/")