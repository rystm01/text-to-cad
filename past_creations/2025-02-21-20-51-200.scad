
module pyramid(size, height) {
    polyhedron(
        points=[
            [0, 0, 0],  // base corner 1
            [size, 0, 0],  // base corner 2
            [size, size, 0],  // base corner 3
            [0, size, 0],  // base corner 4
            [size/2, size/2, height]  // apex
        ],
        faces=[
            [0, 1, 4],  // side 1
            [1, 2, 4],  // side 2
            [2, 3, 4],  // side 3
            [3, 0, 4],  // side 4
            [0, 1, 2, 3]  // base
        ]
    );
}

module cube_with_pyramids(cube_size, pyramid_height) {
    cube([cube_size, cube_size, cube_size], center=true);
    for (i = [-1, 1], j = [-1, 1], k = [-1, 1]) {
        if (i == 0) {  // Only position pyramid for i=0
            translate([j * cube_size / 2, k * cube_size / 2, 0])
            rotate([0, 90 - 90 * k, 90 * k * j])
            pyramid(cube_size, pyramid_height);
        }
        if (j == 0) {  // Only position pyramid for j=0
            translate([i * cube_size / 2, 0, k * cube_size / 2])
            rotate([90 - 90 * k, 0, 90 * k * i])
            pyramid(cube_size, pyramid_height);
        }
        if (k == 0) {  // Only position pyramid for k=0
            translate([0, i * cube_size / 2, j * cube_size / 2])
            rotate([90 * i, 90 - 90 * j, 0])
            pyramid(cube_size, pyramid_height);
        }
    }
}

cube_size = 20;
pyramid_height = 10;

cube_with_pyramids(cube_size, pyramid_height);
