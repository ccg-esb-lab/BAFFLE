
d=0.02;
w_box=220;
h_box=80;

w_beam=20;
h_beam=20;

w_post=25;
h_post=h_box;

r_screw = 2.5;
r_screw_large=3.5;
r_bolt = 5.;
h_bolt = 5;

thick=5;
w_acrylic=5;

            dist_grid=5;
            r_plate=100;
            spacing_leds=10;

//Box
//translate([0,0,-h_box/2]) cube([w_box-d, w_box-d, h_box-d], center=true);
/**********/

//translate([0,0,75]) rotate([0,0,22.5]) import("illuminator_all.stl");

//frame_openBuilds();

//post_frontRight();
//post_frontLeft();
//post_backRight();
//post_backLeft();

/*
color([1,1,1]){
acrylic_right();
}

acrylic_back();
acrylic_right();
acrylic_bottom();
acrylic_left();
acrylic_front();
acrylic_top();
*/

acrylic_top();

//projection(cut = false) 
//acrylic_bottom();

//acrylic_top();
//projection(cut = false) rotate([90,0,0]) acrylic_left();


module thermostat_screws(){
    //difference(){
    //    cube([40,48.5,1], center=true);
        
        dy_screw=40.5;
        dx_screw=32;
        translate([-dx_screw/2,-dy_screw/2,0]) cylinder(r=r_screw, h=h_box, center=true, $fn=100);
        translate([dx_screw/2,-dy_screw/2,0]) cylinder(r=r_screw, h=h_box, center=true, $fn=100);
        translate([-dx_screw/2,dy_screw/2,0]) cylinder(r=r_screw, h=h_box, center=true, $fn=100);
        translate([dx_screw/2,dy_screw/2,0]) cylinder(r=r_screw, h=h_box, center=true, $fn=100);
        
        translate([-3,0,0]) cylinder(r=r_screw, h=h_box, center=true, $fn=100);
        translate([-3,-10,0]) cylinder(r=r_screw, h=h_box, center=true, $fn=100);
        translate([-3,10,0]) cylinder(r=r_screw, h=h_box, center=true, $fn=100);
        
        
        //translate([-10,0,0]) cube([10,22.8,h_box], center=true);
    //}
}

              

/**********/

        //translate([-w_box/2+w_beam/2,-w_box/2+w_beam*1.5,0]) import("20x20_sideplate.stl");
        

module acrylic_bottom(){
    difference(){
        union(){
            translate([w_acrylic*.5,0,-h_box-w_acrylic/2]) cube([w_box+w_acrylic,w_box+w_acrylic*2,w_acrylic], center=true);
            
        }
        
        //screws
        box_screws();
        
    }
}



