
// Vase Profile Points
vase_profile = [
    [0, 0],      // Base center
    [10, 0],     // Base radius
    [8, 10],     // Narrow section
    [15, 30],    // Mid body
    [12, 40],    // Neck
    [20, 45]     // Top
];

// Rotational extrusion to form vase
rotate_extrude(angle = 360)
    polygon(points = vase_profile);
