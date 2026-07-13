from tensorboard.backend.event_processing import event_accumulator
import pandas as pd


event_file = "events.out.tfevents.1764377511.master-0.126044.0"



ea = event_accumulator.EventAccumulator(event_file)

ea.Reload()

print("Tags:")
print(ea.Tags()["scalars"])

# 导出loss
loss_events = ea.Scalars("losses/l_pix")

loss_df = pd.DataFrame([
    {
        "step": e.step,
        "value": e.value,
        "wall_time": e.wall_time
    }
    for e in loss_events
])

loss_df.to_csv("loss_curve_au.csv", index=False)

print("loss_curve_au.csv 已保存")

# 导出psnr
psnr_events = ea.Scalars("metrics/Set14/psnr")

psnr_df = pd.DataFrame([
    {
        "step": e.step,
        "value": e.value,
        "wall_time": e.wall_time
    }
    for e in psnr_events
])

psnr_df.to_csv("psnr_curve_au.csv", index=False)

print("psnr_curve_au.csv 已保存")


print(ea.Tags())