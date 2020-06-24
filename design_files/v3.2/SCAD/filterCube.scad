// Components
d=0.2;
ledDissipatorRadius = 20-.1;
ledDissipatorHeight = 3;
filterRadius = 25/2+.3;
filterHeight = 3.5;

// Dicronic filter



//Aux vaiables

circleSpace = 0.25; // Espacio extra para que embonen los componentes circulares



//filter();

//rotate([0,0,180])translate([0,50,50])import("./files/filterwheel_segment.stl");



/*for(i = [1:5]){
	rotate([0,0,-20+(i*(angle/5))])
	translate([-100,0,45/2])
	filter();
}*/

depth_holder=3;
w_holder=10;
r_screw=2.5;




//translate([0,40,0])
filterCubeBottom();


color( "cyan", 1.0 ){
filterCubeTop();


}


//projection(cut = false) filter_spacer();
module filter_spacer(){
    

    difference(){
        cylinder(r=24/2, h=4, center=true, $fn=100);
        cylinder(r=22/2, h=4+2*d, center=true, $fn=100);
    }
}

module filterCubeTop( BX = 40, BY = 40, H = 40) {
	union(){
		difference(){
			union(){
			rotate([90,0,180])
			translate([-40,0,0])
			prism(BX,H,BY);

			translate([0,-5,0])
			cube(size=[BX,5,H], center=false);

			// Patita para atorar en open builds
			//#rotate([0,90,-90])
			//translate([-45+10,0,7-0.2])
			//import("./tnut_B2.stl");


			// patitas para embone entre cubos
			rotate([45,0,0])
			translate([0,(((40*sqrt(2)) - 15)/2)+15.5,-5])
			cube(size=[4.5,14,5], center=false);

			rotate([45,0,0])
			translate([0,(((40*sqrt(2)) - 15)/2)-14.5,-5])
			cube(size=[4.5,14,5], center=false);

			rotate([45,0,0])
			translate([BX-4.5,(((40*sqrt(2)) - 15)/2)-14.5,-5])
			cube(size=[4.5,14.,5], center=false);

			rotate([45,0,0])
			translate([BX-4.5,(((40*sqrt(2)) - 15)/2)+15.5,-5])
			cube(size=[4.5,14.,5], center=false);
			}

			// Espacio para patitas de embone entre cubos
			rotate([45,0,0])
			translate([0,(((40*sqrt(2)) - 15)/2)-1,-5])
			cube(size=[5.5,15+2,10+1], center=false);

			rotate([45,0,0])
			translate([BX-5.5,(((40*sqrt(2)) - 15)/2)-1.,-5])
			cube(size=[5.5,15+2,10+1], center=false);
			//

			// Espacio cables

			translate([3,-5,H-3])
			cube(size=[3,BY+5,3], center=false);

			translate([BX-6,-5,H-3])
			cube(size=[3,BY+5,3], center=false);

			// Huecos para filtros

			rotate([])
			translate([BX/2,BY/2,35-1])
			cylinder(h=filterHeight+2.6, r=filterRadius + circleSpace, center=false, $fn=100);

			rotate([])
			translate([BX/2,BY/2,0])
			cylinder(h=45, r=filterRadius-2, center=false, $fn=100);
			
			//Hueco para filtro dicronico

			rotate([90,0,180])
			translate([(-BX-23)/2,  (H-25.8)/2, (BY-25.8)/2])
			prism(23, 25.8, 25.8);

			
		}
	}
    
difference(){
    union(){
        translate([6,-5-w_holder,40-depth_holder]) cube([28,w_holder,depth_holder]);
        rotate([0,0,90]) translate([29,10-w_holder,20]) cube([11,w_holder,20]);
        rotate([0,0,90]) translate([29,-50,20]) cube([11,w_holder,20]);
        
    }
    translate([20,-10,40-depth_holder-50])cylinder(r=r_screw, h=100, $fn=100);
    translate([45,34,40-depth_holder-50])cylinder(r=r_screw, h=100, $fn=100);
    translate([-5,34,40-depth_holder-50])cylinder(r=r_screw, h=100, $fn=100);
    
    rotate([45,0,0]) translate([-15,0,-45]) cube([70,80,40]);
}
	
}

