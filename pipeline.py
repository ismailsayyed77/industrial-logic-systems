"""
Industrial Motor Data Pipeline
================================
Reads motor sensor data, cleans anomalies, and generates
statistical trend models with visualization.

Author: Maaz
Project: Industrial Logic & Systems Analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
import os

# ─── CONFIG ────────────────────────────────────────────────
DATA_FILE = "data/motor_data.csv"
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ─── STEP 1: GENERATE DATASET ──────────────────────────────
def generate_dataset(n=500):
    """Simulate realistic industrial motor sensor data."""
    np.random.seed(42)
    data = pd.DataFrame({
        'time': pd.date_range('2024-01-01', periods=n, freq='1min'),
        'voltage':     np.random.normal(415, 10, n),
        'current':     np.random.normal(20, 2, n),
        'temperature': np.cumsum(np.random.randn(n) * 0.3) + 60,
        'rpm':         np.random.normal(1450, 30, n),
        'power_kw':    np.random.normal(11.5, 0.8, n)
    })

    # Inject some anomalies to make cleaning realistic
    data.loc[50:55, 'voltage'] = 0       # Power dip
    data.loc[200, 'current']   = 999     # Sensor spike
    data.loc[350, 'temperature'] = np.nan  # Missing reading

    os.makedirs("data", exist_ok=True)
    data.to_csv(DATA_FILE, index=False)
    print(f"[✓] Dataset generated → {DATA_FILE}  ({n} rows)")
    return data


# ─── STEP 2: CLEAN DATA ────────────────────────────────────
def clean_data(df):
    """Remove anomalies and invalid sensor readings."""
    raw_count = len(df)

    df = df.dropna()
    df = df[df['voltage'].between(300, 450)]
    df = df[df['current'].between(0, 50)]
    df = df[df['temperature'].between(20, 120)]
    df = df[df['rpm'].between(1000, 1800)]
    df = df.reset_index(drop=True)

    removed = raw_count - len(df)
    print(f"[✓] Cleaned data  →  {removed} anomalous rows removed  |  {len(df)} rows kept")
    return df


# ─── STEP 3: TREND ANALYSIS ────────────────────────────────
def trend_analysis(df):
    """Run linear regression on temperature to detect rising trend."""
    x = np.arange(len(df))
    slope, intercept, r, p, _ = linregress(x, df['temperature'])

    print(f"\n── Trend Analysis Results ──────────────────────")
    print(f"  Temperature slope : {slope:.5f} °C/min")
    print(f"  R² value          : {r**2:.4f}")
    print(f"  p-value           : {p:.6f}")
    if slope > 0.001:
        print("  ⚠️  WARNING: Rising temperature trend detected!")
    else:
        print("  ✅  Temperature is STABLE")
    print(f"────────────────────────────────────────────────\n")

    return slope, intercept, r**2


# ─── STEP 4: VISUALIZE ─────────────────────────────────────
def plot_dashboard(df, slope, intercept, r2):
    """Generate 4-panel monitoring dashboard."""
    x = np.arange(len(df))
    fig, axes = plt.subplots(2, 2, figsize=(14, 8))
    fig.suptitle("Industrial Motor Monitoring Dashboard", fontsize=15, fontweight='bold')

    # Temperature trend
    axes[0, 0].plot(df['time'], df['temperature'], alpha=0.6, color='tomato', label='Temperature')
    axes[0, 0].plot(df['time'], intercept + slope * x, 'r--', linewidth=2,
                    label=f'Trend (R²={r2:.3f})')
    axes[0, 0].set_title("Temperature Trend Analysis")
    axes[0, 0].set_ylabel("°C")
    axes[0, 0].legend()
    axes[0, 0].grid(alpha=0.3)

    # Voltage
    axes[0, 1].plot(df['time'], df['voltage'], color='steelblue', alpha=0.7)
    axes[0, 1].axhline(415, color='green', linestyle='--', label='Nominal 415V')
    axes[0, 1].set_title("Supply Voltage")
    axes[0, 1].set_ylabel("Volts (V)")
    axes[0, 1].legend()
    axes[0, 1].grid(alpha=0.3)

    # Current
    axes[1, 0].plot(df['time'], df['current'], color='darkorange', alpha=0.7)
    axes[1, 0].set_title("Current Draw")
    axes[1, 0].set_ylabel("Amperes (A)")
    axes[1, 0].grid(alpha=0.3)

    # RPM
    axes[1, 1].plot(df['time'], df['rpm'], color='mediumseagreen', alpha=0.7)
    axes[1, 1].axhline(1450, color='red', linestyle='--', label='Rated 1450 RPM')
    axes[1, 1].set_title("Motor Speed (RPM)")
    axes[1, 1].set_ylabel("RPM")
    axes[1, 1].legend()
    axes[1, 1].grid(alpha=0.3)

    plt.tight_layout()
    path = f"{OUTPUT_DIR}/motor_dashboard.png"
    plt.savefig(path, dpi=150)
    print(f"[✓] Dashboard saved → {path}")
    plt.show()


# ─── MAIN ──────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("  Industrial Motor Data Pipeline")
    print("=" * 50)

    raw_df   = generate_dataset()
    clean_df = clean_data(raw_df)
    slope, intercept, r2 = trend_analysis(clean_df)
    plot_dashboard(clean_df, slope, intercept, r2)

    print("\n[✓] Pipeline complete!")