module acrylic_top(){
    difference(){
        union(){
            translate([w_acrylic*.5-w_beam/2,0,w_acrylic/2]) cube([w_box+w_beam+w_acrylic,w_box+2*w_acrylic,w_acrylic], center=true);
            
        }
        
        //screws
        translate([w_box/2-w_beam/2, -w_box/2+w_beam/2,0]) cylinder(r=r_screw_large, h=h_box, center=true, $fn=100);
        translate([w_box/2-w_beam/2, w_box/2-w_beam/2,0]) cylinder(r=r_screw_large, h=h_box, center=true, $fn=100);
        //translate([-w_box/2+w_beam*3-r_screw_large/2, -w_box/2+w_beam/2,0]) cylinder(r=r_screw_large, h=h_box, center=true, $fn=100);
        //translate([-w_box/2+w_beam*3-r_screw_large/2, w_box/2-w_beam/2,0]) cylinder(r=r_screw_large, h=h_box, center=true, $fn=100);
        translate([-w_box/2-w_beam/2, 0,0]) cylinder(r=r_screw_large, h=h_box, center=true, $fn=100);
        
          theta=360/8;
                dist_screw=98;
                for (itheta=[0:8]) 
                    rotate([0,0,theta/2+22.5+theta*itheta]) translate([dist_screw,0,0]) cylinder(r=r_bolt,h=h_box,$fn=100, center=true);
                
                //for (itheta=[0:8]) 
                //    rotate([0,0,22.5+theta*itheta]) translate([106,0,0]) cylinder(r=r_screw,h=h_box,$fn=100, center=true);

        
        
        intersection(){
            translate([-w_box/2-w_beam,-w_box/2-10,-d]) cube([60,70,w_acrylic+2*d]);
            union(){
                translate([-w_box/2-w_beam,-w_box/2,-w_acrylic/2]) rotate([0,0,45])  cube([57,120,w_acrylic*2]);
                translate([-w_box/2-w_beam,-w_box/2,-w_acrylic/2]) rotate([0,0,45])  mirror([0,1,0]) cube([57,120,w_acrylic*2]);
                translate([-w_box/2-w_beam-10,-w_box/2,-w_acrylic/2]) rotate([0,0,45])  mirror([0,1,0]) cube([57,120,w_acrylic*2]);
            }
        }
        
        mirror([0,1,0]){
            intersection(){
                translate([-w_box/2-w_beam,-w_box/2-10,-d]) cube([60,70,w_acrylic+2*d]);
                union(){
                    translate([-w_box/2-w_beam,-w_box/2,-w_acrylic/2]) rotate([0,0,45])  cube([57,120,w_acrylic*2]);
                    translate([-w_box/2-w_beam,-w_box/2,-w_acrylic/2]) rotate([0,0,45])  mirror([0,1,0]) cube([57,120,w_acrylic*2]);
                    translate([-w_box/2-w_beam-10,-w_box/2,-w_acrylic/2]) rotate([0,0,45])  mirror([0,1,0]) cube([57,120,w_acrylic*2]);
                }
            }
        }
        
     
         //Screws   
            //for (theta=[0,60,120,180,240,300]){
            //    rotate([0,0,theta]) translate([-thick_bottom/2+r_bottom-thick_device/2,-0,-thick_acrylic/2+d])   cylinder(r=r_screw,h=thick_acrylic*2,$fn=100, center=true);
            //}

            for (igrid=[0:3]){
                difference(){
                    
                    rout=r_plate-spacing_leds-igrid*(dist_grid+thick);
                    rin=r_plate-spacing_leds-igrid*(dist_grid+thick)-thick;
                    
                    translate([0,0,0]) rotate([0,0,22.5]) cylinder(thick*4, rout, rout, $fn=8, center=true);
                    translate([0,0,0]) rotate([0,0,22.5]) cylinder(thick*4, rin, rin, $fn=8, center=true);
                    
                }
                
            }
            
            

        }
        
                theta=360/16;
                for (itheta=[0:16]) 
                    translate([0,0,w_acrylic/2]) rotate([0,0,22.5+theta*itheta]) cube([thick,r_plate*1.9-thick,w_acrylic], center=true);
}

module acrylic_left(){
    difference(){
        #translate([0,-w_box/2-w_acrylic/2,-h_box/2]) cube([w_box, w_acrylic, h_box], center=true);
        
        box_screws();
    }
}

module acrylic_right(){
    difference(){
        #translate([0,w_box/2+w_acrylic/2,-h_box/2]) cube([w_box, w_acrylic, h_box], center=true);
        
        box_screws();
    }
}

module acrylic_front(){
    
    difference(){
        #translate([w_box/2+w_acrylic/2,0,-h_box/2]) rotate([0,0,90]) cube([w_box+2*w_acrylic, w_acrylic, h_box], center=true);
        
        box_screws();
     
        translate([w_box/2,0,-30]) rotate([0,90,0]) thermostat_screws();   
    }
}

module acrylic_back(){
    difference(){
        #translate([-w_box/2+w_acrylic/2,0,-h_box/2]) rotate([0,0,90]) cube([w_box, w_acrylic, h_box], center=true);
        
        translate([0,w_box/2-w_beam/2,-h_beam/2]) cube([2*w_box+d, w_beam+d, h_beam+d], center=true);  
        translate([0,-w_box/2+w_beam/2,-h_beam/2]) cube([2*w_box+d, w_beam+d, h_beam+d], center=true);  
            
        box_screws();
        
    }
}

