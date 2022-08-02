
/************* USER-DEFINED PARAMETERS ***********/
min_area = 100;
x_box=1059;
y_box=44;
width_box=3849;
height_box=3849;


pathDATA = File.directory+"../data/";
expeLabel = "Figure_colonies";

/************* DIRECTORY STRUCTURE ***********/

pathSRC=pathDATA+expeLabel;
pathGFP=pathDATA+expeLabel+"/GFP/";
pathBRIGHT=pathDATA+expeLabel+"/BRIGHT/";
pathALL=pathDATA+expeLabel+"/ALL/";
pathTYPE=pathDATA+expeLabel+"/TYPE/";
pathOVERLAY=pathDATA+expeLabel+"/OVERLAY/";
pathMONTAGE=pathDATA+expeLabel+"/MONTAGE/";
pathCSV=pathDATA+expeLabel+"/DATA/";

if (!File.exists(pathGFP)) File.makeDirectory(pathGFP);
if (!File.exists(pathBRIGHT)) File.makeDirectory(pathBRIGHT);
if (!File.exists(pathALL)) File.makeDirectory(pathALL);
if (!File.exists(pathTYPE)) File.makeDirectory(pathTYPE);
if (!File.exists(pathOVERLAY)) File.makeDirectory(pathOVERLAY);
if (!File.exists(pathCSV)) File.makeDirectory(pathCSV);
if (!File.exists(pathMONTAGE)) File.makeDirectory(pathMONTAGE);

f_data = File.open(pathCSV+"data.txt"); 
print(f_data, "pathBRIGHT\t pathGFP\t coloniesBRIGHT\t coloniesGFP");

/************* FOR ALL FILES IN DIRECTORY ***********/

setBatchMode(true);

