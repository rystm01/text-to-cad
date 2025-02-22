
// Parameters
height = 200;         // Total height of the vase
base_radius = 20;     // Radius of the base
max_radius = 40;      // Maximum radius of the vase
neck_radius = 10;     // Radius of the neck
neck_height = 50;     // Height of the neck section

// Vase profile
module vase_profile() {
    polygon(points=[
        [0, 0],
        [base_radius, 0],
        [max_radius, height * 0.4],
        [max_radius, height * 0.6],
        [neck_radius, height - neck_height],
        [neck_radius, height],
        [0, height]
    ]);
}

// Vase module
module vase() {
    rotate_extrude($fn=100)
        translate([base_radius, 0])
        vase_profile();
}

// Render the vase
vase();