module box_screws(){
            translate([-w_box/2+w_post*1.5+w_acrylic, -w_box/2+w_beam/2,0]) cylinder(r=r_screw_large, h=h_box, center=true, $fn=100);
            translate([-w_box/2+w_post/2+w_acrylic, -w_box/2+w_post/2,-w_beam/2]) rotate([90,0,0]) cylinder(r=r_screw_large, h=h_box, center=true, $fn=100);
            translate([-w_box/2+w_post*1.5+w_acrylic, -w_box/2+w_post/2,-w_beam/2]) rotate([90,0,0]) cylinder(r=r_screw_large, h=h_box, center=true, $fn=100);
            translate([-w_box/2, -w_box/2+w_post/2+w_beam+w_acrylic,-w_beam/2]) rotate([90,0,90]) cylinder(r=r_screw_large, h=h_box, center=true, $fn=100);
            translate([-w_box/2+w_post/2, -w_box/2+w_post+thick/2+thick,-w_beam*1.5]) rotate([90,0,90]) cylinder(r=r_screw_large, h=h_box, center=true, $fn=100);
            translate([-w_box/2+w_acrylic+w_beam/2+thick, -w_box/2+w_post/2-r_screw/2+thick,-h_box]) cylinder(r=r_screw, h=h_box, center=true, $fn=100);
            translate([-w_box/2+w_post/2+w_acrylic*1.5, -w_box/2+w_post/2,r_screw/2+w_beam-h_box]) rotate([90,0,0]) cylinder(r=r_screw, h=h_box, center=true, $fn=100);
            translate([-w_box/2+w_post/2, -w_box/2+w_post/2+thick/2,r_screw/2+w_beam/2-h_box]) rotate([90,0,90]) cylinder(r=r_screw, h=h_box, center=true, $fn=100);
    
             translate([-w_box/2+w_post*1.5+w_acrylic, w_box/2-w_beam/2,0]) cylinder(r=r_screw_large, h=h_box, center=true, $fn=100);
            translate([-w_box/2+w_post/2+w_acrylic, w_box/2-w_post/2,-w_beam/2]) rotate([90,0,0]) cylinder(r=r_screw_large, h=h_box, center=true, $fn=100);
            translate([-w_box/2+w_post*1.5+w_acrylic, w_box/2-w_post/2,-w_beam/2]) rotate([90,0,0]) cylinder(r=r_screw_large, h=h_box, center=true, $fn=100);
            translate([-w_box/2, w_box/2-w_post/2-w_beam-w_acrylic,-w_beam/2]) rotate([90,0,90]) cylinder(r=r_screw_large, h=h_box, center=true, $fn=100);
            translate([-w_box/2+w_post/2, w_box/2-w_post-thick/2-thick,-w_beam*1.5]) rotate([90,0,90]) cylinder(r=r_screw_large, h=h_box, center=true, $fn=100);
            translate([-w_box/2+w_acrylic+w_beam/2+thick, w_box/2-w_post/2+r_screw/2-thick,-h_box]) cylinder(r=r_screw, h=h_box, center=true, $fn=100);
            translate([-w_box/2+w_post/2+w_acrylic*1.5, w_box/2-w_post/2,r_screw/2+w_beam-h_box]) rotate([90,0,0]) cylinder(r=r_screw, h=h_box, center=true, $fn=100);
            translate([-w_box/2+w_post/2, w_box/2-w_post/2-thick/2,r_screw/2+w_beam/2-h_box]) rotate([90,0,90]) cylinder(r=r_screw, h=h_box, center=true, $fn=100);
            
        translate([w_box/2-w_post*1.5, -w_box/2+w_beam/2,0]) cylinder(r=r_screw_large, h=h_box, center=true, $fn=100);
        translate([w_box/2-w_post/2, -w_box/2+w_post/2,-w_beam/2]) rotate([90,0,0]) cylinder(r=r_screw_large, h=h_box, center=true, $fn=100);
        translate([w_box/2-w_post*1.5, -w_box/2+w_post/2,-w_beam/2]) rotate([90,0,0]) cylinder(r=r_screw_large, h=h_box, center=true, $fn=100);
        
