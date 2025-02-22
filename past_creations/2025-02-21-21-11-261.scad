
// Parameters
base_radius = 10;
shaft_height = 100;
shaft_radius = 8;
capital_height = 10;
flute_count = 20;
flute_depth = 0.5;

// Column Function
module roman_pillar() {
    // Base
    cylinder(h = base_radius, r1 = base_radius, r2 = base_radius);

    // Shaft with flutes
    translate([0, 0, base_radius])
        shaft();

    // Capital
    translate([0, 0, base_radius + shaft_height])
        cylinder(h = capital_height, r1 = base_radius, r2 = shaft_radius);
}

// Shaft with flutes
module shaft() {
    difference() {
        cylinder(h = shaft_height, r = shaft_radius);
        for (i = [0 : 360 / flute_count : 360]) {
            rotate([0, 0, i]) {
                translate([shaft_radius, 0, 0])
                    cylinder(h = shaft_height, r1 = flute_depth, r2 = flute_depth);
            }
        }
    }
}

// Create the column
roman_pillar();
