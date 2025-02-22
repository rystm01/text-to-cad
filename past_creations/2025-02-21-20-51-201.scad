
// Size of the cube and pyramids
cubeSize = 20;
pyramidHeight = 10;

// Cube with pyramids
module cubeWithPyramids() {
    // Draw the central cube
    cube([cubeSize, cubeSize, cubeSize], center = true);

    // Pyramids on each face
    translate([0, 0, cubeSize / 2 + pyramidHeight / 2])
        rotate([0, 0, 0])
        pyramid();

    translate([0, 0, -cubeSize / 2 - pyramidHeight / 2])
        rotate([180, 0, 0])
        pyramid();

    translate([cubeSize / 2 + pyramidHeight / 2, 0, 0])
        rotate([0, 0, -90])
        pyramid();

    translate([-cubeSize / 2 - pyramidHeight / 2, 0, 0])
        rotate([0, 0, 90])
        pyramid();

    translate([0, cubeSize / 2 + pyramidHeight / 2, 0])
        rotate([90, 0, 0])
        pyramid();

    translate([0, -cubeSize / 2 - pyramidHeight / 2, 0])
        rotate([-90, 0, 0])
        pyramid();
}

// Pyramid module
module pyramid() {
    polyhedron(
        points = [
            [0, 0, pyramidHeight],
            [-cubeSize / 2, -cubeSize / 2, 0],
            [-cubeSize / 2, cubeSize / 2, 0],
            [cubeSize / 2, cubeSize / 2, 0],
            [cubeSize / 2, -cubeSize / 2, 0]
        ],
        faces = [
            [0, 1, 2],
            [0, 2, 3],
            [0, 3, 4],
            [0, 4, 1],
            [1, 2, 3, 4]
        ]
    );
}

// Call the module
cubeWithPyramids();
