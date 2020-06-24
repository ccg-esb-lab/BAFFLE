d=0.2;

r_shaft=4.5;

wall=3;

r_support=20+2*wall+d;

r_screw=2.5;

h_support=10+wall;

dist_screws=20;
r_bolt=r_screw+2;


r_disc=120;
r_camera=33;
dist_screws=20;
r_filter=12;

dist_filter_min=87.5;
dist_filter_max=98;

depth_acrylic1=5;
depth_acrylic2=3;

h_switch=30;
w_switch=5;
l_switch=60;

/********/


translate([0,0,h_support/2+3.1]) mirror([0,0,1]) support();


//limit_switch();

//projection(cut = false) 
//intersection(){
//color([0,0,0]) 


//projection(cut = false) 
color([1,.5,0]) disc1();



difference(){
    //translate([0,0,20])color([0,1,0])
    translate([0,0,5]) color([1,0,0])  
    //projection(cut = false) 
    disc2();
    translate([0,0,4.]) disc2_layer2();
}


//    rotate([0,0,-5]) translate([-125,-15,-5]) cube([250,30,10]);
//}

  translate([0,0,-0]) filter_cubes();


translate([0,0,-40-wall]) color([.5,1,0])   disc3();
//projection(cut = false)    
    

/***********************/

module filter_cubes(){
    color([1,0,1]){
        for (a =[0,60,180, 240]){
            rotate([0,0,a]) {
                translate([-20,30,-40]) import("../STL/baffle_filterCube_top.stl");
            }
        }
    }
        

    color([0,1,1]){
        for (a =[0,60,180, 240]){
            rotate([0,0,a])
                translate([-20,30,-40]) import("../STL/baffle_filterCube_bottom.stl");
        }   
    }
}

/*****************/

module disc2_layer2(){

        for (a =[0,60,180, 240]){
            rotate([0,0,a]) {
               // translate([-20,dist_filter-20,-40]) import("../STL/baffle_filterCube_top.stl");
            
                //Filter Screws
                translate([0,dist_filter_min-30,wall]) cylinder(r=r_bolt, h=h_support+d*2, $fn=100);
                translate([0,dist_filter_max-30,wall]) cylinder(r=r_bolt, h=h_support+d*2, $fn=100);
                translate([-r_bolt,dist_filter_min-30,wall]) cube([r_bolt*2, dist_filter_max-dist_filter_min, h_support+d*2]);
                
                
                translate([25,dist_filter_max+14,wall]) cylinder(r=r_bolt, h=h_support+d*2, $fn=100);
                translate([25,dist_filter_min+14,wall]) cylinder(r=r_bolt, h=h_support+d*2, $fn=100);
                translate([25-r_bolt,dist_filter_min+14,wall]) cube([r_bolt*2, dist_filter_max-dist_filter_min, h_support+d*2]);
                
                translate([-25,dist_filter_max+14,wall]) cylinder(r=r_bolt, h=h_support+d*2, $fn=100);
                translate([-25,dist_filter_min+14,wall]) cylinder(r=r_bolt, h=h_support+d*2, $fn=100);
                translate([-25-r_bolt,dist_filter_min+14,wall]) cube([r_bolt*2, dist_filter_max-dist_filter_min, h_support+d*2]);
        }
        //rotate([0,0,120]) translate([0,this_dist_filter-30,-50]) cylinder(r=r_screw, h=100, $fn=100);
        //rotate([0,0,300]) translate([0,dist_filter-30,-50]) cylinder(r=r_screw, h=100, $fn=100);
        
    }
      
        
        //Acrylic Screws (outer)
        for (a =[0,60,120,180, 240, 300]){
            rotate([0,0,a]) 
                rotate([0,0,30]) translate([0,r_disc-dist_screws,wall]) cylinder(r=r_bolt, h=h_support+d*2, $fn=6);
        }
        
     
        //Acrylic screws (cablebox)
        rotate([0,0,-240]) translate([0,r_disc-dist_screws,wall]) cylinder(r=r_bolt, h=h_support+d*2,  $fn=100);
        
