import cv2

# Load the original image
image = cv2.imread("data/input/original.jpg")

if image is None:
    print("ERROR: Could not load the image.")
    exit()

print("SUCCESS: Image loaded!")
print("Original image shape:", image.shape)

# Convert BGR to YCrCb
ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)

# Separate the three channels
Y, Cr, Cb = cv2.split(ycrcb)

print("\nYCbCr conversion successful!")

print("Y shape :", Y.shape)
print("Cr shape:", Cr.shape)
print("Cb shape:", Cb.shape)

print("\nData types:")
print("Y :", Y.dtype)
print("Cr:", Cr.dtype)
print("Cb:", Cb.dtype)

# Save the three channels for verification
cv2.imwrite("results/images/Y_channel.png", Y)
cv2.imwrite("results/images/Cr_channel.png", Cr)
cv2.imwrite("results/images/Cb_channel.png", Cb)

print("\nChannels saved successfully!")

# ==========================================
# STEP 2: DIVIDE Y CHANNEL INTO 8x8 TILES
# ==========================================

tile_size = 8

height, width = Y.shape

# Use only the complete 8x8 tiles
usable_height = (height // tile_size) * tile_size
usable_width = (width // tile_size) * tile_size

Y_cropped = Y[:usable_height, :usable_width]

# Store all 8x8 tiles
tiles = []

for row in range(0, usable_height, tile_size):
    for col in range(0, usable_width, tile_size):
        tile = Y_cropped[row:row + tile_size, col:col + tile_size]
        tiles.append(tile)

print("\nTiling successful!")
print("Original Y size:", Y.shape)
print("Cropped Y size:", Y_cropped.shape)
print("Number of 8x8 tiles:", len(tiles))
print("First tile shape:", tiles[0].shape)
# ==========================================
# STEP 3: TILE EXTRACTION FUNCTION
# ==========================================

def extract_tiles(Y, tile_size=8):
    """
    Divide the Y channel into non-overlapping tiles.
    Each tile is tile_size x tile_size.
    """

    height, width = Y.shape

    usable_height = (height // tile_size) * tile_size
    usable_width = (width // tile_size) * tile_size

    cropped = Y[:usable_height, :usable_width]

    tiles = []

    for row in range(0, usable_height, tile_size):
        for col in range(0, usable_width, tile_size):
            tile = cropped[row:row + tile_size,
                           col:col + tile_size]

            tiles.append(tile)

    return tiles, cropped

# Test the tile extraction function
test_tiles, test_cropped = extract_tiles(Y)

print("\nFunction test successful!")
print("Number of tiles:", len(test_tiles))
print("First tile shape:", test_tiles[0].shape)
print("Cropped image shape:", test_cropped.shape)
# ==========================================
# STEP 4: TILE INFORMATION FOR MEMBER 1
# ==========================================

rows_of_tiles = test_cropped.shape[0] // 8
cols_of_tiles = test_cropped.shape[1] // 8

print("\nTile information for Member 1:")
print("Rows of tiles:", rows_of_tiles)
print("Columns of tiles:", cols_of_tiles)
print("Total tiles:", rows_of_tiles * cols_of_tiles)
# ==========================================
# STEP 5: RECONSTRUCT Y FROM TILES
# ==========================================

reconstructed_Y = test_cropped.copy()

tile_index = 0

for row in range(0, test_cropped.shape[0], 8):
    for col in range(0, test_cropped.shape[1], 8):
        reconstructed_Y[row:row + 8, col:col + 8] = test_tiles[tile_index]
        tile_index += 1

# Check whether reconstruction is identical
difference = cv2.absdiff(test_cropped, reconstructed_Y)

print("\nReconstruction test:")
print("Maximum pixel difference:", difference.max())

if difference.max() == 0:
    print("SUCCESS: Y channel reconstructed perfectly!")
else:
    print("ERROR: Reconstruction is not identical.")

    # ============================================================
# STEP 5: CREATE TILE INDEX MAPPING FOR MEMBER 1
# ============================================================

tile_mapping = []

for tile_index in range(len(test_tiles)):
    row = tile_index // cols_of_tiles
    col = tile_index % cols_of_tiles

    tile_mapping.append({
        "tile_index": tile_index,
        "row": row,
        "column": col
    })

print("\nTile mapping created successfully!")

print("First 5 tile mappings:")
for item in tile_mapping[:5]:
    print(item)

print("\nLast 5 tile mappings:")
for item in tile_mapping[-5:]:
    print(item)

print("\nTotal mappings:", len(tile_mapping))
# ============================================================
# STEP 6: SAVE TILE INFORMATION
# ============================================================

import json

tile_info = {
    "image_height": int(test_cropped.shape[0]),
    "image_width": int(test_cropped.shape[1]),
    "tile_size": 8,
    "rows": int(rows_of_tiles),
    "columns": int(cols_of_tiles),
    "total_tiles": len(tile_mapping)
}

with open("results/tile_info.json", "w") as f:
    json.dump(tile_info, f, indent=4)

print("\nTile information saved successfully!")
print("File: results/tile_info.json")