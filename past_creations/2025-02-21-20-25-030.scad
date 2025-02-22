
// Parameters
block_size = 40; // Size of the main block
small_block_size = 5; // Size of the small blocks
num_blocks = 16; // Number of small blocks in a circle
radius_offset = 20; // Distance from the center to the center of small blocks

module circular_blocks_on_face() {
    for (i = [0:num_blocks - 1]) {
        angle = 360 / num_blocks * i;
        translate([radius_offset * cos(angle), radius_offset * sin(angle), 0])
            cube(small_block_size, center = true);
    }
}

module block_with_circular_blocks() {
    // Main block
    cube([block_size, block_size, block_size], center = true);

    // Add circular blocks on each face of the block
    for (side = [0 : 5]) {
        rotate_vector = vectors_to_rotate(side);
        translate_vector = vectors_to_translate(side);

        rotate(rotate_vector)
            translate(translate_vector)
                circular_blocks_on_face();
    }
}

// Define rotation vectors for each cube face
function vectors_to_rotate(side) = [
    [90, 0, 0], // Bottom face
    [-90, 0, 0], // Top face
    [0, 0, 0], // Front face
    [0, 180, 0], // Back face
    [0, -90, 0], // Left face
    [0, 90, 0] // Right face
][side];

// Define translation vectors for each cube face
function vectors_to_translate(side) = [
    [0, 0, -block_size / 2], // Bottom face
    [0, 0, block_size / 2], // Top face
    [0, block_size / 2, 0], // Front face
    [0, -block_size / 2, 0], // Back face
    [-block_size / 2, 0, 0], // Left face
    [block_size / 2, 0, 0] // Right face
][side];

// Render the block with small blocks on each face
block_with_circular_blocks();
