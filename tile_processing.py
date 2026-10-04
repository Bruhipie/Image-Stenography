import numpy as np


def extract_tiles(image, tile_size=8):
    """
    Divide a single-channel image into non-overlapping tiles.

    Parameters:
        image: 2D NumPy array
        tile_size: Size of each square tile

    Returns:
        tiles: List of image tiles
        cropped_image: Image cropped to complete tiles only
    """

    height, width = image.shape

    usable_height = (height // tile_size) * tile_size
    usable_width = (width // tile_size) * tile_size

    cropped_image = image[
        :usable_height,
        :usable_width
    ]

    tiles = []

    for row in range(0, usable_height, tile_size):
        for col in range(0, usable_width, tile_size):

            tile = cropped_image[
                row:row + tile_size,
                col:col + tile_size
            ]

            tiles.append(tile)

    return tiles, cropped_image


def reconstruct_image(tiles, image_shape, tile_size=8):
    """
    Reconstruct an image from its tiles.

    Parameters:
        tiles: List of image tiles
        image_shape: (height, width)
        tile_size: Size of each square tile

    Returns:
        reconstructed_image
    """

    height, width = image_shape

    reconstructed = np.zeros(
        (height, width),
        dtype=tiles[0].dtype
    )

    tile_index = 0

    for row in range(0, height, tile_size):
        for col in range(0, width, tile_size):

            reconstructed[
                row:row + tile_size,
                col:col + tile_size
            ] = tiles[tile_index]

            tile_index += 1

    return reconstructed