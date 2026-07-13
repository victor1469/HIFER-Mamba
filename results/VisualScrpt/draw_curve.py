import pandas as pd
import matplotlib.pyplot as plt

# 读取数据
loss_df = pd.read_csv("loss_curve.csv")
psnr_df = pd.read_csv("psnr_curve.csv")

# -------------------
# Loss Curve
# -------------------
plt.figure(figsize=(6,4))

plt.plot(
    loss_df["step"],
    loss_df["value"],
    linewidth=1
)

plt.xlabel("Iteration")
plt.ylabel("L1 Loss")
plt.title("Training Loss Curve")

plt.tight_layout()
plt.savefig("loss_curve.png", dpi=600)

plt.close()

# -------------------
# PSNR Curve
# -------------------
plt.figure(figsize=(6,4))

plt.plot(
    psnr_df["step"],
    psnr_df["value"],
    linewidth=1.5
)

plt.xlabel("Iteration")
plt.ylabel("PSNR (dB)")
plt.title("Validation PSNR Curve")

plt.tight_layout()
plt.savefig("psnr_curve.png", dpi=600)



loss_df["smooth"] = (
    loss_df["value"]
    .rolling(window=30)
    .mean()
)

plt.figure(figsize=(6,4))

plt.plot(
    loss_df["step"],
    loss_df["smooth"],
    linewidth=1.5
)

plt.xlabel("Iteration")
plt.ylabel("L1 Loss")
plt.title("Training Loss Curve")

plt.tight_layout()
plt.savefig(
    "loss_curve_smooth.png",
    dpi=600
)



plt.close()

print("Done.")