
// Abstract representation of a horse

// Parameters
scale_factor = 2;

// Main body
module horse() {
    difference() {
        // Body
        translate([0, 0, 5 * scale_factor])
        scale([scale_factor, scale_factor, scale_factor])
        rotate([90, 0, 0]) {
            cylinder(h=10, r1=3, r2=3, center=false, $fn=50); // Main body
        }
        
        // Head
        translate([6 * scale_factor, 0, 8 * scale_factor])
        scale([scale_factor, scale_factor, scale_factor])
        rotate([90, 0, 0]) {
            cylinder(h=5, r1=2, r2=2, center=false, $fn=50);
        }
    }
}

// Legs
module leg() {
    scale([scale_factor, scale_factor, scale_factor])
    rotate([90, 0, 0]) {
        cylinder(h=10, r1=0.5, r2=0.5, center=false, $fn=20);
    }
}

// Neck
module neck() {
    scale([scale_factor, scale_factor, scale_factor])
    rotate([-20, 0, 0]) {
        translate([5, 0, 5])
        cylinder(h=5, r1=1, r2=1, center=false, $fn=20);
    }
}

// Tail
module tail() {
    scale([scale_factor, scale_factor, scale_factor])
    rotate([90, 0, 0]) {
        translate([-5, 0, -8])
        cylinder(h=5, r1=0.5, r2=0.5, center=false, $fn=20);
    }
}

// Assembly
union() {
    horse();
    neck();
    tail();
    // Legs
    translate([2 * scale_factor, 2 * scale_factor, 0])
    leg();
    translate([-2 * scale_factor, 2 * scale_factor, 0])
    leg();
    translate([2 * scale_factor, -2 * scale_factor, 0])
    leg();
    translate([-2 * scale_factor, -2 * scale_factor, 0])
    leg();
}
