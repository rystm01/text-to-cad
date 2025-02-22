
// Parameters
cylinder_radius = 50;
cylinder_height = 100;
hole_radius = 10;
hole_position_x = 25;  // Adjust position as needed
hole_position_y = 0;
hole_position_z = 50;  // Centered vertically

// Main Cylinder
module main_cylinder() {
    cylinder(h = cylinder_height, r = cylinder_radius, $fn = 100);  // Increased $fn for smoothness
}

// Hole
module hole() {
    translate([hole_position_x, hole_position_y, hole_position_z])
    rotate([90,0,0])
    cylinder(h = cylinder_radius*2, r = hole_radius, $fn = 100);  // Ensure length is enough to pass through
}

// Main difference
difference() {
    main_cylinder();
    hole();
}
