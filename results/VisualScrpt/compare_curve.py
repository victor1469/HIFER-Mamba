import pandas as pd
import matplotlib.pyplot as plt

ours = pd.read_csv("psnr_curve_au.csv")

baseline = pd.read_csv(
    "psnr_curve_baseline.csv"
)

plt.figure(figsize=(6,4))

plt.plot(
    baseline["step"],
    baseline["value"],
    label="MambaIRv2",
    linewidth=2
)

plt.plot(
    ours["step"],
    ours["value"],
    label="Ours",
    linewidth=2
)



plt.xlabel("Iteration")

plt.ylabel("PSNR (dB)")

plt.legend()

plt.tight_layout()

plt.savefig(
    "psnr_compare.png",
    dpi=600
)


ours = pd.read_csv("loss_curve_au.csv")

baseline = pd.read_csv(
    "loss_curve_baseline.csv"
)

ours["smooth"] = (
    ours["value"]
    .rolling(30)
    .mean()
)

baseline["smooth"] = (
    baseline["value"]
    .rolling(30)
    .mean()
)

plt.figure(figsize=(6,4))

plt.plot(
    baseline["step"],
    baseline["smooth"],
    label="MambaIRv2",
    linewidth=2
)

plt.plot(
    ours["step"],
    ours["smooth"],
    label="Ours",
    linewidth=2
)

plt.xlabel("Iteration")

plt.ylabel("L1 Loss")

plt.legend()

plt.tight_layout()

plt.savefig(
    "loss_compare.png",
    dpi=600
)




plt.show()