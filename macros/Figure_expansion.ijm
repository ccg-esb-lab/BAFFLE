run("Close All");
run("Clear Results");

/************* USER-DEFINED PARAMETERS ***********/

pathDATA = File.directory+"../data/";
expeLabel = "Figure_expansion";

/************* DIRECTORY STRUCTURE ***********/

pathSRC = pathDATA + expeLabel;

pathCSV = pathDATA + expeLabel + "/DATA/";
if (!File.exists(pathCSV)) File.makeDirectory(pathCSV);

/************* FOR ALL FILES IN DIRECTORY ***********/

setBatchMode(false);

//**** GFP ****//

open(pathSRC + "/Consortium_green.tif");
rename('GFP');


getPixelSize(unit, pixelw, pixelh); // gets the pixel dimensions
run("Set Measurements...", "area mean min center integrated bounding slice display redirect=None decimal=4");
imageTitle = getTitle();


CenterX = 1820;
CenterY = 1820; //1200;


x = CenterX / pixelw;
y = CenterY / pixelw; // X and Y position of the center of colony
radius = 10; // radius of the first circle (pixel)
width = 10; // increase of the radius for each iteration


makeOval(x - radius, y - radius, radius * 2, radius * 2);
run("Measure"); // here we measure first circle

for (i = 1; i < 25; i++) {
    radiusb = (radius + (width * i));
    makeOval(x - radiusb, y - radiusb, radiusb * 2, radiusb * 2);
    radiusb -= width;
    setKeyDown("alt");
    makeOval(x - radiusb, y - radiusb, radiusb * 2, radiusb * 2);
    setKeyDown("none");
    run("Measure");


} // draws concentric bands around center of colony
run("Select None");

selectWindow("Results");

saveAs("Results", pathCSV + "Results_GFP.csv");