        //Acrylic screws (limit switch)
        rotate([0,0,-220]) translate([0,r_disc-dist_screws,wall]) cylinder(r=r_bolt, h=h_support+d*2,  $fn=100);
        rotate([0,0,-260]) translate([0,r_disc-dist_screws,wall]) cylinder(r=r_bolt, h=h_support+d*2,  $fn=100);
        rotate([0,0,-220]) translate([0,r_disc-dist_screws*2,wall]) cylinder(r=r_bolt, h=h_support+d*2,  $fn=100);
        rotate([0,0,-260]) translate([0,r_disc-dist_screws*2,wall]) cylinder(r=r_bolt, h=h_support+d*2,  $fn=100);
        
        
        
}

module disc1(){

    
    difference(){
        cylinder(r=r_disc, h=depth_acrylic1, $fn=100);
        
        translate([0,0,-50]) cylinder(r=r_shaft, h=100, $fn=100);
        
        //Box cube holes
        for (a =[0,60,180, 240]){
            rotate([0,0,a]) {
                //translate([-20,dist_filter_min-60,-40]) import("../STL/baffle_filterCube_top.stl");
               // translate([-20,dist_filter_max-60,-40]) import("../STL/baffle_filterCube_top.stl");
                translate([-20-d*2,dist_filter_max-60-d*2+2,-10]) cube([40+d*4,80+d*4,20]);
                translate([-30-d*2,dist_filter_max-20-d*2,-10]) cube([10+d*4,40+d*4,20]);
                translate([20-d*2,dist_filter_max-20-d*2,-10]) cube([10+d*4,40+d*4,20]);
            
        }
        
    }
        
        //Center Screws
        for (a =[0,60,120,180, 240, 300]){
            rotate([0,0,a]) 
                translate([0,dist_screws/2,wall]) cylinder(r=r_screw, h=h_support+d*2, center=true, $fn=100);
        }
        
        //Acrylic Screws (inner)
        for (a =[0,60,120,180, 240, 300]){
            rotate([0,0,a]) 
                translate([0,dist_screws/2+dist_screws,wall]) cylinder(r=r_screw, h=h_support+d*2, center=true, $fn=100);
        }
        
        //Acrylic Screws (outer)
        for (a =[0,60,120,180, 240, 300]){
            rotate([0,0,a]) 
                rotate([0,0,30]) translate([0,r_disc-dist_screws,wall]) cylinder(r=r_screw, h=h_support+d*2, center=true, $fn=100);
        }
     
        //Acrylic screws (cablebox)
        rotate([0,0,-240]) translate([0,r_disc-dist_screws,wall]) cylinder(r=r_screw, h=h_support+d*2, center=true, $fn=100);
        
        //Acrylic screws (limit switch)
        rotate([0,0,-220]) translate([0,r_disc-dist_screws,wall]) cylinder(r=r_screw, h=h_support+d*2, center=true, $fn=100);
        rotate([0,0,-260]) translate([0,r_disc-dist_screws,wall]) cylinder(r=r_screw, h=h_support+d*2, center=true, $fn=100);
        rotate([0,0,-220]) translate([0,r_disc-dist_screws*2,wall]) cylinder(r=r_screw, h=h_support+d*2, center=true, $fn=100);
        rotate([0,0,-260]) translate([0,r_disc-dist_screws*2,wall]) cylinder(r=r_screw, h=h_support+d*2, center=true, $fn=100);
        
        //Camera hole
        rotate([0,0,300]) translate([0,dist_filter_min,wall]) cylinder(r=r_camera, h=h_support+d*2, center=true, $fn=100);
        rotate([0,0,300]) translate([0,dist_filter_max,wall]) cylinder(r=r_camera, h=h_support+d*2, center=true, $fn=100);
        rotate([0,0,300]) translate([-r_camera,dist_filter_min,-d]) cube([r_camera*2, dist_filter_max-dist_filter_min, h_support+d*2]);
        
        //Cable box
        w_cable_box=40;
        h_cable_box=40;
        rotate([0,0,-240]) translate([0,r_disc-dist_screws,wall]) cube([w_cable_box, h_cable_box, 10],center=true);
    }
}



