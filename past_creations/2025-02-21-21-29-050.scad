
// Simple representation of a "big guy"
module big_guy() {
    difference() {
        // Body - a large cylinder
        translate([0, 0, 0])
        cylinder(h=60, r=20, center=true);
        
        // Head - a smaller sphere
        translate([0, 0, 35])
        sphere(r=12);

        // Legs - two smaller cylinders
        translate([-10, 0, -50])
        cylinder(h=40, r=6, center=true);
        
        translate([10, 0, -50])
        cylinder(h=40, r=6, center=true);

        // Arms - two medium-sized cylinders
        translate([-30, 0, 10])
        rotate([0, 90, 0])
        cylinder(h=40, r=5, center=true);
        
        translate([30, 0, 10])
        rotate([0, 90, 0])
        cylinder(h=40, r=5, center=true);
    }
}

// Call the module to render the big guy
big_guy();