        translate([w_box/2-w_post*1.5, -w_box/2+w_post/2-r_screw/2,-h_box]) cylinder(r=r_screw, h=h_box, center=true, $fn=100);
        translate([w_box/2-w_post/2, -w_box/2+w_post/2,r_screw/2+w_beam-h_box]) rotate([90,0,0]) cylinder(r=r_screw, h=h_box, center=true, $fn=100);
        translate([w_box/2-w_post/2, -w_box/2+w_post/2,r_screw/2+w_beam/2-h_box]) rotate([90,0,90]) cylinder(r=r_screw, h=h_box, center=true, $fn=100);
        translate([w_box/2-w_post/2, -w_box/2+w_post/2,-r_screw/2-w_beam*1.5]) rotate([90,0,90]) cylinder(r=r_screw, h=h_box, center=true, $fn=100);
 
 
        translate([w_box/2-w_post*1.5, w_box/2-w_beam/2,0]) cylinder(r=r_screw_large, h=h_box, center=true, $fn=100);
        translate([w_box/2-w_post/2, w_box/2-w_post/2,-w_beam/2]) rotate([90,0,0]) cylinder(r=r_screw_large, h=h_box, center=true, $fn=100);
        translate([w_box/2-w_post*1.5, w_box/2-w_post/2,-w_beam/2]) rotate([90,0,0]) cylinder(r=r_screw_large, h=h_box, center=true, $fn=100);
        translate([w_box/2-w_post*1.5, w_box/2-w_post/2-r_screw/2,-h_box]) cylinder(r=r_screw, h=h_box, center=true, $fn=100);
        translate([w_box/2-w_post/2, w_box/2-w_post/2,r_screw/2+w_beam-h_box]) rotate([90,0,0]) cylinder(r=r_screw, h=h_box, center=true, $fn=100);
        translate([w_box/2-w_post/2, w_box/2-w_post/2,r_screw/2+w_beam/2-h_box]) rotate([90,0,90]) cylinder(r=r_screw, h=h_box, center=true, $fn=100);
        translate([w_box/2-w_post/2, w_box/2-w_post/2,-r_screw/2-w_beam*1.5]) rotate([90,0,90]) cylinder(r=r_screw, h=h_box, center=true, $fn=100);           
}

