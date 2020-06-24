

d=0.25;

r_screw=2.5;

wall=2.5;
acrylic=4;

h_tube=25;
r_out=60; 
r_in=40;
r_acrylic=45;

intersection(){
    rotate([0,0,90]) box();
    translate([-500,0,-500]) cube([1000, 1000,1000]);
}

module box(){
    difference(){
        translate([0, 0, acrylic]) cylinder(h=h_tube+acrylic+wall, r=r_out, center=true, $fn=6);
        
        translate([0,0,h_tube/2+wall]) cylinder(h=h_tube*2, r=r_in, center=true, $fn=200);
        translate([0,0,wall]) cylinder(h=h_tube-wall, r1=r_in+(r_out-r_in)/2, r2=r_in, center=true, $fn=200);
        
        //Acrylic
        translate([0,0, h_tube/2+wall/2+acrylic+d]) cylinder(h=acrylic+d, r=r_acrylic+d, center=true, $fn=200);
        
        #cylinder(h=h_tube*2, r=r_screw, center=true);
    }
}
