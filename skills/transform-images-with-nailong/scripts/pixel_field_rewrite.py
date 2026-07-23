#!/usr/bin/env python3
"""Pixel-field rewrite prototype.

This implementation rewrites pixels from an extracted source component into an
adaptive Nailong topology. It does not composite a Nailong PNG.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps
from scipy import ndimage

def auto_components(rgb: np.ndarray) -> list[np.ndarray]:
    r, g, b = rgb[...,0], rgb[...,1], rgb[...,2]
    # Bright warm strokes/stars against blue or dark backgrounds; intentionally
    # conservative so the rest of the image remains frozen.
    mask = ((r > 125) & (g > 95) & (r > b * 1.15) & (g > b * 1.05)).astype(np.uint8)
    mask = ndimage.binary_opening(mask, iterations=1)
    mask = ndimage.binary_closing(mask, iterations=2)
    labels, n = ndimage.label(mask)
    out = []
    for i in range(1, n+1):
        ys, xs = np.where(labels == i)
        if len(xs) >= 20:
            m = labels == i
            out.append(m)
    return sorted(out, key=lambda x: x.sum(), reverse=True)

def crop_mask(mask):
    ys, xs = np.where(mask)
    return mask[ys.min():ys.max()+1, xs.min():xs.max()+1], (xs.min(), ys.min())

def topology_for_component(h, w, compactness):
    """Create a shape from descriptors, not a pasted asset.

    Compact components use a curled body; elongated components use a stretched
    body. Both share generated head/belly/limb/face anchors.
    """
    canvas = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(canvas)
    cx, cy = w/2, h/2
    if compactness < 1.9:
        # Curled body: thick arc, head at one end, tail at the other.
        box = (w*.14, h*.10, w*.86, h*.92)
        d.arc(tuple(map(int, box)), 205, 510, fill=255, width=max(4, int(min(w,h)*.20)))
        hr = max(5, int(min(w,h)*.24))
        d.ellipse((int(cx-hr), int(cy-h*.36-hr), int(cx+hr), int(cy-h*.36+hr)), fill=255)
        # short limbs at the inner bend
        for dx, dy in [(-.22,.25),(.20,.25),(-.13,.52),(.14,.52)]:
            rr = max(3, int(min(w,h)*.09))
            d.ellipse((int(cx+dx*w-rr), int(cy+dy*h-rr), int(cx+dx*w+rr), int(cy+dy*h+rr)), fill=255)
    else:
        body = (int(w*.20), int(h*.27), int(w*.80), int(h*.85))
        d.ellipse(body, fill=255)
        hr = max(5, int(min(w,h)*.24))
        d.ellipse((int(cx-hr), int(h*.05), int(cx+hr), int(h*.05+2*hr)), fill=255)
        for dx, dy in [(-.27,.48),(.27,.48),(-.18,.82),(.18,.82)]:
            rr = max(3, int(min(w,h)*.10))
            d.ellipse((int(cx+dx*w-rr), int(cy+dy*h-rr), int(cx+dx*w+rr), int(cy+dy*h+rr)), fill=255)
    return np.asarray(canvas) > 0

def rewrite_component(base: Image.Image, src_mask: np.ndarray) -> Image.Image:
    arr = np.asarray(base.convert("RGB"), dtype=np.float32)
    ys, xs = np.where(src_mask)
    x0, x1, y0, y1 = xs.min(), xs.max()+1, ys.min(), ys.max()+1
    src = arr[y0:y1, x0:x1]
    h, w = src.shape[:2]
    area = float(src_mask.sum()); perimeter = float(np.count_nonzero(ndimage.binary_dilation(src_mask) ^ src_mask))
    compactness = (perimeter * perimeter) / max(area, 1.0)
    target = topology_for_component(h, w, compactness)
    # Resize source pixels into target field; preserve local luminance/detail,
    # then remap chroma into a warm Nailong palette.
    tex = Image.fromarray(np.uint8(np.clip(src, 0, 255))).resize((w, h), Image.Resampling.BICUBIC)
    tex = np.asarray(tex, dtype=np.float32)
    lum = 0.2126*tex[...,0] + 0.7152*tex[...,1] + 0.0722*tex[...,2]
    lum = (lum - lum.mean()) * 1.12 + 178
    out = np.zeros((h,w,4), dtype=np.uint8)
    out[...,0] = np.clip(lum + 48, 0, 255)
    out[...,1] = np.clip(lum + 8, 0, 255)
    out[...,2] = np.clip(lum - 78, 0, 255)
    out[...,3] = (target*255).astype(np.uint8)
    layer = Image.fromarray(out, "RGBA")
    # Face/belly are generated inside the same pixel field.
    ld = ImageDraw.Draw(layer)
    cx, cy = w//2, h//2
    rr = max(2, int(min(w,h)*.045))
    for ex in (-.16, .16):
        exx = int(cx + ex*w)
        ld.ellipse((exx-rr, int(h*.23)-rr, exx+rr, int(h*.23)+rr), fill=(20,30,20,255))
        ld.ellipse((exx-rr//3, int(h*.23)-rr*2//3, exx+rr//4, int(h*.23)-rr//4), fill=(255,255,255,255))
    ld.ellipse((cx-rr//2, int(h*.34)-rr//2, cx+rr//2, int(h*.34)+rr//2), fill=(55,20,20,255))
    ld.ellipse((int(w*.39), int(h*.55), int(w*.61), int(h*.80)), fill=(250,222,150,215))
    alpha = layer.getchannel("A").filter(ImageFilter.GaussianBlur(1.0))
    layer.putalpha(alpha)
    result = base.convert("RGBA")
    result.alpha_composite(layer, (x0, y0))
    return result.convert("RGB")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--max-components", type=int, default=6)
    args = p.parse_args()
    image = Image.open(args.input).convert("RGB")
    arr = np.asarray(image)
    components = auto_components(arr)[:args.max_components]
    out = image
    for c in components:
        out = rewrite_component(out, c)
    out.save(args.output, quality=95)
    print(f"rewrote {len(components)} components -> {args.output}")

if __name__ == "__main__":
    main()