module filterCubeBottom( BX = 40, BY = 40, H = 40) {
	
union(){
translate([0,40,0])
difference(){
    filterDepth=20;
    
	cube(size=[BX,filterDepth,H], center=false);

	rotate([90,0,0])
	translate([BX-BX/2,50-30,-filterHeight-filterDepth/2])
	cylinder(h=filterHeight+filterDepth, r=filterRadius-2, center=false, $fn=100);
    
    rotate([90,0,0])
	translate([BX-BX/2, filterDepth,-filterDepth])
	cylinder(h=filterHeight+filterDepth, r=filterRadius+d , center=false, $fn=100);
    
	rotate([90,0,0])
	translate([BX-BX/2,50-30,-filterDepth-1-10])
	cylinder(h=filterDepth, r=ledDissipatorRadius + circleSpace, center=false, $fn=100);


	translate([(BX/2)-2.5,8,40-10])
	cube(size=[5,4,10], center=false);

	//
	// Espacio para cables
	translate([3,0,0])
	cube(size=[3,10,3], center=false);

	translate([BY-6,0,0])
	cube(size=[3,10,3], center=false);

}

difference(){
	union(){
	prism(BX, BY, H);

	rotate([45,0,0])
	translate([0,((40*sqrt(2)) - 15)/2,0])
	cube(size=[5,15,5], center=false);

	rotate([45,0,0])
	translate([BX-5,((40*sqrt(2)) - 15)/2,0])
	cube(size=[5,15,5], center=false);
	}
	// couplers

	rotate([45,0,0])
	translate([0,(((40*sqrt(2)) - 15)/2) +15 -0.5,-5])
	cube(size=[5,15+1,10], center=false);

	rotate([45,0,0])
	translate([0,(((40*sqrt(2)) - 15)/2) -15 -0.5-5.6,-5])
	cube(size=[5,15+1+6,10], center=false);

	rotate([45,0,0])
	translate([BX-5,(((40*sqrt(2)) - 15)/2) +15-0.5,-5])
	cube(size=[5,15+1,10], center=false);

	rotate([45,0,0])
	translate([BX-5,(((40*sqrt(2)) - 15)/2) -15 - 0.5-5-.5,-5])
	cube(size=[5,15+1+6,10], center=false);
	////

	// HUeco para filtro dicroico
	rotate([45,0,0]) 
	translate([(BX-25.5)/2-.25, ((40*sqrt(2)) - 36.25 ) / 2-.5, -2.9]) 
	cube(size=[25.5+.5,36.5+.5,3], center=false);
	
	
	translate([BX/2,BY/2,1]) cylinder(h=40, r=filterRadius, center=false, $fn=100);
	translate([BX/2,BY/2,-1]) cylinder(h=40, r=filterRadius, center=false, $fn=100);
    

	rotate([90,0,0])
	translate([BX/2,BY/2,-40-2])
	cylinder(h=40, r=filterRadius-2, center=false, $fn=100);
	///

	//Espacio para cables
	translate([3,0,0])
	cube(size=[3,BY+10,3], center=false);

	translate([BY-6,0,0])
	cube(size=[3,BY+10,3], center=false);

	
}
}

difference(){
    union(){
        rotate([0,0,90]) translate([29,10-w_holder,0]) cube([11,w_holder,40]);
        rotate([0,0,90]) translate([29,-50,0]) cube([11,w_holder,40]);
        
    }
    translate([45,34.,40-depth_holder-50])cylinder(r=r_screw, h=100, $fn=100);
    translate([-5,34,40-depth_holder-50])cylinder(r=r_screw, h=100, $fn=100);
    
    
    rotate([45,0,0]) translate([-15,0,-5]) cube([70,80,40]);
}



}

   module prism(l, w, h){
       polyhedron(
               points=[[0,0,0], [l,0,0], [l,w,0], [0,w,0], [0,w,h], [l,w,h]],
               faces=[[0,1,2,3],[5,4,3,2],[0,4,5,1],[0,3,4],[5,2,1]]
               );
       
       }
   

module filter() {
	

union(){
cube(size=[45,45,45], center=true);
rotate([0,90,0])translate([0,0,30])cylinder(h=20, r=22.5, center=true, $fn=100);
}

}