module disc2(){
    
    difference(){
        cylinder(r=r_disc, h=depth_acrylic2, $fn=100);
        
        translate([0,0,-40]) cylinder(r=r_shaft, h=100, $fn=100);
        
        
        for (a =[0,60,180, 240]){
            rotate([0,0,a]) {
               // translate([-20,dist_filter-20,-40]) import("../STL/baffle_filterCube_top.stl");
            
                //Filter Screws
                translate([0,dist_filter_min-30,-50]) cylinder(r=r_screw, h=100, $fn=100);
                translate([0,dist_filter_max-30,-50]) cylinder(r=r_screw, h=100, $fn=100);
                translate([-r_screw,dist_filter_min-30,-d]) cube([r_screw*2, dist_filter_max-dist_filter_min, h_support+d*2]);
                
                
                translate([25,dist_filter_max+14,-50]) cylinder(r=r_screw, h=100, $fn=100);
                translate([25,dist_filter_min+14,-50]) cylinder(r=r_screw, h=100, $fn=100);
                translate([25-r_screw,dist_filter_min+14,-d]) cube([r_screw*2, dist_filter_max-dist_filter_min, h_support+d*2]);
                
                translate([-25,dist_filter_max+14,-50]) cylinder(r=r_screw, h=100, $fn=100);
                translate([-25,dist_filter_min+14,-50]) cylinder(r=r_screw, h=100, $fn=100);
                translate([-25-r_screw,dist_filter_min+14,-d]) cube([r_screw*2, dist_filter_max-dist_filter_min, h_support+d*2]);
        }
        //rotate([0,0,120]) translate([0,this_dist_filter-30,-50]) cylinder(r=r_screw, h=100, $fn=100);
        //rotate([0,0,300]) translate([0,dist_filter-30,-50]) cylinder(r=r_screw, h=100, $fn=100);
        
    }
        //Hole for support
        translate([0,0,wall]) cylinder(r=r_support+10, h=h_support+d*2, center=true, $fn=100);
        
        //Center Screws
        for (a =[0,60,120,180, 240, 300]){
            rotate([0,0,a]) 
                translate([0,dist_screws/2,wall]) cylinder(r=r_screw, h=h_support+d*2, center=true, $fn=100);
        }
        
        //Acrylic Screws (inner)
        for (a =[0,60,120,180, 240, 300]){
            rotate([0,0,a]) 
                translate([0,dist_screws/2+dist_screws,wall]) cylinder(r=r_screw, h=h_support+d*2, center=true, $fn=100);
        }
        
        //Acrylic Screws (outer)
        for (a =[0,60,120,180, 240, 300]){
            rotate([0,0,a]) 
                rotate([0,0,30]) translate([0,r_disc-dist_screws,wall]) cylinder(r=r_screw, h=h_support+d*2, center=true, $fn=100);
        }
        
        //Acrylic screws (cablebox)
        rotate([0,0,-240]) translate([0,r_disc-dist_screws,wall]) cylinder(r=r_screw, h=h_support+d*2, center=true, $fn=100);
        
        //Acrylic screws (limit switch)
        rotate([0,0,-220]) translate([0,r_disc-dist_screws,wall]) cylinder(r=r_screw, h=h_support+d*2, center=true, $fn=100);
        rotate([0,0,-260]) translate([0,r_disc-dist_screws,wall]) cylinder(r=r_screw, h=h_support+d*2, center=true, $fn=100);
        rotate([0,0,-220]) translate([0,r_disc-dist_screws*2,wall]) cylinder(r=r_screw, h=h_support+d*2, center=true, $fn=100);
        rotate([0,0,-260]) translate([0,r_disc-dist_screws*2,wall]) cylinder(r=r_screw, h=h_support+d*2, center=true, $fn=100);
        
        //filter holes
        for (a =[0,60,180, 240]){
            rotate([0,0,a]) {
                translate([0,dist_filter_min-2,wall]) cylinder(r=r_filter-2, h=h_support+d*2, center=true, $fn=100);
                translate([0,dist_filter_max+2,wall]) cylinder(r=r_filter-2, h=h_support+d*2, center=true, $fn=100);
                translate([-r_filter+2,dist_filter_min-2,-d]) cube([r_filter*2-4, dist_filter_max-dist_filter_min+4, h_support+d*2]);
            }
        }
        
        rotate([0,0,300]) translate([0,dist_filter_min,wall]) cylinder(r=r_camera, h=h_support+d*2, center=true, $fn=100);
        rotate([0,0,300]) translate([0,dist_filter_max,wall]) cylinder(r=r_camera, h=h_support+d*2, center=true, $fn=100);
        rotate([0,0,300]) translate([-r_camera,dist_filter_min,-d]) cube([r_camera*2, dist_filter_max-dist_filter_min, h_support+d*2]);
        
    }
}



