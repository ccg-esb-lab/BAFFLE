r_screw=4;

w_fan=79;
d_fan=79;
h_fan=15;

w_sink=76;
d_sink=68;
h_sink=44;

d=0.01;
wall=5;


r_base=8;
h_base=wall;


d_screw=72;
//
/*
h_support=h_fan+2*wall;
r_fan=w_fan/2;
difference(){
    translate([0, 0, h_support/2]) cube([w_fan+wall*2, d_fan+wall*2, h_support], center=true);
    
    cylinder(h=w_fan*2, r=r_fan, $fn=100, center=true);
    translate([0,-35+wall,wall*1.5+h_fan/2+d]) cube([w_fan*2, d_fan/4, h_fan+wall], center=true);
    translate([0,35-wall,wall*1.5+h_fan/2+d]) cube([w_fan*2, d_fan/4, h_fan+wall], center=true);
    //translate([-d_fan/2,0,wall*1.5+h_fan/2+d]) cube([w_fan/1.25, d_fan*2, h_fan+wall], center=true);
    
    translate([0,-35,wall*1.5+h_fan/2+d+wall]) cube([w_fan*2, d_fan/4, h_fan+wall], center=true);
    translate([0,35,wall*1.5+h_fan/2+d+wall]) cube([w_fan*2, d_fan/4, h_fan+wall], center=true);
    
    translate([105,-35,wall*1.5+h_fan/2+d]) cube([w_fan*2, d_fan/4, h_fan+wall], center=true);
    translate([105,35,wall*1.5+h_fan/2+d]) cube([w_fan*2, d_fan/4, h_fan+wall], center=true);
        
    translate([-105,-35,wall*1.5+h_fan/2+d]) cube([w_fan*2, d_fan/4, h_fan+wall], center=true);
    translate([-105,35,wall*1.5+h_fan/2+d]) cube([w_fan*2, d_fan/4, h_fan+wall], center=true);
    
   translate([0, 0, h_sink/2+wall]) cube([w_sink, d_sink, h_sink], center=true);
    
    translate([-d_screw/2, d_screw/2,  2]) cylinder(h=h_fan, r=r_screw, $fn=100, center=true);
    translate([d_screw/2, d_screw/2,  2]) cylinder(h=h_fan, r=r_screw, $fn=100, center=true);
    translate([d_screw/2, -d_screw/2,  2]) cylinder(h=h_fan, r=r_screw, $fn=100, center=true);
    translate([-d_screw/2, -d_screw/2, 2]) cylinder(h=h_fan, r=r_screw, $fn=100, center=true);
}
*/


//#translate([0, 0, -h_fan/2+d-wall/2]) cube([w_fan, d_fan, h_fan+wall], center=true);

/*
projection(cut = false) difference(){
    union(){
        translate([-d_screw/2, d_screw/2, -h_fan-wall*1.5]) cylinder(r=r_base, h=h_base, $fn=100, center=true);
        //translate([-d_screw/2, -d_screw/2, -h_fan-wall*1.5]) cylinder(r=r_base, h=h_base, $fn=100, center=true);
        //translate([d_screw/2, d_screw/2, -h_fan-wall*1.5]) cylinder(r=r_base, h=h_base, $fn=100, center=true);
        //translate([d_screw/2, -d_screw/2, -h_fan-wall*1.5]) cylinder(r=r_base, h=h_base, $fn=100, center=true);
    }
    translate([-d_screw/2, d_screw/2,  -h_fan*1.5]) cylinder(h=h_fan, r=r_screw, $fn=100, center=true);
    //translate([d_screw/2, d_screw/2,  -h_fan*1.5]) cylinder(h=h_fan, r=r_screw, $fn=100, center=true);
    //translate([d_screw/2, -d_screw/2,  -h_fan*1.5]) cylinder(h=h_fan, r=r_screw, $fn=100, center=true);
    //translate([-d_screw/2, -d_screw/2, -h_fan*1.5]) cylinder(h=h_fan, r=r_screw, $fn=100, center=true);
    
}
*/

//projection(cut = false) 
difference(){
cylinder(r=3.2, h=17, $fn=100, center=true);
cylinder(r=2.1, h=18, $fn=100, center=true);
    
}
