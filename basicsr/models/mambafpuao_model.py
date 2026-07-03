import torch
from torch.nn import functional as F
from basicsr.utils.registry import MODEL_REGISTRY
from basicsr.models.sr_model import SRModel



@MODEL_REGISTRY.register()
class MambafpuaoModel(SRModel):
    """Mambafpuao backbone wrapped as a BasicSR SRModel."""

    def init_net(self, net_opt):
        """Initialize the Mambafpuao network."""
        self.net_g = Mambafpuao(
            img_size=net_opt.get('img_size', 64),
            embed_dim=net_opt.get('embed_dim', 48),
            d_state=net_opt.get('d_state', 8),
            depths=net_opt.get('depths', [5, 5, 5, 5]),
            num_heads=net_opt.get('num_heads', [4, 4, 4, 4]),
            window_size=net_opt.get('window_size', 16),
            inner_rank=net_opt.get('inner_rank', 32),
            num_tokens=net_opt.get('num_tokens', 64),
            convffn_kernel_size=net_opt.get('convffn_kernel_size', 5),
            mlp_ratio=net_opt.get('mlp_ratio', 1.0),
            upscale=net_opt.get('scale', 2),
            upsampler=net_opt.get('upsampler', 'pixelshuffledirect')
        ).cuda()

        # EMA model
        if net_opt.get('ema', False):
            self.net_g_ema = Mambafpuao(
                img_size=net_opt.get('img_size', 64),
                embed_dim=net_opt.get('embed_dim', 48),
                d_state=net_opt.get('d_state', 8),
                depths=net_opt.get('depths', [5, 5, 5, 5]),
                num_heads=net_opt.get('num_heads', [4, 4, 4, 4]),
                window_size=net_opt.get('window_size', 16),
                inner_rank=net_opt.get('inner_rank', 32),
                num_tokens=net_opt.get('num_tokens', 64),
                convffn_kernel_size=net_opt.get('convffn_kernel_size', 5),
                mlp_ratio=net_opt.get('mlp_ratio', 1.0),
                upscale=net_opt.get('scale', 2),
                upsampler=net_opt.get('upsampler', 'pixelshuffledirect')
            ).cuda()
            self.net_g_ema.load_state_dict(self.net_g.state_dict())

    def test(self):
        """Tile-based inference for large images, same logic as mambairv2_model.py"""
        #1117------
        if not hasattr(self, 'is_training') or not self.is_training:
            net = self.net_g_ema if hasattr(self, 'net_g_ema') else self.net_g
            net.eval()
            with torch.no_grad():
                self.output = net(self.lq)
            return self.output
        #-----1117
        _, C, h, w = self.lq.size()
        split_token_h = h // 200 + 1
        split_token_w = w // 200 + 1

        # padding
        mod_pad_h = (split_token_h - h % split_token_h) if h % split_token_h != 0 else 0
        mod_pad_w = (split_token_w - w % split_token_w) if w % split_token_w != 0 else 0
        img = F.pad(self.lq, (0, mod_pad_w, 0, mod_pad_h), 'reflect')
        _, _, H, W = img.size()

        split_h = H // split_token_h
        split_w = W // split_token_w
        shave_h = split_h // 10
        shave_w = split_w // 10
        scale = getattr(self.net_g, 'upscale', 1)

        # compute slices
        slices = []
        for i in range(split_token_h):
            for j in range(split_token_w):
                top = slice(max(i*split_h - shave_h, 0), min((i+1)*split_h + shave_h, H))
                left = slice(max(j*split_w - shave_w, 0), min((j+1)*split_w + shave_w, W))
                slices.append((top, left))

        # inference
        outputs = []
        net = self.net_g_ema if hasattr(self, 'net_g_ema') else self.net_g
        net.eval()
        with torch.no_grad():
            for top, left in slices:
                outputs.append(net(img[..., top, left]))

        # merge tiles
        _img = torch.zeros(self.lq.size(0), C, H*scale, W*scale, device=self.lq.device)
        idx = 0
        for i in range(split_token_h):
            for j in range(split_token_w):
                top, left = slices[idx]
                #1113------
                out_patch = outputs[idx]

                # 确保输出维度是 (B, C, H, W)
                if out_patch.dim() == 3:
                    out_patch = out_patch.unsqueeze(0)

                # 边界对齐：防止越界 mismatch
                tgt_H = min(out_patch.shape[2], _img.shape[2] - top.start*scale)
                tgt_W = min(out_patch.shape[3], _img.shape[3] - left.start*scale)

                _img[..., top.start*scale:top.start*scale+tgt_H,
                      left.start*scale:left.start*scale+tgt_W] = out_patch[..., :tgt_H, :tgt_W]
                #-----1113 up code translate to next one sentence 
#                 _img[..., top.start*scale:top.stop*scale, left.start*scale:left.stop*scale] = outputs[idx]
                idx += 1

        # remove padding
        self.output = _img[..., :h*scale, :w*scale]

        # restore net to train mode if no EMA
        if not hasattr(self, 'net_g_ema'):
            self.net_g.train()
        return self.output
