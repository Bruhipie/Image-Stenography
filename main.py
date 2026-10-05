import os
import cv2
import numpy as np

from translator import text_to_bits, bits_to_text
from tile_processing import extract_tiles, reconstruct_image
from svd_processor import embed_bit_svd, extract_bit_svd, DELTA


def encode_image(input_image_path: str, secret_text: str, output_image_path: str, delta: float = DELTA):
    image = cv2.imread(input_image_path)
    if image is None:
        raise FileNotFoundError(f"Could not open image at '{input_image_path}'.")

    # Convert to YCrCb & split channels
    ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    Y, Cr, Cb = cv2.split(ycrcb)

    # Extract 8x8 tiles from Y channel
    tiles, cropped_Y = extract_tiles(Y, tile_size=8)
    
    # Convert text message to bit list
    bits = text_to_bits(secret_text)
    if len(bits) > len(tiles):
        raise ValueError(
            f"Message too long! Requires {len(bits)} tiles, but image only provides {len(tiles)} tiles."
        )

    print(f"Embedding {len(bits)} bits ({len(secret_text)} characters) into {len(tiles)} tiles...")

    # Embed bits into tiles using SVD quantization
    modified_tiles = []
    for i, tile in enumerate(tiles):
        if i < len(bits):
            mod_tile = embed_bit_svd(tile, bits[i], delta=delta)
            modified_tiles.append(mod_tile.astype(np.uint8))
        else:
            modified_tiles.append(tile)

    # Reconstruct Y channel & merge back
    stego_Y = reconstruct_image(modified_tiles, cropped_Y.shape, tile_size=8)
    h, w = cropped_Y.shape
    stego_ycrcb = cv2.merge([stego_Y, Cr[:h, :w], Cb[:h, :w]])
    stego_image = cv2.cvtColor(stego_ycrcb, cv2.COLOR_YCrCb2BGR)

    # Ensure output directory exists and save as PNG (lossless)
    os.makedirs(os.path.dirname(output_image_path) or ".", exist_ok=True)
    cv2.imwrite(output_image_path, stego_image)
    print(f"Saved stego image to: {output_image_path}")


def decode_image(stego_image_path: str, delta: float = DELTA) -> str:
    stego_image = cv2.imread(stego_image_path)
    if stego_image is None:
        raise FileNotFoundError(f"Could not open image at '{stego_image_path}'.")

    ycrcb = cv2.cvtColor(stego_image, cv2.COLOR_BGR2YCrCb)
    Y, _, _ = cv2.split(ycrcb)

    tiles, _ = extract_tiles(Y, tile_size=8)
    extracted_bits = [extract_bit_svd(tile, delta=delta) for tile in tiles]
    return bits_to_text(extracted_bits)


def get_valid_image_path(prompt_text: str) -> str:
    while True:
        path = input(prompt_text).strip().strip("'\"")
        if os.path.isfile(path):
            return path
        print(f"Error: File '{path}' does not exist. Please enter a valid path.")


def main():
    print("--- SVD Image Steganography ---")
    print("1. Encode secret message into image")
    print("2. Decode secret message from image")
    choice = input("Select an option (1/2): ").strip()

    if choice == "1":
        img_path = get_valid_image_path("Enter cover image path: ")
        secret_text = input("Enter the secret message to hide: ")
        output_path = input("Enter destination path (e.g., results/images/stego.png): ").strip().strip("'\"")
        
        if not output_path.lower().endswith(".png"):
            output_path += ".png"
            print(f"Note: Saved with .png extension to prevent lossy compression: {output_path}")

        encode_image(img_path, secret_text, output_path)

    elif choice == "2":
        stego_path = get_valid_image_path("Enter stego image path (.png): ")
        extracted_message = decode_image(stego_path)
        print("\n--- Extracted Message ---")
        print(extracted_message)

    else:
        print("Invalid option selected. Exiting.")


if __name__ == "__main__":
    main()