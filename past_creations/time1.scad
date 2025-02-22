
$fn = 100; // set resolution for smooth curves

module roman_vase() {
    // Main body of the vase
    difference() {
        // Outer shape of the vase
        rotate_extrude(angle = 360)
        translate([3, 0, 0])
        scale([1.5, 1.5]) {
            polygon(points=[
                [0, 0],
                [2, 0],
                [2.5, 3],
                [1.8, 4],
                [1, 8],
                [1.2, 10],
                [0.8, 12],
                [0, 14]
            ]);
        }
      
        // Hollow out the center
        translate([0, 0, 0.5]) {
            rotate_extrude(angle = 360)
            translate([3, 0, 0])
            polygon(points=[
                [0.5, 0],
                [1.8, 4],
                [1, 8],
                [1.2, 10],
                [0.8, 12],
                [0, 13.5]
            ]);
        }
    }

    // Add handles
    translate([-2, 0, 7])
    rotate([90, 0, 90])
    cylinder(r1=0.8, r2=0.4, h=3);

    translate([2, 0, 7])
    rotate([90, 0, 270])
    cylinder(r1=0.8, r2=0.4, h=3);
}

roman_vase();
