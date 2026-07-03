import os
import sys
import torch

# Add project root to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(project_root)

from basicsr.archs.mambaipfn_arch import MambaIpfn
from analysis.utils_fvcore import FLOPs

if __name__ == '__main__':
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Image size and scale factor
    H, W = 720, 1280
    scale = 4

    # Initialize model
    model = MambaIpfn(
        upscale=scale,
        in_chans=3,
        img_size=H // scale,
        embed_dim=64
    ).to(device)

    # Compute FLOPs and Params
    with torch.no_grad():
        FLOPs.fvcore_flop_count(model, input_shape=(3, H // scale, W // scale))
