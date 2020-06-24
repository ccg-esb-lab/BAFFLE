

d=0.25;

r_screws=2.5;


wall=3;
acrylic=4;

nsides=8;

h_lid=10;
h_tube=25;
r_out=60; 
r_in=40;
r_acrylic=45;


        d_screws=r_out-r_screws-wall*2;
        r_bolt=4;
        h_bolt=3;
        

/*************/
//color([0,0,0]) translate([0,0,-h_tube/2-acrylic]) import("/Users/ESB/SYNC_RPM/RPM_Work/BAFFLE/design_files/v3.2/STL/baffle_incubator_acrylic_top.stl");

//intersection(){
    union(){
        color([0, .75,  0])translate([0,0,h_tube/2+acrylic+wall*2]) rotate([0,0,45/2]) lid();
    
        color([.75, 0, 0]) rotate([0,0,45/2]) box();
    }
    //translate([-500,0,-500]) cube([1000, 1000,1000]);
//}

/*******************/
/*******************/
module lid(){
    
    //intersect(){
        
        
        difference(){
            union(){
                translate([0, 0, 0]) cylinder(h=wall, r=r_out, center=true, $fn=nsides);
                
                translate([0,0,h_lid/2-wall/2]) cylinder(h=h_lid, r=r_in+wall, center=true, $fn=200);
            }
            
            translate([0,0,h_tube/2+wall]) cylinder(h=h_tube*2, r=r_in, center=true, $fn=200);
              
            for ( iscrew = [0 : nsides ]){
                        theta=iscrew*360/nsides;
                        rotate([0,0,theta])  translate([0,d_screws,h_lid]) cylinder(r=r_screws, h=50, center=true, $fn=100); //Screws
                       rotate([0,0,theta])  translate([0,d_screws,h_bolt/2]) cylinder(r=r_bolt, h=h_bolt, center=true, $fn=100); //Bolt
             }
        }
   // }
}



module box(){
     difference(){
        union(){
            
            difference(){
                translate([0, 0, -h_tube/2+wall*2+1]) cylinder(h=h_tube/2, r=r_out, center=true, $fn=nsides);
                translate([0,0,-h_tube/2/2+wall]) cylinder(h=h_tube/2, r=r_acrylic+wall, center=true, $fn=200);
                
            }
            
            
            difference(){
                translate([0, 0, acrylic]) cylinder(h=h_tube+acrylic+wall, r=r_out, center=true, $fn=nsides);
                
                translate([0,0,h_tube/2+wall]) cylinder(h=h_tube*2, r=r_in, center=true, $fn=200);
                translate([0,0,wall]) cylinder(h=h_tube-wall, r1=r_in+(r_out-r_in)/2, r2=r_in, center=true, $fn=200);
                
                //Acrylic
                translate([0,0, h_tube/2+wall/2+acrylic+d]) cylinder(h=acrylic+d, r=r_acrylic+d, center=true, $fn=200);
                

            }
        }
                for ( iscrew = [0 : nsides ]){
                    theta=iscrew*360/nsides;
                    rotate([0,0,theta])  translate([0,d_screws,10]) cylinder(r=r_screws, h=50, center=true, $fn=100); //Screws
                    rotate([0,0,theta])  translate([0,d_screws,-h_tube/2+h_bolt/2]) cylinder(r=r_bolt, h=h_bolt, center=true, $fn=6); //Bolt
                }
                //Cables
                rotate([0,0,-45/2]) translate([r_out/2,-wall,-h_tube/2+wall*2]) cube([r_out, wall*2, wall]);
    }
}
