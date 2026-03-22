#!/usr/bin/env python3
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
file_dir="vcluster"
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

    fig, ax = plt.subplots(figsize=(7, 5))
    for size, grp in sub.groupby(group_col):
        ax.plot(grp["procs"], grp["time"],
                marker="o", linestyle="--", linewidth=1, label=f"{group_col}={int(size):,}")
    if scaling == "strong":
        ax.set_ylim(0, 0.7)
    
    else:
        ax.set_ylim(0, 0.35)
    ax.set_xlabel("Number of processes")
    ax.set_ylabel("Time [s]")
    ax.set_title(f"{scaling.capitalize()} scaling - execution time")
    ax.xaxis.set_major_locator(ticker.FixedLocator(procs_vals))
    ax.legend()
    ax.grid(alpha=0.35)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    plt.savefig(f"plots/{file_dir}/{scaling}_time.png", dpi=150)
    plt.close()

    fig, ax = plt.subplots(figsize=(7, 5))
    for size, grp in sub.groupby(group_col):
        grp = grp.sort_values("procs")
        t1 = grp[grp["procs"] == 1]["time"].values
        if len(t1) == 0:
            continue
        speedup = t1[0] / grp["time"]
        ax.plot(grp["procs"], speedup,
                marker="o", linestyle="--", linewidth=1, label=f"{group_col}={int(size):,}")

    if scaling == "strong":
        ax.set_ylim(0, 12)
        ax.plot(procs_vals, procs_vals, color="black",
                linestyle="-", linewidth=0.8, alpha=0.4, label="Ideal S = p")
        ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
    else:
        ax.set_ylim(0, 1.1)
        ax.yaxis.set_major_locator(ticker.MultipleLocator(0.2))
        ax.axhline(1.0, color="black", linestyle="-",
                   linewidth=0.8, alpha=0.4, label="Ideal S = 1")

    ax.set_xlabel("Number of processes")
    ax.set_ylabel("Speedup S(p)")
    ax.set_title(f"{scaling.capitalize()} scaling - speedup")
    ax.xaxis.set_major_locator(ticker.FixedLocator(procs_vals))
        
    ax.legend()
    ax.grid(alpha=0.35)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    plt.savefig(f"plots/{file_dir}/{scaling}_speedup.png", dpi=150)
    plt.close()

print(f"Done. Plots saved to plots/{file_dir}/")