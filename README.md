# SVD-Based Image Steganography

A Python-based image steganography application that embeds secret text into cover images using Singular Value Decomposition (SVD) and YCrCb color space transformation. The tool achieves imperceptible data hiding by quantizing singular values across non-overlapping 8×8 blocks of the luminance channel.

---

## Technical Overview

### 1. Color Space Conversion (YCrCb)
Cover images are converted from BGR to YCrCb. The secret payload is embedded strictly into the luminance (Y) channel to minimize visible color artifacts, leaving chrominance channels (Cr, Cb) untouched.

### 2. Block Tiling
The Y channel is divided into sequential, non-overlapping 8×8 pixel tiles. Each 8×8 block accommodates exactly 1 bit of information.

### 3. Singular Value Quantization (SVD)
For each 8×8 tile matrix **A**, Singular Value Decomposition factors the block:

> **A = U · Σ · Vᵀ**  
> where **Σ = diag(S₀, S₁, ..., S₇)**

Bits are embedded by parity quantization of the second singular value (**S₁**) using a step size **Δ = 20.0**:

* **Embedding**: Compute `q = floor(S₁ / Δ)`
  * For bit **1**, adjust S₁ so that `floor(S₁ / Δ)` is odd.
  * For bit **0**, adjust S₁ so that `floor(S₁ / Δ)` is even.
* **Extraction**: Compute the parity directly from the reconstructed tile's singular values:
  * **bit = round(S₁ / Δ) mod 2**

### 4. Framing & Storage Constraints
* **Length Header**: The bitstream begins with a 16-bit unsigned integer representing message character length. This prevents reading uninitialized trailing blocks during extraction.
* **Format**: Stego images must be stored using lossless compression (`.png`). Lossy formats (like `.jpeg`) alter matrix values and corrupt the singular value parity.

---

## Project Structure

```text
.
├── translator.py          # text_to_bits() and bits_to_text() with 16-bit header
├── tile_processing.py     # 8x8 tile extraction and channel reconstruction
├── color_processing.py    # Color space transformations and validations
├── svd_processor.py       # SVD factorization and singular value quantization
├── main.py                # Interactive CLI for encoding and decoding
└── README.md              # Project documentation