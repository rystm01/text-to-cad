
$fn = 100;

module vase() {
    rotate_extrude(angle = 360) {
        translate([5, 0, 0]) {
            scale([1, 1]) {
                polygon(points = [
                    [0, 0],
                    [1, 0.5],
                    [0.8, 2],
                    [1.5, 4],
                    [0.3, 8],
                    [0.5, 10],
                    [0, 10]
                ]);
            }
        }
    }
}

vase();
