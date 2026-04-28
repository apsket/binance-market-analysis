import matplotlib.pyplot as plt


def plot_market_overview(df, title="Market Overview"):
    fig, ax1 = plt.subplots()

    # Price axis
    ax1.plot(df["open_time"], df["vwap"], label="VWAP")
    ax1.fill_between(df["open_time"], df["low"], df["high"], alpha=0.2)
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Price")

    # Volume axis
    ax2 = ax1.twinx()
    ax2.bar(df["open_time"], df["volume"], alpha=0.2)
    ax2.plot(df["open_time"], df["volume_baseline"], linestyle="--", color="red", label="Volume Baseline")
    ax2.set_ylabel("Volume")

    # Relative Volatility axis
    ax3 = ax1.twinx()
    ax3.spines["right"].set_position(("outward", 60))
    ax3.plot(df["open_time"], df["relative_volatility"], alpha=0.3, linestyle="--", color="orange", label="Relative Volatility")
    ax3.set_ylabel("Relative Volatility")

    # --- Legend handling ---
    lines, labels = [], []
    for ax in [ax1, ax2, ax3]:
        l, lab = ax.get_legend_handles_labels()
        lines += l
        labels += lab

    ax1.legend(lines, labels, loc="upper left")

    plt.title(title)
    fig.autofmt_xdate()
    plt.tight_layout()

    plt.close(fig)

    return fig, ax1, ax2, ax3
