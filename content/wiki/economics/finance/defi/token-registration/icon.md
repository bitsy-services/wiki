---
title: "Making the Icon"
weight: 10
---

A token icon is displayed at 20 to 24 pixels in a wallet balance row, which is the size at which it does its actual work. Everything else — the 256-pixel version in the repository, the 512-pixel version on the project page — is a downscale target. Design for the 20-pixel render, then produce the seven files the registrars ask for from one vector source.

## Constraints that come from the render size

- **One mark, no wordmark.** The symbol is already printed next to the icon in every interface that shows it. Lettering inside a 20-pixel square is four or five pixels tall and resolves to a smear.
- **Stroke weight at or above 6% of the canvas.** A 256-pixel canvas wants strokes of 16 pixels or more; below that, the 20-pixel downscale drops them to under one pixel and the antialiaser turns them into grey haze.
- **Two colors, high contrast.** Gradients average out at small sizes, so a gradient icon renders as its mean color and stops being distinguishable from every other icon whose mean is a similar blue.
- **Give the mark its own disc.** Surfaces disagree about their background: Etherscan is light, most wallets default to dark, and a transparent icon that is pure black or pure white vanishes on one of them. A filled circle behind the mark makes the icon background-independent and also survives the circular cropping several wallets apply.
- **Keep the mark inside 88% of the canvas.** Interfaces that crop to a circle cut the corners off a square icon.

## The source file

Author in SVG and rasterize from it. A hand-drawn 256-pixel bitmap cannot produce a clean 32-pixel version, but the reverse works every time.

Keep the authored file separate from the exported one — the flattening step below is lossy and irreversible, so name the source `logo.src.svg`.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256">
  <!-- Own disc: legible against light and dark chrome, survives circular crop. -->
  <circle cx="128" cy="128" r="128" fill="#1c1f2b"/>
  <!-- 18px strokes on a 256px canvas = 7%, so ~1.4px at the 20px render. -->
  <g fill="none" stroke="#5ad1a4" stroke-width="18" stroke-linecap="round">
    <path d="M78 168 V104 a50 50 0 0 1 100 0 v64"/>
    <path d="M78 136 H178"/>
  </g>
</svg>
```

Two things must be true of the file before it goes anywhere. Text has to be converted to paths, because the renderer on the other end does not have your font and will substitute or drop it. And it must not reference anything external — no `<image>` href, no remote stylesheet, no script — because sanitizers strip those and leave you with a blank square.

```bash
inkscape logo.src.svg --export-type=svg --export-plain-svg --export-text-to-path \
         --export-filename=logo-flat.svg
npx svgo --multipass logo-flat.svg -o logo.svg
```

`logo.svg` is now the distributable: paths only, no font dependency, minified. Rasterize from it, and keep editing `logo.src.svg`.

## What each registrar wants

| Target | Format | Dimensions | Ceiling |
| --- | --- | --- | --- |
| `trustwallet/assets` | PNG, named `logo.png` | 256 × 256 | 100 kB |
| Etherscan family | SVG **or** PNG | 32 × 32 SVG, 64 × 64 PNG | — |
| Blockscout | image at a public URL | 48 × 48 | — |
| CoinGecko | PNG | 200 × 200 | — |
| CoinMarketCap | PNG | 200 × 200 | — |
| Token list `logoURI` | PNG or SVG at a URL | 256 × 256 conventional | — |
| [`wallet_watchAsset`](/wiki/economics/finance/defi/token-registration/on-chain-metadata#pushing-the-icon-at-the-wallet) image | PNG, JPG, SVG, or data URI | ≤ 512 × 512 | 256 kB |

## Rasterizing

```bash
for px in 32 48 64 128 200 256 512; do
  rsvg-convert -w "$px" -h "$px" logo.svg -o "logo-$px.png"
done
```

Inkscape does the same job if librsvg is not installed:

```bash
inkscape logo.svg --export-type=png --export-width=256 \
         --export-filename=logo-256.png
```

ImageMagick is the wrong tool for this step. Given an SVG it rasterizes at the file's intrinsic size and then resamples, so `magick logo.svg -resize 256x256` produces visibly softer edges than a direct 256-pixel render. Use it for the PNG-to-PNG work below and for inspection, and let `rsvg-convert` or Inkscape handle the vector.

## Getting under 100 kB

A flat vector mark at 256 × 256 lands around 8 kB after lossless optimization, so the Trust Wallet ceiling only becomes a problem for photographic or heavily gradient icons.

```bash
oxipng -o4 --strip safe logo-*.png            # lossless, typically 20-40% off
pngquant --quality 65-90 --ext .png --force logo-256.png   # lossy, 60-70% off
```

`pngquant` quantizes to an 8-bit palette. On flat artwork the result is indistinguishable; on a gradient it bands, which is one more reason not to use a gradient.

## Check yourself

Confirm dimensions, alpha channel, and byte count in one pass:

```bash
magick identify -format '%f  %wx%h  %[channels]  %b\n' logo-*.png
```

The `channels` field must read `srgba`. If it says `srgb`, the alpha channel was flattened somewhere and the icon now carries a white box that will be visible on every dark background.

Look at the icon the size it will actually be shown, blown up with nearest-neighbour so the pixels are visible:

```bash
magick logo-256.png -resize 20x20 -scale 400x400 preview-20.png
```

Composite it against both grounds:

```bash
magick logo-256.png -background white   -flatten on-light.png
magick logo-256.png -background '#0d1117' -flatten on-dark.png
```

And apply the circular crop the wallets apply:

```bash
magick logo-256.png \
  \( -size 256x256 xc:none -fill white -draw 'circle 128,128 128,0' \) \
  -alpha set -compose DstIn -composite circle-256.png
```

## Naming and placement

Registrars key on the [EIP](/wiki/economics/finance/defi/ethereum/eip)-55 checksummed address, mixed case, rather than the lowercase form most tools print, and some of them compare it as a string:

```bash
cast to-check-sum-address 0x1f9840a85d5af5bf1d1762f925bdaddc4201f984
# 0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984
```

And every form asks for a link rather than an upload, so the files need a permanent home before you start submitting. A path on your own domain works and can be repointed later; [IPFS](/wiki/cs/ipfs) or [Arweave](/wiki/economics/finance/defi/arweave) works and cannot. Whichever you choose, the URL is going to be copied into half a dozen third-party databases that will never re-fetch it, so treat it as immutable from the first submission onward.
