#!/usr/bin/env python3
"""generate_gallery.py - JLP photo delivery: build a PIN-gated client gallery on the VPS.

Usage:
  generate_gallery.py --source <dir> --slug <slug> --couple "First & First"
      --date "Month DD, YYYY" --pin NNNN [--session-type wedding] [--no-zip]

Flow: source photos -> EXIF screen (GPS is a hard fail) -> previews (2000px q85,
EXIF-stripped) -> zip of previews -> gallery page (from gallery_template.html)
-> manifest.json. Gallery bytes live on the VPS under
/root/projects/sites/jlp-deliveries/<slug>/ and NEVER go into the public git
repo. Public exposure is path-scoped Tailscale Funnel.
"""
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent / "gallery_template.html"
DELIVERIES = Path("/root/projects/sites/jlp-deliveries")
PUBLIC_URL = "https://vmi3233088.tail66a84c.ts.net/jenna-photos"
PUBLIC_HOST = "vmi3233088.tail66a84c.ts.net"

IMG_EXTS = {".jpeg", ".jpg", ".png", ".webp", ".heic", ".heif"}
MAX_EDGE = 2600
THUMB_EDGE = 800
MEDIUM_EDGE = 1650  # grid srcset tier: covers 3x-DPR phones (needs ~1050-1260px)
JPEG_Q = 85

GPS_KEYS = ("gpslatitude", "gpslatitudeRef", "gpslongitude", "gpslongitudeRef",
            "gpsdatetime", "gpsdatestamp", "gpsposition", "gpsversionid")


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def esc(s):
    """HTML-escape &, <, >, quote for attribute/element text insertion."""
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))


def slug_ok(slug):
    return bool(slug) and bool(__import__("re").fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", slug))


def exif_json(path):
    r = run(["exiftool", "-j", "-G", str(path)])
    if r.returncode != 0 or not r.stdout.strip():
        return {}
    try:
        return json.loads(r.stdout.strip())[0]
    except Exception:
        return {}


def gps_tags(exif):
    out = {}
    for k, v in exif.items():
        kl = k.lower()
        if any(g in kl for g in ("gpslatitude", "gpslongitude", "gpsposition",
                                 "gpsdatetime", "gpsdatestamp", "gpsversionid")):
            out[k] = v
    return out


def pii_tags(exif):
    out = {}
    for k, v in exif.items():
        kl = k.lower()
        if kl.endswith(("artist", "by-line", "by-linetitle", "copyright",
                        "credit", "ownername", "description", "comment",
                        "usercomment")) and v:
            out[k] = v
    return out


def probe_sources(src_dir):
    """Return (ok, list-of-(path, problems-dict)). GPS aborts; PII warns."""
    files = sorted(p for p in src_dir.rglob("*")
                   if p.is_file() and p.suffix.lower() in IMG_EXTS
                   and not p.name.startswith("."))
    if not files:
        return False, [("NONE", {"error": "no image files found in source"})]
    screened = []
    for p in files:
        exif = exif_json(p)
        problems = {}
        gps = gps_tags(exif)
        if gps:
            problems["GPS"] = gps  # hard fail
        pii = pii_tags(exif)
        if pii:
            problems["PII"] = pii  # warning only
        screened.append((p, problems))
    ok = not any("GPS" in pr for _, pr in screened)
    return ok, screened


def make_preview(src, dst, max_edge=MAX_EDGE):
    from PIL import Image, ImageOps
    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im)
        im = im.convert("RGB")
        w, h = im.size
        scale = max_edge / max(w, h)
        if scale < 1:
            im = im.resize((round(w * scale), round(h * scale)), Image.LANCZOS)
        im.save(dst, "JPEG", quality=JPEG_Q, optimize=True)


def photo_dimensions(path):
    from PIL import Image
    with Image.open(path) as im:
        return im.size