module disc3(){
    
    difference(){
        cylinder(r=r_disc, h=depth_acrylic2, $fn=100);
        
        //shaft
        //translate([0,0,-40]) cylinder(r=r_shaft, h=100, $fn=100);
        
        
        for (a =[0,60,180, 240]){
            rotate([0,0,a]) {
               // translate([-20,dist_filter-20,-40]) import("../STL/baffle_filterCube_top.stl");
            
                //Filter Screws
                translate([0,dist_filter_min-30,-50]) cylinder(r=r_screw, h=100, $fn=100);
                translate([0,dist_filter_max-30,-50]) cylinder(r=r_screw, h=100, $fn=100);
                translate([-r_screw,dist_filter_min-30,-d]) cube([r_screw*2, dist_filter_max-dist_filter_min, h_support+d*2]);
                
                
                translate([25,dist_filter_max+14,-50]) cylinder(r=r_screw, h=100, $fn=100);
                translate([25,dist_filter_min+14,-50]) cylinder(r=r_screw, h=100, $fn=100);
                translate([25-r_screw,dist_filter_min+14,-d]) cube([r_screw*2, dist_filter_max-dist_filter_min, h_support+d*2]);
                
                translate([-25,dist_filter_max+14,-50]) cylinder(r=r_screw, h=100, $fn=100);
                translate([-25,dist_filter_min+14,-50]) cylinder(r=r_screw, h=100, $fn=100);
                translate([-25-r_screw,dist_filter_min+14,-d]) cube([r_screw*2, dist_filter_max-dist_filter_min, h_support+d*2]);
        }
        //rotate([0,0,120]) translate([0,this_dist_filter-30,-50]) cylinder(r=r_screw, h=100, $fn=100);
        //rotate([0,0,300]) translate([0,dist_filter-30,-50]) cylinder(r=r_screw, h=100, $fn=100);
        
    }
        //Hole for support
        //translate([0,0,wall]) cylinder(r=r_support+10, h=h_support+d*2, center=true, $fn=100);
        
        //Center Screws
    /*
        for (a =[0,60,120,180, 240, 300]){
            rotate([0,0,a]) 
                translate([0,dist_screws/2,wall]) cylinder(r=r_screw, h=h_support+d*2, center=true, $fn=100);
        }
    */
        
    
        //Acrylic Screws (inner)
        for (a =[0,60,120,180, 240, 300]){
            rotate([0,0,a]) 
                translate([0,dist_screws/2+dist_screws,wall]) cylinder(r=r_screw, h=h_support+d*2, center=true, $fn=100);
        }
    
        
        //Acrylic Screws (outer)
        for (a =[0,60,120,180, 240, 300]){
            rotate([0,0,a]) 
                rotate([0,0,30]) translate([0,r_disc-dist_screws,wall]) cylinder(r=r_screw, h=h_support+d*2, center=true, $fn=100);
        }
        
        //Acrylic screws (cablebox)
        rotate([0,0,-240]) translate([0,r_disc-dist_screws,wall]) cylinder(r=r_screw, h=h_support+d*2, center=true, $fn=100);
        
        //Acrylic screws (limit switch)
        rotate([0,0,-220]) translate([0,r_disc-dist_screws,wall]) cylinder(r=r_screw, h=h_support+d*2, center=true, $fn=100);
        rotate([0,0,-260]) translate([0,r_disc-dist_screws,wall]) cylinder(r=r_screw, h=h_support+d*2, center=true, $fn=100);
        rotate([0,0,-220]) translate([0,r_disc-dist_screws*2,wall]) cylinder(r=r_screw, h=h_support+d*2, center=true, $fn=100);
        rotate([0,0,-260]) translate([0,r_disc-dist_screws*2,wall]) cylinder(r=r_screw, h=h_support+d*2, center=true, $fn=100);
        
        //filter holes
        for (a =[0,60,180, 240]){
            rotate([0,0,a]) {
                translate([0,dist_filter_min,wall]) cylinder(r=r_filter, h=h_support+d*2, center=true, $fn=100);
                translate([0,dist_filter_max,wall]) cylinder(r=r_filter, h=h_support+d*2, center=true, $fn=100);
                translate([-r_filter,dist_filter_min,-d]) cube([r_filter*2, dist_filter_max-dist_filter_min, h_support+d*2]);
            }
        }
        
        rotate([0,0,300]) translate([0,dist_filter_min,wall]) cylinder(r=r_camera, h=h_support+d*2, center=true, $fn=100);
        rotate([0,0,300]) translate([0,dist_filter_max,wall]) cylinder(r=r_camera, h=h_support+d*2, center=true, $fn=100);
        rotate([0,0,300]) translate([-r_camera,dist_filter_min,-d]) cube([r_camera*2, dist_filter_max-dist_filter_min, h_support+d*2]);
        
    }
}


