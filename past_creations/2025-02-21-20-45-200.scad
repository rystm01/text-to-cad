
// Parameters
coaster_radius = 50; // Radius of the coaster's base
coaster_thickness = 5; // Thickness of the coaster
edge_height = 3; // Height of the raised edge
edge_thickness = 2; // Thickness of the raised edge

// Coaster Base
module coaster() {
    // Base of the coaster
    cylinder(h = coaster_thickness, r = coaster_radius);
  
    // Raised Edge
    translate([0, 0, coaster_thickness])
        cylinder(h = edge_height, r = coaster_radius + edge_thickness);
        
    // Subtract Inner Circle to create actual edge
    translate([0, 0, coaster_thickness])
        cylinder(h = edge_height + 0.1, r = coaster_radius); // +0.1 to ensure clean subtraction
}

// Call the coaster module
coaster();
