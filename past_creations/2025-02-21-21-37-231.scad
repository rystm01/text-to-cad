
module vase() {
    difference() {
        // Outer shape
        rotate_extrude(angle = 360)
        translate([3, 0, 0])
        scale([1, 1.25])
        offset(r = 0.5)
        polygon(points = [[0,0], [6,0], [3,15], [0,15]]);

        // Inner hollow
        translate([0, 0, 1])
        rotate_extrude(angle = 360)
        translate([3, 0, 0])
        scale([0.8, 1.1])
        offset(r = 0.5)
        polygon(points = [[0,0], [5,0], [3,14], [0,14]]);
    }
}

vase();