module limit_switch(){
    
    difference(){
        union(){
            #rotate([0,0,30])  translate([-80,0,wall/2]) cube([l_switch, 2*w_switch, wall],center=true);
            #rotate([0,0,30])  translate([-80,0,wall/2+h_switch/2]) cube([l_switch/2, w_switch, h_switch],center=true);
        }
    
    
        rotate([0,0,-240]) translate([0,r_disc-dist_screws,wall]) cylinder(r=r_screw, h=h_support+d*2, center=true, $fn=100);
        rotate([0,0,-240]) translate([0,r_disc-dist_screws*3,wall]) cylinder(r=r_screw, h=h_support+d*2, center=true, $fn=100);
        
    }
}


module support(){
    difference(){
        union(){
           translate([0,0,-wall]) cylinder(r=r_support, h=h_support, center=true, $fn=100);
          translate([0,0,wall]) cylinder(r=r_support+10, h=wall, center=true, $fn=100);
        
        }    
            
        cylinder(r=r_shaft, h=h_support+d*2, center=true, $fn=100);
        rotate([0,0,0]) translate([0,0,-wall]) cylinder(r=r_support-wall+1, h=h_support+d*2, center=true,$fn=6);
        
        //Support screw
        for (a =[0,60,120,180, 240, 300]){
            rotate([0,0,a]) 
                translate([0,dist_screws/2,wall]) cylinder(r=r_screw, h=h_support+d*2, center=true, $fn=100);
        }
        
        //Filter holes
        //rotate([0,0,300]) translate([0,dist_filter,wall]) cylinder(r=r_camera, h=h_support+d*2, center=true, $fn=100);
        
        for (a =[0,60,120,180, 240]){
            rotate([0,0,a]) {
                //Filter Screws
                translate([0,dist_filter-30,-50]) cylinder(r=r_screw, h=100, $fn=100);
            }
        }
        
                
        for (a =[0,60,120,180, 240, 300]){
            rotate([0,0,a]) {
                //support screws
                translate([0,dist_screws/2+dist_screws,-50]) cylinder(r=r_screw, h=100, $fn=100);
            }
        }
        
    }
    
}