/**********/
module post_backRight(){
    difference(){
            union(){
                translate([-w_box/2+w_post/2+w_acrylic, w_box/2-w_post/2,-h_post/2]) cube([w_post, w_post, h_post], center=true);
                
                translate([-w_box/2+w_post+w_acrylic, w_box/2-w_post/2,-w_beam-thick/2]) cube([w_post*2, w_post, thick], center=true);
                translate([-w_box/2+w_post+w_acrylic, w_box/2-w_post+thick/2,-w_beam-thick/2+w_beam/2]) rotate([90,0,0]) cube([w_post*2, w_post, thick], center=true);
                
                translate([-w_box/2+w_post-w_post+thick/2+w_acrylic, w_box/2-w_post,-w_beam-thick/2+w_beam/2]) rotate([90,0,90]) cube([w_post*2, w_post, thick], center=true);
                translate([-w_box/2+w_post-w_post+thick/2+w_acrylic, w_box/2-w_post+thick/2.-3.8,-w_beam-thick/2-w_beam/2+1]) rotate([90,45,90]) cube([w_post*1.7, w_post, thick], center=true);
            
            }
            
            translate([0,w_box/2-w_beam/2,-h_beam/2]) cube([2*w_box+d, w_beam+d, h_beam+d], center=true);  
            translate([-w_box/2+w_post/2+2*thick+d/2, w_box/2-w_post/2-thick,-h_post/2-w_beam/2]) cube([w_post+d, w_post+d, h_post-w_beam-thick*2], center=true); 
            
             //screws
            //translate([-w_box/2+w_post*.5+w_acrylic, -w_box/2+w_beam/2,0]) cylinder(r=r_screw_large, h=h_box, center=true, $fn=100);
            translate([-w_box/2+w_post*1.5+w_acrylic, w_box/2-w_beam/2,0]) cylinder(r=r_screw_large, h=h_box, center=true, $fn=100);
            translate([-w_box/2+w_post/2+w_acrylic, w_box/2-w_post/2,-w_beam/2]) rotate([90,0,0]) cylinder(r=r_screw_large, h=h_box, center=true, $fn=100);
            translate([-w_box/2+w_post*1.5+w_acrylic, w_box/2-w_post/2,-w_beam/2]) rotate([90,0,0]) cylinder(r=r_screw_large, h=h_box, center=true, $fn=100);
            translate([-w_box/2, w_box/2-w_post/2-w_beam-w_acrylic,-w_beam/2]) rotate([90,0,90]) cylinder(r=r_screw_large, h=h_box, center=true, $fn=100);
            translate([-w_box/2+w_post/2, w_box/2-w_post-thick/2-thick,-w_beam*1.5]) rotate([90,0,90]) cylinder(r=r_screw_large, h=h_box, center=true, $fn=100);
            
            
            translate([-w_box/2+w_acrylic+w_beam/2+thick, w_box/2-w_post/2+r_screw/2-thick,-h_box]) cylinder(r=r_screw, h=h_box, center=true, $fn=100);
            translate([-w_box/2+w_post/2+w_acrylic*1.5, w_box/2-w_post/2,r_screw/2+w_beam-h_box]) rotate([90,0,0]) cylinder(r=r_screw, h=h_box, center=true, $fn=100);
            translate([-w_box/2+w_post/2, w_box/2-w_post/2-thick/2,r_screw/2+w_beam/2-h_box]) rotate([90,0,90]) cylinder(r=r_screw, h=h_box, center=true, $fn=100);
            
            
        }
}


/***********/
module post_backLeft(){
        difference(){
            union(){
                translate([-w_box/2+w_post/2+w_acrylic, -w_box/2+w_post/2,-h_post/2]) cube([w_post, w_post, h_post], center=true);
                
                translate([-w_box/2+w_post+w_acrylic, -w_box/2+w_post/2,-w_beam-thick/2]) cube([w_post*2, w_post, thick], center=true);
                translate([-w_box/2+w_post+w_acrylic, -w_box/2+w_post-thick/2,-w_beam-thick/2+w_beam/2]) rotate([90,0,0]) cube([w_post*2, w_post, thick], center=true);
                
                translate([-w_box/2+w_post-w_post+thick/2+w_acrylic, -w_box/2+w_post,-w_beam-thick/2+w_beam/2]) rotate([90,0,90]) cube([w_post*2, w_post, thick], center=true);
                  translate([-w_box/2+w_post-w_post+thick/2+w_acrylic, -w_box/2+w_post-thick/2.+3.8,-w_beam-thick/2-w_beam/2+1]) rotate([90,-45,90]) cube([w_post*1.7, w_post, thick], center=true);
            
            }
            
            translate([0,-w_box/2+w_beam/2,-h_beam/2]) cube([2*w_box+d, w_beam+d, h_beam+d], center=true);  
            translate([-w_box/2+w_post/2+2*thick+d/2, -w_box/2+w_post/2+thick,-h_post/2-w_beam/2]) cube([w_post+d, w_post+d, h_post-w_beam-thick*2], center=true); 
            
             //screws
            //translate([-w_box/2+w_post*.5+w_acrylic, -w_box/2+w_beam/2,0]) cylinder(r=r_screw_large, h=h_box, center=true, $fn=100);
            translate([-w_box/2+w_post*1.5+w_acrylic, -w_box/2+w_beam/2,0]) cylinder(r=r_screw_large, h=h_box, center=true, $fn=100);
            translate([-w_box/2+w_post/2+w_acrylic, -w_box/2+w_post/2,-w_beam/2]) rotate([90,0,0]) cylinder(r=r_screw_large, h=h_box, center=true, $fn=100);
            translate([-w_box/2+w_post*1.5+w_acrylic, -w_box/2+w_post/2,-w_beam/2]) rotate([90,0,0]) cylinder(r=r_screw_large, h=h_box, center=true, $fn=100);
            translate([-w_box/2, -w_box/2+w_post/2+w_beam+w_acrylic,-w_beam/2]) rotate([90,0,90]) cylinder(r=r_screw_large, h=h_box, center=true, $fn=100);
            translate([-w_box/2+w_post/2, -w_box/2+w_post+thick/2+thick,-w_beam*1.5]) rotate([90,0,90]) cylinder(r=r_screw_large, h=h_box, center=true, $fn=100);
            
            
            translate([-w_box/2+w_acrylic+w_beam/2+thick, -w_box/2+w_post/2-r_screw/2+thick,-h_box]) cylinder(r=r_screw, h=h_box, center=true, $fn=100);
            translate([-w_box/2+w_post/2+w_acrylic*1.5, -w_box/2+w_post/2,r_screw/2+w_beam-h_box]) rotate([90,0,0]) cylinder(r=r_screw, h=h_box, center=true, $fn=100);
            translate([-w_box/2+w_post/2, -w_box/2+w_post/2+thick/2,r_screw/2+w_beam/2-h_box]) rotate([90,0,90]) cylinder(r=r_screw, h=h_box, center=true, $fn=100);
            
        }
}


