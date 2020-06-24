include <parametric_butt_hinge_3.5.2.scad>;
//main();


/************/

d=.5;
r_top=80;
r_hole=50;
r_bottom=120;
d_bottom=30;

r_screw=3.;
r_bolt=5.;
h_screw=100;
h_bolt=3.6;
r_screw_small=1.5;

h_device=120;

w_acrylic=3;

num_sides=8;



wall=4;
d_acrylic=3;
w_segment=22;
shift_segment=3;

h_bottom=wall;
h_top=wall;

r_acrylic_bottom=110;

/********/

all();

/********/

module all(){
    
        union(){
            theta=360/num_sides;
            for (itheta=[0:num_sides]) 
                rotate([0,0,theta*itheta]){
                    all_segment();
                }
        }
}

module all_segment(){
    //projection(cut = false)  translate([0,0,-70]) rotate([-51.1,-62,0]) 
    //color([1,1,1]) base_acrylic();

    color([.5,1,.5]) support_segment();
    color([1,1,0]) base_segment();

    color([1,.5,1]) hinge_segment();
    
    
    //color([1,1,1]) top_acrylic_segment();

    //projection(cut = false) bottom_acrylic_segment();

    //
    //projection(cut = false)  translate([0,0,-74.5]) rotate([-51.1,-62,0]) 
    //color([0,1,1]) acrylic_segment();
    color([.5,.5,1]) led_segment();

}

module bottom_acrylic_segment(){

      translate([0,0,-h_bottom-4.5])   
      difference(){
        union(){
                difference(){
                    union(){
                        translate([0,0,-h_device/2-h_bottom]) cylinder(r1=r_bottom, r2=r_bottom, h=h_bottom, $fn=num_sides); //Bottom circle
                    
                    }    
                    translate([0,0,-h_device/2-10]) cylinder(r1=r_bottom-d_bottom, r2=r_bottom-d_bottom, h=40, $fn=num_sides); //Bottom circle
                    
                }
                
        }
        scale([1,1,1.001]) rotate([0,0,-360/num_sides]) translate([-h_device*2,-h_device*2,-h_device]) 
        cube([4*h_device,h_device*2,h_device*2]);
        scale([1,1,1.001]) rotate([0,0,0]) translate([-2*h_device,0,-2*h_device/2]) cube([4*h_device,2*h_device,2*h_device]);   
        
        //Screws
        rotate([0,0,-360/num_sides/2]) translate([r_bottom-22,0,-h_screw/2]) cylinder(r=r_screw, h=h_screw, center=true); //bottom
        rotate([0,0,-360/num_sides/2]) translate([r_top-17,0,h_screw/2]) cylinder(r=r_screw, h=h_screw, center=true); //top
        rotate([0,0,-360/num_sides/2]) translate([r_top-17,0,h_screw/2+h_bolt-d]) cylinder(r=r_bolt, h=h_bolt, center=true); //top
        
    }

}

module top_acrylic_segment(){
    translate([0,0,.5+5])
    difference(){
        union(){
            rotate([0,0,-22.5]) translate([-15.2,-50,h_device/2]) cube([100,200,5]);
            
                   
        }
        translate([0,0,h_device/2-wall-h_top*2]) cylinder(r1=r_hole, r2=r_hole, h=h_top*6, $fn=100); //Top hole#
       //# translate([0,0,-wall])  segment(40,d_acrylic+d,0.0);
        //pestana acrilico
        
        scale([1,1,1.001]) rotate([0,0,-360/num_sides]) translate([-h_device*2,-h_device*2,-h_device]) 
        cube([4*h_device,h_device*2,h_device*2]);
        scale([1,1,1.001]) rotate([0,0,0]) translate([-2*h_device,0,-2*h_device/2]) cube([4*h_device,2*h_device,2*h_device]);  
        translate([0,0,h_device/2-wall-h_top]) cylinder(r1=r_hole, r2=r_hole, h=h_top*4, $fn=100); //Top hole#
        rotate([0,0,-360/num_sides/2]) translate([r_top-17,0,h_screw/2]) cylinder(r=r_screw, h=h_screw, center=true); //top screw
    }
}


//#segment(44,d_acrylic,0.1);

