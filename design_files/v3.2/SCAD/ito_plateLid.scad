
d=0.2;
wall_thickness=2.5;

diameter_plate=88;
height_plate=15;

diameter_lid=90;

size_ito=100;
height_ito=10;

glass_thickness=1;

r_screw=1.8;
r_bolt=5;

w_ring=8;
w_caiman=6;
h_caiman=13;
dist_caiman=26;


acrylic_thickness=3;
/*******************/

//translate([0,0,height_plate/2-wall_thickness/2+acrylic_thickness]) color([1,1,1]) plate_bottom();
//translate([0,0,height_plate+wall_thickness/2+d]) color([1,1,0]) plate_lid();

projection(cut = false) translate([0,0,height_plate+acrylic_thickness+wall_thickness+d]) color([0,1,1]) ito_glass_bottom();
//translate([0,0,height_plate+acrylic_thickness+wall_thickness*2+d*2]) color([1,1,1,.25]) ito_glass();
//projection(cut = false) translate([0,0,height_plate+wall_thickness*2+d*5+5]) color([0,0,1]) ito_glass_top();


/*******************/
//Ito glass


module ito_glass(){
    
    rotate([0,0,45]) translate([0,0,0]) square([size_ito,size_ito], center=true);
                
}

module ito_glass_bottom(){
    
    difference(){
        union(){
           // translate([0,0,0]) cube([size_ito,size_ito, acrylic_thickness], center=true);
            translate([0,0,0]) cylinder(r=(diameter_plate+wall_thickness*2)/2+w_ring, h=acrylic_thickness, center=true, $fn=100);
        }
        //translate([0,0,wall_thickness]) cylinder(r=diameter_plate/2-wall_thickness/2, h=height_plate, center=true, $fn=100);
        
         //Spacing for connection to ito glass
        
         translate([dist_caiman/2-w_caiman/2,diameter_lid/2+w_ring-h_caiman+wall_thickness,-wall_thickness]) cube([w_caiman,h_caiman,wall_thickness*2]);
         translate([-dist_caiman/2-w_caiman/2,-diameter_lid/2-w_ring-wall_thickness,-wall_thickness]) cube([w_caiman,h_caiman,wall_thickness*2]);
        
        
         translate([-dist_caiman/2-w_caiman/2,diameter_lid/2+w_ring-h_caiman+wall_thickness,-wall_thickness]) cube([w_caiman,h_caiman,wall_thickness*2]);
         translate([dist_caiman/2-w_caiman/2,-diameter_lid/2-w_ring-wall_thickness,-wall_thickness]) cube([w_caiman,h_caiman,wall_thickness*2]);
           
        
            //Screws
                        translate([diameter_lid/2+w_ring/2+r_screw,0,-wall_thickness]) cylinder(r=r_screw, h=wall_thickness*2, $fn=100);
            translate([-diameter_lid/2-w_ring/2-r_screw,0,-wall_thickness]) cylinder(r=r_screw, h=wall_thickness*2, $fn=100);
            rotate([0,0,90]) translate([diameter_lid/2+w_ring/2+r_screw,0,-wall_thickness]) cylinder(r=r_screw, h=wall_thickness*2, $fn=100);
            rotate([0,0,90]) translate([-diameter_lid/2-w_ring/2-r_screw,0,-wall_thickness]) cylinder(r=r_screw, h=wall_thickness*2, $fn=100);
    }
                
}


module ito_glass_top(){
    
    difference(){
        union(){
           // translate([0,0,0]) cube([size_ito,size_ito, acrylic_thickness], center=true);
            translate([0,0,0]) cylinder(r=(diameter_plate+wall_thickness*2)/2+w_ring, h=acrylic_thickness, center=true, $fn=100);
        }
        
         //Spacing for connection to ito glass
         translate([-size_ito+d,diameter_lid/2+w_ring-h_caiman+wall_thickness*1.5,-wall_thickness]) cube([size_ito*2,h_caiman,wall_thickness*2]);
         translate([-size_ito+d,-diameter_lid/2-w_ring-wall_thickness*1.5,-wall_thickness]) cube([size_ito*2+d,h_caiman,wall_thickness*4]);
           
        
            translate([diameter_lid/2+w_ring/2+r_screw,0,-wall_thickness]) cylinder(r=r_screw, h=wall_thickness*2, $fn=100);
            translate([-diameter_lid/2-w_ring/2-r_screw,0,-wall_thickness]) cylinder(r=r_screw, h=wall_thickness*2, $fn=100);
            rotate([0,0,90]) translate([diameter_lid/2+w_ring/2+r_screw,0,-wall_thickness]) cylinder(r=r_screw, h=wall_thickness*2, $fn=100);
            rotate([0,0,90]) translate([-diameter_lid/2-w_ring/2-r_screw,0,-wall_thickness]) cylinder(r=r_screw, h=wall_thickness*2, $fn=100);
    }
                
}

