d=0.02;
r_tube=6;

h_tube=17;

w_holder=35;
wall_space=3;

wall=4;
w_screw=r_tube*2+wall;
r_screw=2.5;

difference(){
    union(){
        cylinder(r=r_tube+wall, h=h_tube, $fn=100, center=true);
        translate([r_tube+w_holder/2,0,0]) cube([w_holder,wall,h_tube], center=true);
        translate([-w_screw,wall/2,0]) cube([w_screw,r_tube,h_tube], center=true);
        translate([-w_screw,-wall/2,0]) cube([w_screw,r_tube,h_tube], center=true);
    }
    
    translate([0,0,0]) cylinder(r=r_tube, h=h_tube+2, $fn=100, center=true);
    translate([-w_holder/2,0,0]) cube([w_holder, wall_space,h_tube+2], center=true);
    
   translate([-r_tube-w_holder/2+wall,0,0]) rotate([90,0,0]) cylinder(r=r_screw, h=h_tube, center=true, $fn=100);
    translate([r_tube+w_holder/2-wall,0,0]) rotate([90,0,0]) cylinder(r=r_screw, h=h_tube, center=true, $fn=100);
}