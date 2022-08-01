run("Close All");
run("Clear Results");

/************* USER-DEFINED PARAMETERS ***********/

pathDATA = File.directory + "../data/";
expeLabel = "Figure_timelapse";
pathSRC="";
/************* DIRECTORY STRUCTURE ***********/

pathSRC = pathDATA + expeLabel;

pathCSV = pathDATA + expeLabel + "/DATA/";
if (!File.exists(pathCSV)) File.makeDirectory(pathCSV);

/************* FOR ALL FILES IN DIRECTORY ***********/

setBatchMode(true);
print(pathSRC + "/Dendritiformis_mask_small.tif");
open(pathSRC + "/Dendritiformis_mask_small.tif");


getPixelSize(unit, pixelw, pixelh); // gets the pixel dimensions
run("Set Measurements...", "area mean min center integrated bounding slice display redirect=None decimal=4");
imageTitle = getTitle();


CenterX = 179; //1170;
CenterY = 162; //1200;


setSlice(1);

x = CenterX / pixelw;
y = CenterY / pixelw; // X and Y position of the center of colony
radius = 10; // radius of the first circle (pixel)
width = 10; // increase of the radius for each iteration

threshold_intensity = 10;

for (k = 1; k < 180; k++) {

	colony_radius = 0;
	setSlice(k);

	x = CenterX / pixelw;
	y = CenterY / pixelw; // X and Y position of the center of colony
	radius = 1; // radius of the first circle (pixel)
	width = 5; // increase of the radius for each iteration

	makeOval(x - radius, y - radius, radius * 2, radius * 2);
	run("Measure"); // here we measure first circle

	for (i = 10; i < 100; i++) {
		radiusb = (radius + (width * i));
		makeOval(x - radiusb, y - radiusb, radiusb * 2, radiusb * 2);
		radiusb -= width;
		setKeyDown("alt");
		makeOval(x - radiusb, y - radiusb, radiusb * 2, radiusb * 2);
		setKeyDown("none");
		run("Measure");


		this_intensity = getResult("Mean", nResults - 1);
		this_radius = getResult("Width", nResults - 1);

		if (this_intensity < threshold_intensity) {
			if (colony_radius == 0) {
				colony_radius = this_radius / 2 - 2 * radius;

				setForegroundColor(255, 93, 239);
				run("Draw", "slice");

			}
		}


	} // draws concentric bands around center of colony
	//print(k + "\t" + colony_radius);
	run("Select None");


}


setBatchMode(false);