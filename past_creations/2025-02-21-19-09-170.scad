
$fn = 100;  // Sets the resolution of the circular parts

module vase(height, top_diameter, bottom_diameter, thickness) {
    difference() {
        // Outer shape of the vase
        scale([1,1,2]) 
            rotate_extrude(angle = 360)
                translate([bottom_diameter/2, 0, 0])
                    offset(r = thickness)
                      polygon(points=[ 
                          [0, 0], 
                          [-bottom_diameter/2, height/4], 
                          [-top_diameter/2, height]
                      ]);
        
        // Inner shape of the vase (hollow part)
        scale([1,1,2]) 
            rotate_extrude(angle = 360)
                translate([bottom_diameter/2 - thickness, 0, 0])
                    polygon(points=[ 
                        [0, 0], 
                        [-(bottom_diameter/2 - thickness), height/4], 
                        [-(top_diameter/2 - thickness), height]
                    ]);
    }
}

// Parameters: height, top diameter, bottom diameter, thickness
vase(100, 40, 60, 3);
