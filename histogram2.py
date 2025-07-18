import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def load_data(path: str) -> pd.DataFrame:
    
    df = pd.read_parquet(path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


def compute_instantaneous_speed(group: pd.DataFrame) -> pd.DataFrame:
   
    group = group.sort_values("timestamp")

    dt = group["timestamp"].diff().dt.total_seconds()
    dx = group["x_hive"].diff()
    dy = group["y_hive"].diff()

    distance = np.sqrt(dx**2 + dy**2)
    group["speed"] = distance / dt

    return group


def summarize_speed(df: pd.DataFrame, method: str = "mean") -> pd.Series:
    
    df_clean = df.replace([np.inf, -np.inf], np.nan).dropna(subset=["speed"])
    if method == "median":
        return df_clean.groupby("bee_id")["speed"].median()
    return df_clean.groupby("bee_id")["speed"].mean()


def plot_speed_distribution(speeds: pd.Series, method: str = "mean", output_file: str = None):
    
    plt.figure(figsize=(12, 7))

    plt.hist(speeds, bins=50, color="red", edgecolor="black", alpha=0.85)

    
    plt.title(f"Distribution of {method.capitalize()} Bee Speeds", fontsize=20, fontweight="bold", pad=20)
    plt.xlabel("Speed (cm/s)", fontsize=18, labelpad=12)
    plt.ylabel("Number of Bees", fontsize=18, labelpad=12)

    
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)

    
    plt.grid(True, linestyle=":", linewidth=0.8, alpha=0.7)

    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(1.2)
    ax.spines['bottom'].set_linewidth(1.2)

    plt.tight_layout()

    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')

    plt.show()


if __name__ == "__main__":
   
    parquet_file = "Hive_A_2024-07-20T03_00_00Z--2024-07-20T09_00_00Z.parquet"

    
    df = load_data(parquet_file)
    df = df.groupby("bee_id", group_keys=False).apply(compute_instantaneous_speed)

    
    mean_speeds = summarize_speed(df, method="mean")

    
    valid_bees = mean_speeds[mean_speeds <= 2].index
    df = df[df["bee_id"].isin(valid_bees)]
    filtered_speeds = mean_speeds.loc[valid_bees]

    print(f"Number of bees after filtering: {len(filtered_speeds)}")


    
    plot_speed_distribution(filtered_speeds, method="mean")
