import numpy as np

DELTA = 20.0  # Quantization step size

def embed_bit_svd(tile: np.ndarray, bit: int, delta: float = DELTA) -> np.ndarray:
    if bit not in (0, 1):
        raise ValueError("Bit must be either 0 or 1.")

    tile_float = tile.astype(np.float64)
    U, S, Vt = np.linalg.svd(tile_float, full_matrices=True)
    
    # Quantize S[1] so that round(S[1] / delta) has the same parity as the bit
    q = np.floor(S[1] / delta)
    if bit == 1:
        if q % 2 == 0:
            S[1] = (q + 1) * delta
        else:
            S[1] = q * delta
    else:  # bit == 0
        if q % 2 != 0:
            S[1] = (q + 1) * delta
        else:
            S[1] = q * delta

    S_matrix = np.zeros((8, 8), dtype=np.float64)
    np.fill_diagonal(S_matrix, S)
    
    reconstructed_tile = U @ S_matrix @ Vt
    stego_tile = np.clip(reconstructed_tile, 0, 255)
    return stego_tile


def extract_bit_svd(tile: np.ndarray, delta: float = DELTA) -> int:
    tile_float = tile.astype(np.float64)
    _, S, _ = np.linalg.svd(tile_float, full_matrices=True)
    
    # Check parity of the quantized singular value
    q = int(np.round(S[1] / delta))
    return q % 2