/*******************/
//Plate 
module plate_lid(){
        rotate([0,0,0]){ 
        difference(){
            union(){
                //translate([0,0,0]) cube([size_ito,size_ito, wall_thickness], center=true);
                translate([0,0,-height_ito/2+wall_thickness]) cylinder(r1=(diameter_lid+wall_thickness*2)/2+2, r2=(diameter_lid+wall_thickness*2)/2, h=height_ito-wall_thickness, center=true, $fn=100);
                
                translate([0,0,-height_ito/2+wall_thickness]) cylinder(r1=(diameter_lid+wall_thickness)/2, r2=(diameter_lid+wall_thickness)/2, h=height_ito-wall_thickness, center=true, $fn=100);
                difference(){
                    translate([0,0,0]) cylinder(r=(diameter_plate+wall_thickness*2)/2+w_ring, h=wall_thickness, center=true, $fn=100);
                    
                    //Caiman
            
                 translate([dist_caiman/2-w_caiman/2,diameter_lid/2+w_ring-h_caiman+wall_thickness,-wall_thickness/2-d]) cube([w_caiman,h_caiman,wall_thickness*2]);
                 translate([-dist_caiman/2-w_caiman/2,-diameter_lid/2-w_ring-wall_thickness,-wall_thickness/2-d]) cube([w_caiman,h_caiman,wall_thickness*2]);
                translate([-dist_caiman/2-w_caiman/2,diameter_lid/2+w_ring-h_caiman+wall_thickness,-wall_thickness/2-d]) cube([w_caiman,h_caiman,wall_thickness*2]);
                 translate([dist_caiman/2-w_caiman/2,-diameter_lid/2-w_ring-wall_thickness,-wall_thickness/2-d]) cube([w_caiman,h_caiman,wall_thickness*2]);
                }
            }
                     translate([0,0,0]) cylinder(r=(diameter_plate+wall_thickness)/2+d*2-wall_thickness, h=height_ito, center=true, $fn=100);
           
                translate([0,0,-height_ito/2-wall_thickness/2]) cylinder(r2=(diameter_plate)/2+d*2, r1=(diameter_plate)/2+d*2+2, h=height_ito, center=true, $fn=100);
            translate([0,0,-height_ito/2-wall_thickness/2]) cylinder(r=(diameter_plate+wall_thickness)/2+d*2, h=height_ito, center=true, $fn=100);
            
           
            //Screws
            translate([diameter_lid/2+w_ring/2+r_screw,0,-wall_thickness]) cylinder(r=r_screw, h=wall_thickness*2, $fn=100);
            translate([-diameter_lid/2-w_ring/2-r_screw,0,-wall_thickness]) cylinder(r=r_screw, h=wall_thickness*2, $fn=100);
            rotate([0,0,90]) translate([diameter_lid/2+w_ring/2+r_screw,0,-wall_thickness]) cylinder(r=r_screw, h=wall_thickness*2, $fn=100);
            rotate([0,0,90]) translate([-diameter_lid/2-w_ring/2-r_screw,0,-wall_thickness]) cylinder(r=r_screw, h=wall_thickness*2, $fn=100);
            
            translate([diameter_lid/2+w_ring/2+r_screw,0,-wall_thickness*4-1-d]) cylinder(r=r_bolt, h=wall_thickness*4, $fn=100);
            translate([-diameter_lid/2-w_ring/2-r_screw,0,-wall_thickness*4-1-d]) cylinder(r=r_bolt, h=wall_thickness*4, $fn=100);
            rotate([0,0,90]) translate([diameter_lid/2+w_ring/2+r_screw,0,-wall_thickness*4-1-d]) cylinder(r=r_bolt, h=wall_thickness*4, $fn=100);
            rotate([0,0,90]) translate([-diameter_lid/2-w_ring/2-r_screw,0,-wall_thickness*4-1-d]) cylinder(r=r_bolt, h=wall_thickness*4, $fn=100);
            
            
        }
      
 
     }
}
/*******************/
//Plate 
module plate_bottom(){
    difference(){
        cylinder(r=(diameter_plate+wall_thickness)/2, h=height_plate+wall_thickness, center=true, $fn=100);
        translate([0,0,wall_thickness]) cylinder(r=diameter_plate/2, h=height_plate, center=true, $fn=100);
        
    }
}

