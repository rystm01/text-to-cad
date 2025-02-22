
// Parameters for vase dimensions
vase_height = 200;
vase_width = 100;
neck_height = 50;
neck_width = 40;
base_height = 20;
base_width = 60;

// Function to define the profile of the vase
module vase_profile() {
    // Define the shape using a series of points
    polyline = [
        [0, 0], // Bottom of vase
        [base_width / 2, 0],
        [base_width / 2, base_height], // Base transition
        [vase_width / 2, vase_height - neck_height], // Main body
        [neck_width / 2, vase_height], // Neck
        [0, vase_height] // Top center
    ];
    
    // Create the profile for rotation
    polygon(points = polyline);
}

// Create the 3D vase by rotating the profile
rotate_extrude() {
    vase_profile();
}