module hinge_segment(){
    translate([0,0,.5])
    difference(){
        union(){
            rotate([0,0,-22.5]) translate([r_top,0,h_device/2])  mirror([0,0,1]) leaf ( C_MALE ); 
            rotate([0,0,-22.5]) translate([-25.2,-50,h_device/2]) cube([100,200,5]);
            
            translate([0,0,h_device/2-wall/2-h_top*1.5]) cylinder(r1=r_top-21, r2=r_top-21, h=h_top*2+wall+1, $fn=num_sides); //Top circle
                   
        }
        translate([0,0,h_device/2-wall-h_top*2]) cylinder(r1=r_hole, r2=r_hole, h=h_top*6, $fn=100); //Top hole#
       //# translate([0,0,-wall])  segment(40,d_acrylic+d,0.0);
        //pestana acrilico
                    intersection(){
                        translate([0,0,-wall]) scale([1.0,1.,1.0]) segment(41,d_acrylic+d,0.);
                        rotate([0,-15,20-360/num_sides]) translate([48+10,-8,-20]) cube([20,20,h_device]);
                    }

        
        scale([1,1,1.001]) rotate([0,0,-360/num_sides]) translate([-h_device*2,-h_device*2,-h_device]) 
        cube([4*h_device,h_device*2,h_device*2]);
        scale([1,1,1.001]) rotate([0,0,0]) translate([-2*h_device,0,-2*h_device/2]) cube([4*h_device,2*h_device,2*h_device]);  
        translate([0,0,h_device/2-wall-h_top]) cylinder(r1=r_hole, r2=r_hole, h=h_top*4, $fn=100); //Top hole#
        rotate([0,0,-360/num_sides/2]) translate([r_top-17,0,h_screw/2]) cylinder(r=r_screw, h=h_screw, center=true); //top screw
    }
}

module support_segment(){
        //mirror([0,0,1]) leaf (  C_FEMALE ); 
    
        difference(){
            segment(0,2*wall,0.0);
            
            difference(){
                scale([1.1,1.1,1.1]) segment(wall*4,wall*3,8);
            
                rotate([0,0,-360/num_sides]) translate([0,-100,-h_device/2]) cube([200,200,5]);
                rotate([0,0,-360/num_sides]) translate([0,-100,h_device/2-h_top*5+1]) cube([200,200,8]);
            }
            //#scale([1.0,1.0,1.0]) segment(-2,wall*3,8);

//            segment(2,2*wall,0);

        }
        
        
      difference(){
        union(){
                difference(){
                    union(){
                        translate([0,0,-h_device/2-h_bottom]) cylinder(r1=r_bottom, r2=r_bottom, h=h_bottom, $fn=num_sides); //Bottom circle
                    
                    }    
                    //difference(){
                        translate([-13,wall+d,-h_device/2-h_bottom-wall*2]) cylinder(r1=r_bottom-wall+.5, r2=r_bottom-wall-5.5, h=h_bottom+wall*4, $fn=num_sides); //Bottom circle
                        translate([0,0,-wall]) scale([1.0,1.,1.0]) segment(41,d_acrylic+d,0.);
                    //}
                    
                    //translate([0,0,-h_device/2-1-h_bottom*2]) cylinder(r1=r_bottom-d_bottom, r2=r_bottom-d_bottom, h=h_bottom*5, $fn=num_sides); //Bottom circle
                   // #translate([0,0,0]) scale([1.,1.,1]) segment(44,d_acrylic,0.);
                }
                difference(){
                    union(){
                        translate([0,0,h_device/2-wall/2-h_top/2]) cylinder(r1=r_top, r2=r_top, h=h_top, $fn=num_sides); //Top circle
                        translate([0,0,h_device/2-wall/2-h_top*1.5]) cylinder(r1=r_top, r2=r_top, h=h_top*2, $fn=num_sides); //Top circle
                    }
                   translate([0,0,h_device/2-wall-h_top*2]) cylinder(r1=r_hole, r2=r_hole, h=h_top*6, $fn=100); //Top hole#
                    
                    translate([0,0,h_device/2-wall/2-h_top*1.5-d]) cylinder(r1=r_top-21, r2=r_top-21, h=h_top*2+1, $fn=num_sides); //Top circle
                    //#translate([0,1,-wall])  segment(41,d_acrylic+d,0.1);
                    
                    //pestana acrilico
                    intersection(){
                        translate([0,0,-wall]) scale([1.0,1.,1.0]) segment(41,d_acrylic+d,0.);
                        rotate([0,-15,20-360/num_sides]) translate([48+10,-8,-20]) cube([20,20,h_device]);
                    }

                }
        }
        scale([1,1,1.001]) rotate([0,0,-360/num_sides]) translate([-h_device*2,-h_device*2,-h_device]) 
        cube([4*h_device,h_device*2,h_device*2]);
        scale([1,1,1.001]) rotate([0,0,0]) translate([-2*h_device,0,-2*h_device/2]) cube([4*h_device,2*h_device,2*h_device]);   
        
        //Screws
        rotate([0,0,-360/num_sides/2]) translate([r_bottom-22,0,-h_screw/2]) cylinder(r=r_screw, h=h_screw, center=true); //bottom
        rotate([0,0,-360/num_sides/2]) translate([r_bottom-22,0,-h_device/2-h_bolt/2+1]) rotate([0,0,30]) cylinder(r=r_bolt, h=h_bolt, center=true, $fn=6); //bottom
        
        rotate([0,0,-360/num_sides/2]) translate([r_top-17,0,h_screw/2]) cylinder(r=r_screw, h=h_screw, center=true); //top
        rotate([0,0,30-360/num_sides/2]) translate([r_top-17-8-1,-14-17,h_screw/2+h_bolt-d]) cylinder(r=r_bolt, h=h_bolt, center=true, $fn=6); //top
        
    }

        
        
    
}

