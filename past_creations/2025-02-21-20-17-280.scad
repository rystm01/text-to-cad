
// Define a simple profile for the vase
vase_profile = [
    [0, 0],    // Bottom point at the origin
    [10, 0],   // Base of the vase (radius of 10 units)
    [8, 20],   // Tapering inward
    [12, 40],  // Widening outwards
    [7, 60],   // Neck of the vase
    [0, 80]    // Top of the vase
];

// Rotate the profile around the Z-axis to create a vase
rotate_extrude(angle = 360)
    polygon(vase_profile);
