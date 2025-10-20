import pygame
from entity.terrain import Terrain

TILE_SIZE = 64  # each block = 64x64 pixels


class Level:
    """Base class for all levels."""
    def __init__(self, level_id, spawn, map_size, terrain_matrix):
        self.level_id = level_id
        self.spawn = spawn

        # Add 1-block border around the terrain matrix
        self.terrain_matrix = self.add_border(terrain_matrix)

        # Automatically recalculate map size based on bordered matrix
        self.map_size = (
            len(self.terrain_matrix[0]) * TILE_SIZE,  # width
            len(self.terrain_matrix) * TILE_SIZE      # height
        )

    def add_border(self, matrix):
        """Add a 1-block thick border around the map."""
        if not matrix:
            return [[1]]

        rows = len(matrix)
        cols = len(matrix[0])

        # Create new bordered matrix
        bordered = [[1] * (cols + 2)]  # top border
        for row in matrix:
            bordered.append([1] + row + [1])  # left/right borders
        bordered.append([1] * (cols + 2))  # bottom border

        return bordered

    def get_terrain(self):
        """Convert terrain matrix into a list of Terrain objects."""
        terrain_list = []
        for row_index, row in enumerate(self.terrain_matrix):
            for col_index, tile in enumerate(row):
                if tile == 1:  # solid block
                    x = col_index * TILE_SIZE
                    y = row_index * TILE_SIZE
                    terrain_list.append(Terrain(x, y, TILE_SIZE))
        return terrain_list


# ===========================================================
#                    HORIZONTAL MAP LEVELS
# ===========================================================

class Level1(Level):
    """Flat horizontal level"""
    def __init__(self):
        terrain_matrix = [
            [0] * 80 for _ in range(10)
        ]
        terrain_matrix.append([1] * 80)  # bottom ground row

        super().__init__(
            level_id=1,
            spawn=(100, 704 - 128),
            map_size=(5120, 704),
            terrain_matrix=terrain_matrix
        )


class Level2(Level):
    """Gentle slopes and gaps"""
    def __init__(self):
        terrain_matrix = [[0] * 80 for _ in range(10)]

        # Uneven terrain
        terrain_matrix[9][0:20] = [1] * 20
        terrain_matrix[9][25:40] = [1] * 15
        terrain_matrix[9][45:80] = [1] * 35

        # Elevated platforms
        terrain_matrix[7][10:15] = [1] * 5
        terrain_matrix[6][30:35] = [1] * 5
        terrain_matrix[8][50:55] = [1] * 5

        super().__init__(
            level_id=2,
            spawn=(150, 704 - 160),
            map_size=(5120, 704),
            terrain_matrix=terrain_matrix
        )


class Level3(Level):
    """Platforming challenge with holes"""
    def __init__(self):
        terrain_matrix = [[0] * 80 for _ in range(10)]

        # Ground with gaps
        terrain_matrix[9] = [
            1 if not (10 <= i < 13 or 30 <= i < 33 or 55 <= i < 58) else 0
            for i in range(80)
        ]

        # Floating platforms
        terrain_matrix[6][15:20] = [1] * 5
        terrain_matrix[5][40:45] = [1] * 5
        terrain_matrix[7][60:65] = [1] * 5

        super().__init__(
            level_id=3,
            spawn=(100, 704 - 192),
            map_size=(5120, 704),
            terrain_matrix=terrain_matrix
        )
