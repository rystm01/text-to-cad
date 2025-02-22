
// Parameters
module roman_pillar(
    height = 200,
    base_height = 20,
    capital_height = 30,
    shaft_radius = 20,
    base_radius = 30,
    capital_radius = 25,
    flute_count = 8,
    flute_depth = 1.5,
    detail = 100
) {
    // Base
    difference() {
        cylinder(h = base_height, r = base_radius, $fn = detail);
        cylinder(h = base_height + 1, r = shaft_radius + 1, $fn = detail);
    }

    // Shaft with flutes
    translate([0, 0, base_height])
    shaft(shaft_radius, height - base_height - capital_height, flute_count, flute_depth, detail);

    // Capital
    translate([0, 0, height - capital_height])
    capital(capital_radius, capital_height, detail);
}

// Shaft module with flutes
module shaft(r, h, flute_count, depth, detail) {
    cylinder(h = h, r = r, $fn = detail);

    // Create flutes
    for(i = [0:flute_count-1]) {
        angle = 360 / flute_count * i;
        rotate([0,0,angle])
        translate([r - depth, 0, 0])
        linear_extrude(height = h)
        polygon(points = [
            [0,0],
            [depth, depth],
            [depth, -depth]
        ]);
    }
}

// Capital module (Ionic style)
module capital(r, h, detail) {
    // Simple Ionic capital with volutes
    cylinder(h = h/2, r1 = r, r2 = r, $fn = detail);
    translate([0,0,h/2])
    difference() {
        cylinder(h = h/2, r1 = r, r2 = r, $fn = detail);
        for(angle = [45, 225]) {
            rotate([0,0,angle])
            translate([r*0.5,0,0])
            scale([0.3, 0.3, 1])
            rotate([90,0,0])
            cylinder(h = h/2, r = r*0.5, $fn = 16);
        }
    }
}

// Render the Roman pillar
roman_pillar();
