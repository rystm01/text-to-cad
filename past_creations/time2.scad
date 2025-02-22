
// Simple Horse Model
module horse() {
    // Body
    scale([1, 0.5, 0.3])
        translate([0, 0, 8])
        cylinder(h = 20, r = 5, center = true);

    // Head
    translate([5, 0, 12])
        rotate([0, 0, 45])
        scale([1, 0.5, 0.5])
        sphere(r = 3);
    
    // Neck
    translate([2.5, 0, 10])
        rotate([0, 0, 45])
        cylinder(h = 8, r1 = 2, r2 = 1, center = false);

    // Tail
    translate([-10, 0, 6])
        cube([2, 1, 10]);

    // Legs
    leg([3.5, 2, 0]);
    leg([-3.5, 2, 0]);
    leg([3.5, -3, 0]);
    leg([-3.5, -3, 0]);

}

module leg(position) {
    translate(position)
        rotate([90, 0, 0])
        cylinder(h = 10, r = 0.8, center = true);
}

horse();
