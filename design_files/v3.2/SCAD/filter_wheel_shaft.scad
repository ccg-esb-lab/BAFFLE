//import("/Users/ESB/Downloads/Motor_Mount_Plate.stl");

d=0.2;

wall=3;

$fs = 0.2;

w_plate=82;
h_plate=40;

depth_plate=3;

r_shaft=4.5;
r_bearing=8.4;

r_screw=2.75;

depth_device=20;

w_openbuilds=40;
depth_openbuilds=20;
l_openbuilds=100;

depth_bearing=6;

/********************/

//color([1,1,1]) translate([40+d,0,0]) cube([w_openbuilds, l_openbuilds, depth_openbuilds], center=true);

translate([0,0,-depth_device/2-d]) plate_top();

//translate([0,0,depth_device/2+d]) color([0,1,1]) mirror([0,0,1]) plate_top();

//color([1,0,1]) spacer();




module spacer(){
    difference() {
        translate([0,0,0]) cylinder(r=r_bearing-2*d, h=(depth_openbuilds)-2*depth_bearing-2*d, center=true, $fn=100);
        cylinder(r=r_shaft, h=depth_device*2, center=true, $fn=100);
        
    }
}


module plate_top(){

    //translate([w_plate/4,0,depth_openbuilds/4-depth_plate/2]) cube([w_plate, h_plate, depth_openbuilds/2+d+depth_plate], center=true);
    
    difference(){

        translate([w_plate/4,0,depth_openbuilds/4-depth_plate/2])  roundedcube([w_plate, h_plate, depth_openbuilds/2+d+depth_plate], true, 5, "z");
        
        translate([w_plate-w_openbuilds+.5,0,depth_openbuilds/2]) cube([w_openbuilds+d, h_plate+d, depth_openbuilds], center=true);
        
        cylinder(r=r_shaft, h=depth_device*2, center=true, $fn=100);
        translate([0,0,depth_openbuilds/2]) cylinder(r=r_bearing, h=depth_openbuilds, center=true, $fn=100);
        
        // Openbuilds Screws
        translate([32.5,10,0]) cylinder(r=r_screw, h=depth_device*2, center=true, $fn=100);
        translate([32.5,-10,0]) cylinder(r=r_screw, h=depth_device*2, center=true, $fn=100);
        translate([52.5,10,0]) cylinder(r=r_screw, h=depth_device*2, center=true, $fn=100);
        translate([52.5,-10,0]) cylinder(r=r_screw, h=depth_device*2, center=true, $fn=100);
        
        
        // Openbuilds Screws
        rotate([0,0,45]) translate([20,0,0]) cylinder(r=r_screw, h=depth_device*2, center=true, $fn=100);
        rotate([0,0,45*3]) translate([20,0,0]) cylinder(r=r_screw, h=depth_device*2, center=true, $fn=100);
        rotate([0,0,45*5]) translate([20,0,0]) cylinder(r=r_screw, h=depth_device*2, center=true, $fn=100);
        rotate([0,0,45*7]) translate([20,0,0]) cylinder(r=r_screw, h=depth_device*2, center=true, $fn=100);
    }
}



module roundedcube(size = [1, 1, 1], center = false, radius = 0.5, apply_to = "all") {
	// If single value, convert to [x, y, z] vector
	size = (size[0] == undef) ? [size, size, size] : size;

	translate_min = radius;
	translate_xmax = size[0] - radius;
	translate_ymax = size[1] - radius;
	translate_zmax = size[2] - radius;

	diameter = radius * 2;

	obj_translate = (center == false) ?
		[0, 0, 0] : [
			-(size[0] / 2),
			-(size[1] / 2),
			-(size[2] / 2)
		];

	translate(v = obj_translate) {
		hull() {
			for (translate_x = [translate_min, translate_xmax]) {
				x_at = (translate_x == translate_min) ? "min" : "max";
				for (translate_y = [translate_min, translate_ymax]) {
					y_at = (translate_y == translate_min) ? "min" : "max";
					for (translate_z = [translate_min, translate_zmax]) {
						z_at = (translate_z == translate_min) ? "min" : "max";

						translate(v = [translate_x, translate_y, translate_z])
						if (
							(apply_to == "all") ||
							(apply_to == "xmin" && x_at == "min") || (apply_to == "xmax" && x_at == "max") ||
							(apply_to == "ymin" && y_at == "min") || (apply_to == "ymax" && y_at == "max") ||
							(apply_to == "zmin" && z_at == "min") || (apply_to == "zmax" && z_at == "max")
						) {
							sphere(r = radius);
						} else {
							rotate = 
								(apply_to == "xmin" || apply_to == "xmax" || apply_to == "x") ? [0, 90, 0] : (
								(apply_to == "ymin" || apply_to == "ymax" || apply_to == "y") ? [90, 90, 0] :
								[0, 0, 0]
							);
							rotate(a = rotate)
							cylinder(h = diameter, r = radius, center = true);
						}
					}
				}
			}
		}
	}
}