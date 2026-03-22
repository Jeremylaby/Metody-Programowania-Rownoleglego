#!/usr/bin/env python3
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

os.makedirs("plots/pp", exist_ok=True)

df1 = pd.read_csv("results/pp/ping_pong_result_1.csv")
df2 = pd.read_csv("results/pp/ping_pong_result_2.csv")
df1["config"] = "1 node"
df2["config"] = "2 nodes"

df = pd.concat([df1, df2], ignore_index=True)


def format_bytes(x, _):
    if x >= 1_048_576:
        return f"{x/1_048_576:.0f} MB"
    elif x >= 1_024:
        return f"{x/1_024:.0f} KB"
    return f"{x:.0f} B"


colors = {"1 node": "#185FA5", "2 nodes": "#D85A30"}

# --- bandwidth ---
fig, ax = plt.subplots(figsize=(8, 5))
for config, grp in df.groupby("config"):
    ax.plot(grp["size_bytes"], grp["bandwidth_mbit_s"],
            marker="o", linestyle="--", linewidth=1,
            color=colors[config], label=config)
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel("Message size")
ax.set_ylabel("Bandwidth [Mbit/s]")
ax.set_title("P2P bandwidth (MPI_Send/MPI_Recv)")
ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_bytes))
ax.xaxis.set_major_locator(ticker.LogLocator(base=4))
plt.xticks(rotation=30, ha="right")
ax.set_ylim(bottom=0)
ax.legend()
ax.grid(alpha=0.35)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.savefig("plots/pp/bandwidth.png", dpi=150)
plt.close()

# --- latency ---
fig, ax = plt.subplots(figsize=(8, 5))
for config, grp in df.groupby("config"):
    ax.plot(grp["size_bytes"], grp["latency_ms"],
            marker="o", linestyle="--", linewidth=1,
            color=colors[config], label=config)
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel("Message size")
ax.set_ylabel("Latency [ms]")
ax.set_title("P2P latency (MPI_Send/MPI_Recv)")
ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_bytes))
ax.xaxis.set_major_locator(ticker.LogLocator(base=4))
plt.xticks(rotation=30, ha="right")
ax.set_ylim(bottom=0)
ax.legend()
ax.grid(alpha=0.35)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.savefig("plots/pp/latency.png", dpi=150)
plt.close()

print("Done. Plots saved to plots/pp/")

# --- print latency for 1B (opoznienie) ---
for config, grp in df.groupby("config"):
    row = grp[grp["size_bytes"] == 1]
    if not row.empty:
        print(f"Latency 1B [{config}]: {row['latency_ms'].values[0]:.6f} ms")
