#!/usr/bin/env python3
"""Model-free, style-preserving Nailong raster renderer.

The renderer creates a Nailong topology mask procedurally, samples the source
image's local colour/texture field, and blends only inside the requested mask.
It never uses a transparent Nailong PNG as the final texture.
"""
from __future__ import annotations
import argparse, json, math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageEnhance, ImageOps

def rotated_layer(size, w, h, angle, source):
    layer = Image.new("RGBA", (max(4, int(w*2.5)), max(4, int(h*2.5))), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cx, cy = layer.width//2, layer.height//2
    sx, sy = w/2, h/2
    # Continuous body/head silhouette with explicit limbs and tail.
    d.ellipse((cx-sx*.72, cy-sy*.22, cx+sx*.72, cy+sy*.78), fill=(255,255,255,255))
    d.ellipse((cx-sx*.58, cy-sy*.82, cx+sx*.58, cy+sy*.08), fill=(255,255,255,255))
    d.ellipse((cx-sx*.34, cy-sy*.02, cx+sx*.34, cy+sy*.48), fill=(220,220,220,255))
    limb_w, limb_h = max(3, int(sx*.24)), max(4, int(sy*.38))
    for x, y, a in [(-.65,.28,-28),(.65,.28,28),(-.46,.72,14),(.46,.72,-14)]:
        limb = Image.new("RGBA", (limb_w*3, limb_h*3), (0,0,0,0))
        ImageDraw.Draw(limb).ellipse((limb_w, limb_h//2, limb_w*2, limb_h*2), fill=(255,255,255,255))
        limb = limb.rotate(a, resample=Image.Resampling.BICUBIC, expand=True)
        layer.alpha_composite(limb, (int(cx+x*sx-limb.width/2), int(cy+y*sy-limb.height/2)))
    tail = [(cx+sx*.52, cy+sy*.55), (cx+sx*.98, cy+sy*.35), (cx+sx*.83, cy+sy*.72), (cx+sx*.48, cy+sy*.75)]
    d.polygon(tail, fill=(255,255,255,255))
    # Face anchors; these survive texture transfer.
    for ex in (-.23, .23):
        d.ellipse((cx+ex*sx*.9-sx*.09, cy-sy*.52, cx+ex*sx*.9+sx*.09, cy-sy*.34), fill=(20,35,25,255))
        d.ellipse((cx+ex*sx*.9-sx*.03, cy-sy*.49, cx+ex*sx*.9+sx*.02, cy-sy*.43), fill=(255,255,255,255))
    d.ellipse((cx-sx*.035, cy-sy*.28, cx+sx*.035, cy-sy*.20), fill=(35,20,20,255))
    return layer.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)

def fit_texture(image, center, box):
    x, y = center; w, h = box
    r = int(max(w, h)*.75)
    left, top = max(0, x-r), max(0, y-r)
    right, bottom = min(image.width, x+r), min(image.height, y+r)
    patch = image.crop((left, top, right, bottom)).resize((w, h), Image.Resampling.BICUBIC)
    # Preserve local value structure while gently warming the new character.
    # A restrained warm tint makes the new topology read as Nailong while
    # retaining the source's brush marks and luminance structure.
    # Transfer luminance/brush rhythm, then colourize that field into a
    # Nailong palette. This avoids a grey photographic cut-out.
    lum = ImageOps.grayscale(patch)
    patch = ImageOps.colorize(lum, black=(133, 73, 22), mid=(235, 157, 48), white=(255, 224, 116)).convert("RGBA")
    patch = ImageEnhance.Contrast(patch).enhance(1.08)
    return patch.convert("RGBA")

def render(input_path: Path, output_path: Path, objects: list[dict]):
    base = Image.open(input_path).convert("RGB")
    out = base.convert("RGBA")
    for obj in objects:
        x, y = int(obj["x"]), int(obj["y"])
        w, h = int(obj["width"]), int(obj["height"])
        angle = float(obj.get("angle", 0))
        shape = rotated_layer(base.size, w, h, angle, base)
        sx, sy = x-shape.width//2, y-shape.height//2
        # Build texture exactly in the shape's local frame.
        tex = fit_texture(base, (x, y), (shape.width, shape.height))
        alpha = shape.getchannel("A").filter(ImageFilter.GaussianBlur(1.2))
        tex.putalpha(alpha)
        # Preserve source lighting around the edge via local texture blend.
        out.alpha_composite(tex, (sx, sy))
        # Re-apply topology anchors after texture transfer; otherwise the
        # source brush field would erase the eyes, belly and mouth.
        draw = ImageDraw.Draw(out)
        face_y = int(y - h * .26)
        for ex in (-.20, .20):
            exx = int(x + ex*w)
            draw.ellipse((exx-int(w*.065), face_y-int(h*.09), exx+int(w*.065), face_y+int(h*.03)), fill=(24,35,25,255))
            draw.ellipse((exx-int(w*.022), face_y-int(h*.065), exx+int(w*.015), face_y-int(h*.028)), fill=(255,255,255,255))
        draw.ellipse((x-int(w*.025), int(y-h*.12), x+int(w*.025), int(y-h*.04)), fill=(45,20,20,255))
        belly = (x-int(w*.20), y-int(h*.02), x+int(w*.20), y+int(h*.30))
        draw.ellipse(belly, fill=(249,224,154,210))
    out.convert("RGB").save(output_path, quality=95)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--objects", type=Path, required=True, help="JSON array: x,y,width,height,angle")
    args = p.parse_args()
    render(args.input, args.output, json.loads(args.objects.read_text()))
    print(args.output)

if __name__ == "__main__":
    main()