/************/

module post_frontLeft(){
    //Front-Left post
    difference(){
        union(){
            translate([w_box/2-w_post/2, -w_box/2+w_post/2,-h_post/2]) cube([w_post, w_post, h_post], center=true);
            
            translate([w_box/2-w_post, -w_box/2+w_post/2,-w_beam-thick/2]) cube([w_post*2, w_post, thick], center=true);
            translate([w_box/2-w_post, -w_box/2+thick/2+w_beam,-w_beam/2-thick/2]) rotate([90,0,0]) cube([w_post*2, w_post, thick], center=true);
            
            translate([w_box/2-w_post, -w_box/2+w_post/2,thick/2-h_box]) cube([w_post*2, w_post, thick], center=true);
            
        }
        
        translate([0,-w_box/2+w_beam/2,-h_beam/2]) cube([2*w_box+d, w_beam+d, h_beam+d], center=true);  
        translate([w_box/2-w_post/2-thick, -w_box/2+w_post/2+thick,-h_post/2-w_beam/2]) cube([w_post, w_post, h_post-w_beam-thick*2], center=true); 
        
        //screws
        translate([w_box/2-w_post*1.5, -w_box/2+w_beam/2,0]) cylinder(r=r_screw_large, h=h_box, center=true, $fn=100);
        translate([w_box/2-w_post/2, -w_box/2+w_post/2,-w_beam/2]) rotate([90,0,0]) cylinder(r=r_screw_large, h=h_box, center=true, $fn=100);
        translate([w_box/2-w_post*1.5, -w_box/2+w_post/2,-w_beam/2]) rotate([90,0,0]) cylinder(r=r_screw_large, h=h_box, center=true, $fn=100);
        
        translate([w_box/2-w_post*1.5, -w_box/2+w_post/2-r_screw/2,-h_box]) cylinder(r=r_screw, h=h_box, center=true, $fn=100);
        translate([w_box/2-w_post/2, -w_box/2+w_post/2,r_screw/2+w_beam-h_box]) rotate([90,0,0]) cylinder(r=r_screw, h=h_box, center=true, $fn=100);
        translate([w_box/2-w_post/2, -w_box/2+w_post/2,r_screw/2+w_beam/2-h_box]) rotate([90,0,90]) cylinder(r=r_screw, h=h_box, center=true, $fn=100);
        translate([w_box/2-w_post/2, -w_box/2+w_post/2,-r_screw/2-w_beam*1.5]) rotate([90,0,90]) cylinder(r=r_screw, h=h_box, center=true, $fn=100);
    }
}