module base_acrylic(){
    translate([-2,0,-h_bottom-.5]) {
        difference(){
            translate([0,0,0]) scale([1.,1.,1]) segment(36,d_acrylic,d_acrylic);
            
             translate([0,-200,56]) cube([4*h_device,h_device*2,h_device*2]);
            
             
        }
        //pestana acrilico
                    #intersection(){
                        translate([0,0,0]) scale([1.0,1.,1.0]) segment(36,d_acrylic,0);
                        rotate([0,-15,20-360/num_sides]) translate([48+10,-8,-20]) cube([20,20,h_device]);
                    }
               }
        
}

module base_segment(){
    
      translate([0,0,-h_bottom-.5])   
      difference(){
        union(){
                difference(){
                    union(){
                        translate([0,0,-h_device/2-h_bottom]) cylinder(r1=r_bottom, r2=r_bottom, h=h_bottom, $fn=num_sides); //Bottom circle
                       translate([-17,wall,-h_device/2-h_bottom+wall]) cylinder(r1=r_bottom-wall, r2=r_bottom-wall-2, h=h_bottom+wall*3, $fn=num_sides); //Bottom circle
                    
                    }    
                    translate([0,0,-h_device/2-10]) cylinder(r1=r_bottom-d_bottom, r2=r_bottom-d_bottom, h=40, $fn=num_sides); //Bottom circle
                    
                    translate([0,0,0]) scale([1.,1.,1]) segment(36,d_acrylic*2,0.);
                }
                
        }
        scale([1,1,1.001]) rotate([0,0,-360/num_sides]) translate([-h_device*2,-h_device*2,-h_device]) 
        cube([4*h_device,h_device*2,h_device*2]);
        scale([1,1,1.001]) rotate([0,0,0]) translate([-2*h_device,0,-2*h_device/2]) cube([4*h_device,2*h_device,2*h_device]);   
        
        //Screws
        rotate([0,0,-360/num_sides/2]) translate([r_bottom-22,0,-h_screw/2]) cylinder(r=r_screw, h=h_screw, center=true); //bottom
        rotate([0,0,-360/num_sides/2]) translate([r_top-17,0,h_screw/2]) cylinder(r=r_screw, h=h_screw, center=true); //top
        rotate([0,0,-360/num_sides/2]) translate([r_top-17,0,h_screw/2+h_bolt-d]) cylinder(r=r_bolt, h=h_bolt, center=true); //top
        
    }

        
        
    
}


module acrylic_segment(){

difference(){

        difference(){
            segment(25,w_acrylic,10.51);
            
           
            
        }
                     
             rotate([0,88,-22.5]) translate([r_top-114+r_screw_small,17,h_device/2]) cylinder(r=r_screw_small*1.5, h=h_bolt*5, $fn=100);  //acrylic screw
             rotate([0,88,-22.5]) translate([r_top-114+r_screw_small,-17,h_device/2]) cylinder(r=r_screw_small*1.5, h=h_bolt*5, $fn=100); //acrylic screw
             rotate([0,88,-22.5]) translate([r_top-35+r_screw_small,0,22+h_device/2]) cylinder(r=r_screw_small*1.5, h=h_bolt*5, $fn=100); //acrylic screw
    }
    //#segment(0,14,margin_segment);
    
}