AVIF_ENC = "/root/.hermes/tools/ffmpeg-9.0.1-linux-x64/bin/ffmpeg"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    ap.add_argument("--slug", required=True)
    ap.add_argument("--couple", required=True)
    ap.add_argument("--title", default=None,
                    help="Gallery display title, e.g. 'Jossalyn Grad Session' (defaults to --couple)")
    ap.add_argument("--date", required=True)
    ap.add_argument("--pin", required=True)
    ap.add_argument("--session-type", default="wedding")
    ap.add_argument("--no-zip", action="store_true")
    ap.add_argument("--yes", action="store_true", help="skip confirmation prompt")
    args = ap.parse_args()

    src = Path(args.source).expanduser().resolve()
    if not src.is_dir():
        sys.exit(f"source dir not found: {src}")
    slug = args.slug.strip().lower()
    if not slug_ok(slug):
        sys.exit("slug must be lowercase letters/digits separated by single hyphens")
    pin = args.pin.strip()
    if not pin.isdigit() or not (4 <= len(pin) <= 8):
        sys.exit("PIN must be 4-8 digits")
    couple = args.couple.strip()
    firstnames = " & ".join(p.strip() for p in couple.split("&"))
    gallery_title = (args.title or couple).strip()

    # 1. EXIF screen
    ok, screened = probe_sources(src)
    gps_files = [str(p) for p, pr in screened if "GPS" in pr]
    pii_files = [str(p) for p, pr in screened if "PII" in pr]
    if gps_files:
        print("ABORT: GPS metadata present in:")
        for f in gps_files:
            print("  ", f)
        sys.exit(2)
    if pii_files:
        print(f"note: {len(pii_files)} file(s) carry Artist/Copyright/Description "
              f"metadata (photographer copyright is fine; will be stripped in previews)")

    out = DELIVERIES / slug
    previews = out / "photos"
    mediums = out / "photos-md"
    thumbs = out / "thumbs"
    if out.exists():
        if not args.yes:
            ans = input(f"'{out}' exists. Rebuild? [y/N] ")
            if ans.strip().lower() != "y":
                sys.exit("aborted")
        shutil.rmtree(out)
    previews.mkdir(parents=True, exist_ok=True)
    mediums.mkdir(parents=True, exist_ok=True)
    thumbs.mkdir(parents=True, exist_ok=True)

    # 2. previews + thumbs (PIL re-encode drops ALL metadata incl. GPS by construction)
    photos = []
    for i, (p, pr) in enumerate(screened, 1):
        dst = previews / f"{slug}-{i:02d}.jpg"
        make_preview(p, dst)
        mdst = mediums / f"{slug}-{i:02d}.jpg"
        make_preview(p, mdst, max_edge=MEDIUM_EDGE)
        tdst = thumbs / f"{slug}-{i:02d}.jpg"
        make_preview(p, tdst, max_edge=THUMB_EDGE)
        w, h = photo_dimensions(dst)
        label = f"{args.session_type.capitalize()} photo {i}"
        photos.append({
            "file": dst.name, "thumb": f"thumbs/{tdst.name}",
            "medium": f"photos-md/{mdst.name}", "label": label,
            "orig": p.name,
            "w": w, "h": h,
            "src_name": p.name, "src_bytes": p.stat().st_size,
            "preview_bytes": dst.stat().st_size,
            "had_pii": "PII" in pr,
        })
        print(f"  [{i}/{len(screened)}] {p.name} -> {dst.name} ({w}x{h})")

    # 2b. modern-format variants (AVIF > WebP > JPEG <picture> chain; Matt 2026-09-25):
    #     previews only — the zip stays full-res EXIF-stripped JPEG by design.
    import concurrent.futures
    from PIL import Image
    def _encode_variants(ph):
        stem = Path(ph["thumb"]).name[:-4]  # strip .jpg
        # idempotent: skip re-encoding when all four variants already exist
        if all((thumbs / f"{stem}.{ext}").exists() for ext in ("avif", "webp")) and \
           all((mediums / f"{stem}.{ext}").exists() for ext in ("avif", "webp")):
            ph = dict(ph)
            ph["thumb_avif"] = f"thumbs/{stem}.avif"
            ph["thumb_webp"] = f"thumbs/{stem}.webp"
            ph["medium_avif"] = f"photos-md/{stem}.avif"
            ph["medium_webp"] = f"photos-md/{stem}.webp"
            return ph
        avif_t = thumbs / f"{stem}.avif"
        webp_t = thumbs / f"{stem}.webp"
        avif_m = mediums / f"{stem}.avif"
        webp_m = mediums / f"{stem}.webp"
        try:
            # thumbs: Pillow WebP (fast) + ffmpeg AVIF (qp 68 measured -50-75%)
            with Image.open(thumbs / f"{stem}.jpg") as im:
                im.save(webp_t, "WEBP", quality=80, method=4)
            r = subprocess.run([AVIF_ENC, "-y", "-loglevel", "error",
                                "-i", str(thumbs / f"{stem}.jpg"),
                                "-c:v", "libaom-av1", "-still-picture", "1",
                                "-qp", "68", "-pix_fmt", "yuv420p", str(avif_t)],
                               capture_output=True, text=True, timeout=120)
            if r.returncode != 0 or not avif_t.exists():
                return None
            # md: WebP via Pillow, AVIF via ffmpeg (qp 68)
            with Image.open(mediums / f"{stem}.jpg") as im:
                im.save(webp_m, "WEBP", quality=82, method=4)
            r2 = subprocess.run([AVIF_ENC, "-y", "-loglevel", "error",
                                 "-i", str(mediums / f"{stem}.jpg"),
                                 "-c:v", "libaom-av1", "-still-picture", "1",
                                 "-qp", "68", "-pix_fmt", "yuv420p", str(avif_m)],
                                capture_output=True, text=True, timeout=300)
            if r2.returncode != 0 or not avif_m.exists():
                return None
        except Exception:
            return None
        ph = dict(ph)
        ph["thumb_avif"] = f"thumbs/{avif_t.name}"
        ph["thumb_webp"] = f"thumbs/{webp_t.name}"
        ph["medium_avif"] = f"photos-md/{avif_m.name}"
        ph["medium_webp"] = f"photos-md/{webp_m.name}"
        return ph
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        encoded = list(pool.map(_encode_variants, photos))
    if all(e is not None for e in encoded) and len(encoded) == len(photos):
        photos = encoded
        print(f"  modern formats: AVIF+WebP emitted for {len(photos)} photos (thumbs+md)")
    else:
        print("  note: some AVIF/WebP encodes failed; falling back to JPEG-only manifest")

    # 3. zip of FULL-RESOLUTION originals, EXIF-stripped losslessly
    #    (clients pay for full-res delivery; on-screen previews stay 2000px
    #    for fast browsing — Pixieset-style split)
    zip_name = None
    if not args.no_zip:
        zip_name = f"{slug}-photos.zip"
        zpath = out / zip_name
        staging = out / ".zip-stage"
        if staging.exists():
            shutil.rmtree(staging)
        staging.mkdir()
        with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
            for ph in photos:
                src_file = src / ph["orig"]
                staged = staging / ph["file"]
                shutil.copy2(src_file, staged)
                # strip ALL metadata losslessly (JPEG untouched, no re-encode)
                r = subprocess.run(["exiftool", "-overwrite_original", "-all=", str(staged)],
                                   capture_output=True, text=True)
                if r.returncode != 0:
                    raise SystemExit(f"exiftool failed on {src_file}: {r.stderr[:200]}")
                z.write(staged, ph["file"])
        shutil.rmtree(staging)
        print(f"  zip: {zip_name} ({zpath.stat().st_size / 1e6:.1f} MB) — full-res, EXIF-stripped")

    # 3b. cover pick: prefer a portrait-orientation photo (likely head-and-
    #     shoulders) so the split hero shows the person, not the scenery
    def _cover_pick(cands):
        for ph in cands:
            if ph["h"] > ph["w"]:
                return ph
        return cands[0] if cands else None

    cover_ph = _cover_pick(photos)

    # 4. gallery page from template (token substitution; HTML-escape text)
    tpl = TEMPLATE.read_text()
    def _photo_entry(ph):
        # v4.4-M: [full, alt, thumb, medium, w, h] (6-element, dims for masonry)
        # v4.4-M.2: + [thumb_avif, thumb_webp, medium_avif, medium_webp] at [6..9]
        # when modern formats were emitted (10-element). Template guards by length.
        e = [f"photos/{ph['file']}", ph["label"], f"thumbs/{Path(ph['thumb']).name}",
             f"photos-md/{Path(ph['medium']).name}", ph["w"], ph["h"]]
        if "thumb_avif" in ph:
            e += [ph["thumb_avif"], ph["thumb_webp"], ph["medium_avif"], ph["medium_webp"]]
        return e
    photos_json = json.dumps([_photo_entry(ph) for ph in photos])
    # 4-element legacy entries remain valid input (template probe fallback).
    # per-photo srcset with TRUE pixel widths (portrait vs landscape differ);
    # JSON layout: [preview, label, thumb, medium, srcset]
    def _w_at(edge, w, h):
        return w if max(w, h) <= edge else round(w * edge / max(w, h))
    srcset_map = {}
    srcset_avif = {}
    srcset_webp = {}
    for ph in photos:
        tw = _w_at(THUMB_EDGE, ph["w"], ph["h"])
        mw = _w_at(MEDIUM_EDGE, ph["w"], ph["h"])
        srcset_map[f"thumbs/{Path(ph['thumb']).name}"] = \
            f"thumbs/{Path(ph['thumb']).name} {tw}w, photos-md/{Path(ph['medium']).name} {mw}w, photos/{ph['file']} {ph['w']}w"
        if "thumb_avif" in ph:
            ta = Path(ph["thumb_avif"]).name
            ma = Path(ph["medium_avif"]).name
            twa = _w_at(THUMB_EDGE, ph["w"], ph["h"])
            mwa = _w_at(MEDIUM_EDGE, ph["w"], ph["h"])
            srcset_avif[f"thumbs/{ta}"] = f"thumbs/{ta} {twa}w, photos-md/{ma} {mwa}w"
            twp = Path(ph["thumb_webp"]).name
            mwp = Path(ph["medium_webp"]).name
            srcset_webp[f"thumbs/{twp}"] = f"thumbs/{twp} {tw}w, photos-md/{mwp} {mw}w"
    subs = {
        "__COUPLE__": esc(gallery_title),
        "__COUPLE_HTML__": esc(gallery_title),
        "__FIRSTNAMES__": esc(firstnames),
        "__FIRSTNAMES_HTML__": esc(firstnames),
        "__DATE__": esc(args.date),
        "__COUNT__": str(len(photos)),
        "__PIN__": pin,
        "__ZIP__": zip_name or "",
        "__SLUG__": slug,
        "__PHOTOS_JSON__": photos_json,
        "__SRCSET_JSON__": json.dumps(srcset_map),
        "__SRCSET_AVIF_JSON__": json.dumps(srcset_avif),
        "__SRCSET_WEBP_JSON__": json.dumps(srcset_webp),
        "__COVER__": f"photos/{cover_ph['file']}" if cover_ph else "",
        "__COVER_ALT__": esc(f"{couple} — {args.session_type} photograph by Jenna Lynn Photography"),
        "__COVER_POS__": "50%",  # neutral center (v4: faces clear on wide boxes; per-photo override via --cover-pos later)
        "__SESSION_LABEL__": esc(args.session_type.capitalize()),
        "__SESSION_LABEL_LOW__": esc(args.session_type.lower()),
        "__GENERATED__": subprocess.run(["date", "+%Y-%m-%d %H:%M"],
                                        capture_output=True, text=True).stdout.strip(),
    }
    for k, v in subs.items():
        tpl = tpl.replace(k, v)
    (out / "index.html").write_text(tpl)

    # 5. manifest
    manifest = {
        "slug": slug, "couple": couple, "title": gallery_title, "firstnames": firstnames,
        "date": args.date, "session_type": args.session_type,
        "count": len(photos),
        "zip": zip_name,
        "public_url": f"{PUBLIC_URL}/{slug}/",
        "local_path": str(out),
        "generated": subs["__GENERATED__"],
        "source_dir": str(src),
        "photos": photos,
        "sha256_index": hashlib.sha256((out / "index.html").read_bytes()).hexdigest(),
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2))
    print(f"\nDONE: {out}")
    print(f"  public URL : {manifest['public_url']}")
    print(f"  PIN        : {pin}  (share with Jenna, never in the public repo)")
    if pii_files:
        print(f"  note: {len(pii_files)} source file(s) had PII-ish metadata; "
              f"previews and zip are stripped by re-encode.")

    # 6. branded redirect page on the public site domain
    #    (galleries/<slug>/index.html — meta-refresh + JS + manual link fallback)
    redirect_tpl = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__ — Your Gallery | Jenna Lynn Photography</title>
