
// Define parameters for the hat
hat_height = 50;            // Height of the conical hat part
hat_rad_top = 5;            // Top radius (small point of the cone)
hat_rad_bottom = 100;       // Bottom radius of the hat

// Create the conical part of the hat
module chinese_hat() {
    difference() {
        // Cone
        cylinder(h = hat_height, r1 = hat_rad_bottom, r2 = hat_rad_top);

        // Hollow inside
        translate([0, 0, -1])
        cylinder(h = hat_height + 1, r1 = hat_rad_bottom - 5, r2 = hat_rad_top);
    }
}

// Render the hat
chinese_hat();