module led_segment(){

    difference(){
        difference(){
            union(){
                rotate([0,73,-22.5]) translate([r_top-114,0,34+h_device/2])  mirror([0,0,1]) leaf (  C_FEMALE ); 
                rotate([0,0,0]) segment(-24.5,6,4);
                segment(shift_segment-22.5,w_segment,10.5);
                intersection(){
                    segment(shift_segment-22.5+wall,2*wall,4);
                    rotate([0,0,-360/num_sides-15]) translate([0,0,-h_device/2-1]) cube([200,200,12]);
                }
            }
            
            difference(){
                segment(-19,w_segment,12.5);
                
                intersection(){
                     union(){
                        rotate([0,88,-22.5]) translate([r_top-114-2,12,10+h_device/2]) cube([r_bolt*2, r_bolt*2,30]); 
                        rotate([0,88,-22.5]) translate([r_top-114-2,-22,10+h_device/2]) cube([r_bolt*2, r_bolt*2,30]);
                        rotate([0,88,-22.5]) translate([r_top-37,-r_bolt,30+h_device/2]) cube([r_bolt*2, r_bolt*2,30]);
                     }
                     segment(-19,w_segment,12.5);
                 }

                
            }
            rotate([0,-15,-22.5]) translate([80,-0,0]) cube([10,10,100],center=true);
                         
                 rotate([0,88,-22.5]) translate([r_top-114+r_screw_small,17,11+h_device/2]) cylinder(r=r_screw_small, h=h_bolt*2, $fn=30);  //acrylic screw
                 rotate([0,88,-22.5]) translate([r_top-114+r_screw_small,-17,11+h_device/2]) cylinder(r=r_screw_small, h=h_bolt*2, $fn=30); //acrylic screw
                 rotate([0,88,-22.5]) translate([r_top-35+r_screw_small,0,32+h_device/2]) cylinder(r=r_screw_small, h=h_bolt*2, $fn=30); //acrylic screw
        }
        //#segment(0,14,margin_segment);
        
    }
}




/*
module all(){
    
        union(){
            theta=360/num_sides;
            for (itheta=[0:num_sides]) 
                rotate([0,0,theta*itheta]){
                    segment();
                }
        }
}
*/

module segment(shift_segment, wall, margin_segment){
    rotate([0,0,0])
    difference(){
        cylinder(h_device, r_bottom-shift_segment/2, r_top-shift_segment/2,$fn=num_sides, center=true);
        scale([1,1,1.001]) translate([0,0,0]) cylinder(h_device, r_bottom-wall-shift_segment/2, r_top-wall-shift_segment/2,$fn=num_sides, center=true);
        //cylinder(h_device, r_bottom, r_top,$fn=num_sides, center=true);
        
        
        scale([1,1,1.001]) rotate([0,0,-margin_segment/2]) translate([-h_device,0,-h_device/2]) cube([2*h_device,h_device,h_device]);
        scale([1,1,1.001]) rotate([0,0,-360/num_sides+margin_segment/4]) translate([-h_device,0,-h_device/2+h_device-margin_segment*2]) cube([2*h_device,h_device,h_device]);
        scale([1,1,1.001]) rotate([0,0,-360/num_sides+margin_segment/4]) translate([-h_device,-100,-h_device*3/2+margin_segment]) cube([3*h_device,h_device*2,h_device]);
        
        
        scale([1,1,1.001]) rotate([0,0,-360/num_sides+margin_segment/2]) translate([-h_device*2,-h_device*2,-h_device]) 
        cube([4*h_device,h_device*2,h_device*2]);
        scale([1,1,1.001]) rotate([0,0,-margin_segment/2]) translate([-2*h_device,0,-2*h_device/2]) cube([4*h_device,2*h_device,2*h_device]);
        
        
        cylinder(2*h_device, r_hole, r_hole,$fn=100, center=true);
    }
}

/*
difference(){
    cylinder(h_device, r_bottom, r_top,$fn=num_sides, center=true);
    cylinder(2*h_device, r_hole, r_hole,$fn=100, center=true);
}
*/