<meta name="robots" content="noindex, nofollow">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 110 110'><text x='50%' y='55%' dominant-baseline='middle' text-anchor='middle' font-size='80'>📸</text></svg>">
<meta http-equiv="refresh" content="0;url=__PUBLIC_URL__">
<style>
body{margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center;
  font-family:'Montserrat',sans-serif;background:#fdf2f4;color:#2c2c2c;text-align:center;padding:24px}
.card{max-width:420px}
.names{font-family:'Cormorant Garamond',serif;font-size:2.2rem;font-weight:500;margin:0 0 8px}
.sub{font-size:14px;color:#6e6961;margin:0 0 24px}
.link{display:inline-block;padding:14px 32px;border-radius:4px;background:#a85a70;color:#fff;
  text-decoration:none;font-size:14px;font-weight:600}
.small{margin-top:18px;font-size:12px;color:#6e6961}
</style>
</head>
<body>
<div class="card">
  <p class="names">__COUPLE__</p>
  <p class="sub">Taking you to your gallery…</p>
  <a class="link" href="__PUBLIC_URL__">Open your gallery</a>
  <p class="small">If nothing happens, tap the button above.</p>
</div>
<script>location.replace("__PUBLIC_URL__");</script>
</body>
</html>"""
    gdir = Path("/root/repos/jenna-lynn-photography/galleries") / slug
    gdir.mkdir(parents=True, exist_ok=True)
    redirect_html = (redirect_tpl
                     .replace("__COUPLE__", esc(couple))
                     .replace("__TITLE__", esc(gallery_title))
                     .replace("__PUBLIC_URL__", manifest["public_url"]))
    (gdir / "index.html").write_text(redirect_html)
    print(f"  brand link : https://photographybyjennalynn.com/galleries/{slug}/  (redirect)")


if __name__ == "__main__":
    main()