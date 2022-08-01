
run("Close All");
run("Clear Results");

/************* USER-DEFINED PARAMETERS ***********/

pathDATA = File.directory+"../data/";
IJ.log(pathDATA)
expeLabel = "Figure_calibration";

/************* DIRECTORY STRUCTURE ***********/

pathSRC=pathDATA+expeLabel;
setBatchMode(true);

/************* DARK ***********/

open(pathSRC + "/plate_DARK.jpg");
run("8-bit");
rename("DARK");
saveAs("Tiff", pathSRC+"/od_DARK.tif");

/************* GFP ***********/

open(pathSRC + "/plate_GFP.jpg");
run("Split Channels");

selectWindow("plate_GFP.jpg (blue)");
close();
selectWindow("plate_GFP.jpg (red)");
close();

open(pathSRC + "/bg_GFP.jpg");
run("Split Channels");

imageCalculator("Subtract create", "plate_GFP.jpg (green)","bg_GFP.jpg (green)");
selectWindow("Result of plate_GFP.jpg (green)");
rename("GFP");
saveAs("Tiff", pathSRC+"/od_GFP.tif");

selectWindow("bg_GFP.jpg (blue)");
close();
selectWindow("bg_GFP.jpg (red)");
close();
selectWindow("bg_GFP.jpg (green)");
close();

selectWindow("plate_GFP.jpg (green)");
close();


/************* RFP ***********/

open(pathSRC + "/plate_RFP.jpg");
run("Split Channels");

selectWindow("plate_RFP.jpg (blue)");
close();
selectWindow("plate_RFP.jpg (green)");
close();

open(pathSRC + "/bg_RFP.jpg");
run("Split Channels");

imageCalculator("Subtract create", "plate_RFP.jpg (red)","bg_RFP.jpg (red)");
selectWindow("Result of plate_RFP.jpg (red)");
rename("RFP");
saveAs("Tiff", pathSRC+"/od_RFP.tif");

selectWindow("bg_RFP.jpg (blue)");
close();
selectWindow("bg_RFP.jpg (green)");
close();
selectWindow("bg_RFP.jpg (red)");
close();

selectWindow("plate_RFP.jpg (red)");
close();


/************* RFP ***********/

open(pathSRC + "/plate_CFP.jpg");
run("Split Channels");

selectWindow("plate_CFP.jpg (red)");
close();
selectWindow("plate_CFP.jpg (green)");
close();

open(pathSRC + "/bg_CFP.jpg");
run("Split Channels");

imageCalculator("Subtract create", "plate_CFP.jpg (blue)","bg_CFP.jpg (blue)");
selectWindow("Result of plate_CFP.jpg (blue)");
rename("CFP");
saveAs("Tiff", pathSRC+"/od_CFP.tif");

selectWindow("bg_CFP.jpg (red)");
close();
selectWindow("bg_CFP.jpg (green)");
close();
selectWindow("bg_CFP.jpg (blue)");
close();

selectWindow("plate_CFP.jpg (blue)");
close();


/************* YFP ***********/
open(pathSRC + "/plate_YFP.jpg");
run("Split Channels");


selectWindow("plate_YFP.jpg (blue)");
close();
selectWindow("plate_YFP.jpg (red)");
close();

open(pathSRC + "/bg_YFP.jpg");
run("Split Channels");

imageCalculator("Subtract create", "plate_YFP.jpg (green)","bg_YFP.jpg (green)");
selectWindow("Result of plate_YFP.jpg (green)");
rename("YFP");
saveAs("Tiff", pathSRC+"/od_YFP.tif");

selectWindow("bg_YFP.jpg (blue)");
close();
selectWindow("bg_YFP.jpg (red)");
close();
selectWindow("bg_YFP.jpg (green)");
close();

selectWindow("plate_YFP.jpg (green)");
close();




setBatchMode(false);