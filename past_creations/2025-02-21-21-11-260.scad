
// Roman Pillar Dimensions
pillar_height = 100;    // Height of the pillar shaft
pillar_radius = 10;     // Radius of the pillar shaft
base_height = 15;       // Height of the base
base_radius = 14;       // Radius of the base
capital_height = 20;    // Height of the capital
capital_radius = 15;    // Radius of the capital

// Create the Roman Pillar
module roman_pillar() {
    // Base of the Pillar
    cylinder(h = base_height, r = base_radius, center = false);
    
    // Shaft of the Pillar
    translate([0, 0, base_height])
        cylinder(h = pillar_height, r = pillar_radius, center = false);
    
    // Capital of the Pillar
    translate([0, 0, base_height + pillar_height])
        cylinder(h = capital_height, r1 = capital_radius, r2 = pillar_radius, center = false);
}

// Call the roman_pillar module to render the pillar
roman_pillar();
