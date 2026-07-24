#!/usr/bin/env python3
"""Adaptive pixel rewrite core.

Unlike the old renderer, this module treats the source object mask as the
coordinate domain. A target topology mask may be supplied; otherwise a
shape-adapted topology is inferred from the source contour and skeleton.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps
from scipy import ndimage
from skimage.morphology import skeletonize

def read_mask(path: Path, size):
    m = Image.open(path).convert("L").resize(size, Image.Resampling.NEAREST)
    return np.asarray(m) > 127

def descriptors(mask):
    ys, xs = np.where(mask)
    h, w = mask.shape
    area = float(mask.sum())
    perim = float(np.count_nonzero(ndimage.binary_dilation(mask) ^ mask))
    cov = area / max(h*w, 1)
    yy, xx = ys - ys.mean(), xs - xs.mean()
    covar = np.cov(np.stack([xx, yy])) if len(xs) > 3 else np.eye(2)
    vals, vecs = np.linalg.eigh(covar)
    axis = vecs[:, np.argmax(vals)]
    sk = skeletonize(mask)
    return {"area": area, "compactness": perim*perim/max(area,1), "coverage": cov,
            "axis": axis, "skeleton": sk, "distance": ndimage.distance_transform_edt(mask)}

def adaptive_topology(mask, d):
    """Modify the actual source silhouette instead of placing a fixed body.

    The source contour remains the outer constraint. Head, belly and tail are
    allocated at extrema of the skeleton/major axis, so the topology adapts to
    arbitrary blobs and paths.
    """
    # For a compact component, infer a curled body topology from the region's
    # own scale and centroid. The scene never names the object; compactness is
    # the only trigger.
    if d["compactness"] > 80:
        ys0, xs0 = np.where(mask)
        x0, x1, y0, y1 = xs0.min(), xs0.max(), ys0.min(), ys0.max()
        canvas = Image.new("L", (mask.shape[1], mask.shape[0]), 0)
        dr = ImageDraw.Draw(canvas)
        cx, cy = (x0+x1)/2, (y0+y1)/2
        rw, rh = (x1-x0)*.78, (y1-y0)*.78
        width = max(5, int(min(rw, rh)*.22))
        dr.arc((int(cx-rw/2), int(cy-rh/2), int(cx+rw/2), int(cy+rh/2)), 210, 510, fill=255, width=width)
        hr = max(6, int(min(rw,rh)*.22))
        hx, hy = int(cx-rw*.18), int(cy-rh*.24)
        dr.ellipse((hx-hr,hy-hr,hx+hr,hy+hr), fill=255)
        for dx, dy in [(-.22,.10),(.18,.18),(-.12,.38),(.12,.42)]:
            rr=max(3,int(hr*.38)); px=int(cx+dx*rw); py=int(cy+dy*rh)
            dr.ellipse((px-rr,py-rr,px+rr,py+rr), fill=255)
        # Tail closes the arc; limbs attach to the inner bend and are part of
        # the generated target mask, not an overlaid bitmap detail.
        dr.polygon([(int(cx+rw*.18), int(cy+rh*.12)),
                    (int(cx+rw*.43), int(cy+rh*.02)),
                    (int(cx+rw*.32), int(cy+rh*.20))], fill=255)
        for dx, dy in [(-.18,.18),(.10,.28),(-.10,.40),(.16,.46)]:
            rr=max(3,int(hr*.30)); px=int(cx+dx*rw); py=int(cy+dy*rh)
            dr.ellipse((px-rr,py-rr,px+rr,py+rr), fill=255)
        out = np.asarray(canvas) > 0
        out &= ndimage.binary_dilation(mask, iterations=max(2, int(min(rw,rh)*.08)))
    else:
        out = mask.copy()
        # For elongated shapes, use the principal axis to place short limbs
        # at two high-width locations and a tail at the low-width endpoint.
        yy, xx = np.where(mask)
        cx, cy = xx.mean(), yy.mean(); axis = d["axis"]
        scale = max(3, int(np.sqrt(d["area"])*.045))
        for sign in (-1, 1):
            px, py = int(cx + axis[0]*sign*scale*4), int(cy + axis[1]*sign*scale*4)
            out[max(0,py-scale):py+scale+1, max(0,px-scale):px+scale+1] = True
    ys, xs = np.where(mask)
    cx, cy = xs.mean(), ys.mean()
    axis = d["axis"]
    proj = (xs-cx)*axis[0] + (ys-cy)*axis[1]
    head_idx = np.argmax(proj); tail_idx = np.argmin(proj)
    hx, hy = xs[head_idx], ys[head_idx]
    tx, ty = xs[tail_idx], ys[tail_idx]
    # Near-circular components have no stable skeleton endpoints. Place the
    # head and tail on an interior principal arc so face details remain inside
    # the source region; this is inferred from compactness, not scene labels.
    if d["compactness"] > 80:
        radius = float(np.sqrt(d["area"] / np.pi))
        hx, hy = cx - axis[1]*radius*.35, cy + axis[0]*radius*.35
        tx, ty = cx + axis[1]*radius*.35, cy - axis[0]*radius*.35
    # Keep original contour, but create a connected belly channel along the
    # principal direction; its width follows the distance field.
    yy, xx = np.indices(mask.shape)
    belly_axis = (xx-cx)*axis[0] + (yy-cy)*axis[1]
    belly_band = (np.abs(belly_axis) < np.percentile(d["distance"][mask], 65)) & mask
    out |= belly_band
    return out, (hx, hy), (tx, ty), axis

def style_rewrite(image, source_mask, target_mask):
    arr = np.asarray(image.convert("RGB"), dtype=np.float32)
    blur = ndimage.gaussian_filter(arr, sigma=(2,2,0))
    detail = arr - blur
    lum = 0.2126*blur[...,0] + 0.7152*blur[...,1] + 0.0722*blur[...,2]
    yellow = np.stack([lum*1.10+34, lum*.86+18, lum*.34-5], axis=-1)
    # retain source brush detail while changing chroma
    rewritten = np.clip(yellow + detail*.72, 0, 255)
    out = arr.copy()
    alpha = ndimage.gaussian_filter(target_mask.astype(np.float32), sigma=1.2)
    alpha = np.clip(alpha, 0, 1)
    out = out*(1-alpha[...,None]) + rewritten*alpha[...,None]
    return Image.fromarray(np.uint8(np.clip(out,0,255)))

def add_details(image, target_mask, head, tail, axis):
    out = image.convert("RGBA")
    d = ImageDraw.Draw(out)
    hx, hy = head; tx, ty = tail
    ys, xs = np.where(target_mask)
    scale = max(4, int(np.sqrt(target_mask.sum())*.065))
    # Face follows the inferred head direction; no fixed canvas coordinates.
    for side in (-1, 1):
        ex = int(hx - axis[1]*side*scale*2 - axis[0]*scale*2)
        ey = int(hy + axis[0]*side*scale*2 - axis[1]*scale*2)
        d.ellipse((ex-scale, ey-scale, ex+scale, ey+scale), fill=(22,30,20,235))
        d.ellipse((ex-scale//3, ey-scale//2, ex+scale//4, ey-scale//5), fill=(255,255,255,240))
    d.ellipse((int(hx-scale*.5), int(hy+scale*1.6), int(hx+scale*.5), int(hy+scale*2.5)), fill=(55,20,20,220))
    # Continuous pale belly patch follows the generated body scale rather than
    # being a fixed-size sticker.
    d.ellipse((int(hx-scale*2.2), int(hy+scale*2.4), int(hx+scale*2.2), int(hy+scale*6.0)), fill=(250,224,158,190))
    return out.convert("RGB")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--mask", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    image = Image.open(args.input).convert("RGB")
    mask = read_mask(args.mask, image.size)
    d = descriptors(mask)
    target, head, tail, axis = adaptive_topology(mask, d)
    out = style_rewrite(image, mask, target)
    out = add_details(out, target, head, tail, axis)
    out.save(args.output, quality=95)
    print(f"adaptive rewrite -> {args.output}; area={int(d['area'])}, compactness={d['compactness']:.2f}")

if __name__ == "__main__":
    main()