//import("v-slot_joiner.stl");
module post_frontRight(){
    //Front-Right post
    difference(){
        
        union(){
            translate([w_box/2-w_post/2, w_box/2-w_post/2,-h_post/2]) cube([w_post, w_post, h_post], center=true);
            
            
            translate([w_box/2-w_post, w_box/2-w_post/2,-w_beam-thick/2]) cube([w_post*2, w_post, thick], center=true);
            translate([w_box/2-w_post, w_box/2-thick/2-w_beam,-w_beam/2-thick/2]) rotate([90,0,0]) cube([w_post*2, w_post, thick], center=true);
            translate([w_box/2-w_post, w_box/2-w_post/2,thick/2-h_box]) cube([w_post*2, w_post, thick], center=true);
        }
        
        
        
        translate([0,w_box/2-w_beam/2,-h_beam/2]) cube([2*w_box+d, w_beam+d, h_beam+d], center=true);  
        translate([w_box/2-w_post/2-thick, w_box/2-w_post/2-thick,-h_post/2-w_beam/2]) cube([w_post, w_post, h_post-w_beam-thick*2], center=true); 
        
        
        //screws
        translate([w_box/2-w_post*1.5, w_box/2-w_beam/2,0]) cylinder(r=r_screw_large, h=h_box, center=true, $fn=100);
        translate([w_box/2-w_post/2, w_box/2-w_post/2,-w_beam/2]) rotate([90,0,0]) cylinder(r=r_screw_large, h=h_box, center=true, $fn=100);
        translate([w_box/2-w_post*1.5, w_box/2-w_post/2,-w_beam/2]) rotate([90,0,0]) cylinder(r=r_screw_large, h=h_box, center=true, $fn=100);
        
        translate([w_box/2-w_post*1.5, w_box/2-w_post/2-r_screw/2,-h_box]) cylinder(r=r_screw, h=h_box, center=true, $fn=100);
        translate([w_box/2-w_post/2, w_box/2-w_post/2,r_screw/2+w_beam-h_box]) rotate([90,0,0]) cylinder(r=r_screw, h=h_box, center=true, $fn=100);
        translate([w_box/2-w_post/2, w_box/2-w_post/2,r_screw/2+w_beam/2-h_box]) rotate([90,0,90]) cylinder(r=r_screw, h=h_box, center=true, $fn=100);
        translate([w_box/2-w_post/2, w_box/2-w_post/2,-r_screw/2-w_beam*1.5]) rotate([90,0,90]) cylinder(r=r_screw, h=h_box, center=true, $fn=100);
    }
}

//OpenBeams
module frame_openBuilds(){
    color([0,1,1]) {
    //translate([0,-w_box/2+w_beam/2,-h_beam/2]) cube([w_box, w_beam, h_beam], center=true);  //left
        
            translate([-w_box/2,w_box/2-w_beam/2,-h_beam/2])  rotate([0,90,0]) scale([1,1,22])  import("V-Slot_Rail.stl");
        translate([-w_box/2,-w_box/2+w_beam/2,-h_beam/2])  rotate([0,90,0]) scale([1,1,22])  import("V-Slot_Rail.stl");
        
        //translate([-w_box/2-w_beam/2, 0,-h_beam]) cube([w_beam, w_box, h_beam*2], center=true);  //Back
        translate([-w_box/2-w_beam/2, w_box/2,-w_beam/2]) rotate([90,0,0])scale([1,1,22]) import("V-Slot_Rail.stl");
        translate([-w_box/2-w_beam/2, w_box/2,-w_beam*1.5]) rotate([90,0,0])scale([1,1,22]) import("V-Slot_Rail.stl");
        
        translate([-w_box/2+w_beam/2,-w_box/2+w_beam*1.5,0]) import("20x20_sideplate.stl");
        translate([-w_box/2+w_beam/2,w_box/2-w_beam*1.5,0]) mirror([0,1,0]) import("20x20_sideplate.stl");
        
        
    }

}

