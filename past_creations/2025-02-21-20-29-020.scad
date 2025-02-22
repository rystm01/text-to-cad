
// Parameters
block_size = 20;
pyramid_height = 10;

// Main block with pyramids
module block_with_pyramids() {
    // Central block
    cube([block_size, block_size, block_size], center=true);
    
    // Pyramids
    pyramid([0, 0, block_size/2 + pyramid_height], "z");
    pyramid([block_size/2 + pyramid_height, 0, 0], "x");
    pyramid([-block_size/2 - pyramid_height, 0, 0], "x");
    pyramid([0, block_size/2 + pyramid_height, 0], "y");
    pyramid([0, -block_size/2 - pyramid_height, 0], "y");
    pyramid([0, 0, -block_size/2 - pyramid_height], "z");
}

module pyramid(position, axis) {
    translate(position)
    rotate_pyramid(axis)
    {
        // Create a pyramid with a square base
        polyhedron(
            points=[
                [block_size/2, block_size/2, 0],
                [-block_size/2, block_size/2, 0],
                [-block_size/2, -block_size/2, 0],
                [block_size/2, -block_size/2, 0],
                [0, 0, pyramid_height]
            ],
            faces=[
                [0, 1, 4],
                [1, 2, 4],
                [2, 3, 4],
                [3, 0, 4],
                [0, 1, 2, 3]
            ]
        );
    }
}

// Function to rotate the pyramid based on the given axis
module rotate_pyramid(axis) {
    if (axis == "x") {
        rotate([0, 90, 0]);
    } else if (axis == "y") {
        rotate([90, 0, 0]);
    } else if (axis == "z") {
        // No rotation needed for the z-axis
    }
}

block_with_pyramids();