list = getFileList(pathSRC);
for (i=0; i<list.length; i++){  //
	
	file_BRIGHT='';
	if(i<list.length)
		if(endsWith(list[i], 'JPG')){
			file_BRIGHT=list[i];
		}

	i=i+1;
	file_GFP='';
	if(i<list.length)
		if(endsWith(list[i], 'JPG'))
			file_GFP=list[i];

	if(file_GFP!="" && file_BRIGHT!=""){
		/************* BRIGHT ***********/
		print("Loading "+pathSRC + "/" + file_BRIGHT);
		open(pathSRC + "/" + file_BRIGHT);
		run("8-bit");
		run("Subtract Background...", "rolling=50 light");
		setThreshold(0, 250);
		run("Threshold...");
		run("Convert to Mask");
		run("Gaussian Blur...", "sigma=2");
		makeRectangle(x_box, y_box, width_box, height_box);
		setOption("BlackBackground", false);
		setBackgroundColor(0,0,0);
		run("Clear Outside");
		run("Convert to Mask");
		run("Analyze Particles...", "size="+min_area+"-10000 circularity=0.50-1.00 show=[Masks] display add");
		setThreshold(0, 250);
		run("Convert to Mask");
		run("Invert");
		run("Watershed");
		rename("BRIGHT_colonies");
		run("Select All");
		roiManager("Deselect");
		roiManager("Delete");
		
		selectWindow("BRIGHT_colonies");
		run("8-bit");
		saveAs("Tiff", pathBRIGHT+file_BRIGHT);
		rename("BRIGHT_colonies");
		
		/************* GFP ***********/
		
		open(pathSRC + "/" + file_GFP);
		run("8-bit");
		rename("GFP");
		run("Auto Local Threshold", "method=Bernsen radius=15 parameter_1=0 parameter_2=0 white");
		run("Convert to Mask");
		run("Fill Holes");
		run("Gaussian Blur...", "sigma=5");
		setOption("BlackBackground", true);
		run("Gaussian Blur...", "sigma=5");
		run("Make Binary");
		makeRectangle(x_box, y_box, width_box, height_box);
		setBackgroundColor(0,0,0);
		run("Clear Outside");
		run("Make Binary");
		run("Analyze Particles...", "size="+min_area+"-10000 circularity=0.70-1.00 show=Masks display add");
		rename("GFP_colonies");
		
		setThreshold(0, 250);
		run("Convert to Mask");
		run("Invert");
		run("Watershed");
		selectWindow("GFP_colonies");
		run("8-bit");
		saveAs("Tiff", pathGFP+file_GFP);
		rename("GFP_colonies");
		
		
		/************* MASK (ALL COLONIES) ***********/
		
		setBackgroundColor(255,255,255);
		imageCalculator("OR create", "BRIGHT_colonies", "GFP_colonies");
		selectWindow("Result of BRIGHT_colonies");
		rename("ALL_colonies");
		run("Convert to Mask");
		run("Analyze Particles...", "size="+min_area+"-10000 circularity=0.20-1.00 show=Nothing display clear add");
		
		selectWindow("ALL_colonies");
		run("Invert");
		run("8-bit");
		saveAs("Tiff", pathALL+file_BRIGHT);
		rename("ALL_colonies");
		
		if (isOpen("Results")) {
		    selectWindow("Results");
		    run("Close");
		}

		imageCalculator("XOR create", "ALL_colonies", "GFP_colonies");
		rename("NONGFP_colonies");
		
		saveAs("Tiff", pathTYPE+file_BRIGHT);
		close();
		
		/************* OBTAIN STATISTICS ***********/
		
		num_type1 = 0;
		num_type2 = 0;
		
		//Now loop roi manager and color roi based on val
		n = roiManager("count");
		for (iRoi = 0; iRoi < n; iRoi++) {
		
		    roiManager("select", iRoi);
		
		    selectWindow("GFP_colonies");
		    roiManager("Measure");
		
		    area = getResult("Area", iRoi);
		    maxval = getResult("Max", iRoi);
		    if (area < min_area) {
		        type = 0; //Pseudocolonies
		        fillColor="#FFFFFF";
		    	roiManager("Set Fill Color", fillColor);
		    } else {
		        if (maxval > 0) {
		            type = 2;
		            num_type1 = num_type1 + 1;
			        fillColor="#009E4A";
			    	roiManager("Set Fill Color", fillColor);
		        } else {
		            type = 1;
		            num_type2 = num_type2 + 1;
			        fillColor="#6B0E69";
			    	roiManager("Set Fill Color", fillColor);
		        }
		    }
		    setResult("Type", iRoi, type);
		}
		
		selectWindow("ALL_colonies");
		roiManager("Show All without labels");
		run("Flatten");
		saveAs("Tiff", pathTYPE+file_BRIGHT);
		
		/*********** OVERLAY ************/
		
		open(pathSRC + "/" + file_BRIGHT);
		rename("OVERLAY_colonies");
		
		roiManager("Show All without labels");
		selectWindow("OVERLAY_colonies");
		run("Flatten");
		saveAs("Tiff", pathOVERLAY+file_BRIGHT);
		
		/*********** EXPORT DATA ************/
		
		fileCSV=substring(file_BRIGHT, 0, lastIndexOf(file_BRIGHT, "."));
		saveAs("Results", pathCSV+""+fileCSV+".csv");
		IJ.log("Exporting "+fileCSV+".csv");
		
		print(f_data, file_BRIGHT+"\t "+file_GFP+"\t "+num_type2+"\t "+num_type1);
		run("Close All");

		
	}
	
}

/************* FOR ALL FILES IN BRIGHT DIRECTORY ***********/

setBatchMode(true);
list = getFileList(pathSRC);

for (i=0; i<list.length; i++){
	file_BRIGHT='';
	if(i<list.length)
		if(endsWith(list[i], 'JPG'))
			file_BRIGHT=list[i];

	i=i+1;
	file_GFP='';
	if(i<list.length)
		if(endsWith(list[i], 'JPG'))
			file_GFP=list[i];

	if(file_GFP!="" && file_BRIGHT!=""){
	
		open(pathSRC + "/" + file_BRIGHT);
		open(pathSRC + "/" + file_GFP);
		
		open(pathOVERLAY + "/" + file_BRIGHT);


		run("Images to Stack", "name=Stack title=[] use");
		run("Make Montage...", "columns=3 rows=1 scale=0.25");
		selectWindow("Stack");
		close();
		
		selectWindow("Montage");
		saveAs("TIF", pathMONTAGE+file_BRIGHT);
		close();

	}
	
}

IJ.log("Finished");
setBatchMode(false);
