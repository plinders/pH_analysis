//Generate ROIs for ratiometric calculation
//User adds cells to ROI manager by drawing a ROI first

n_cell = roiManager("count"); //Count number of cells to be processed
windowname = getTitle(); //Get title of original image
dir = getDirectory("image"); //Get directory of original image
cell_array = newArray(); //Initiate array to store names of generate cell images

selectWindow(windowname);
//Extract series name from filename + window title
filename = getInfo("image.filename");
seriesname = substring(windowname, lengthOf(filename) + 3, lengthOf(windowname));

//Save ROIs to zip so they can be reused later
//roiManager("Save", dir+"\\"+seriesname+"_ROIs.zip");

//Generate single cell images from user-defined ROIs
for (i=0; i < n_cell; i++) {
	roiManager("Select", i);
	name = seriesname+"_cell"+i+1;
	run("Duplicate...", "duplicate");
	rename(name); //Renames new image to <seriesname>_cell_<number>
	run("Clear Outside", "stack"); //remove content outside original ROI
		// cell_array = Array.concat(cell_array, name); //Add name of new cell image to array
	File.makeDirectory(dir+"\\"+name);
	saveAs("Tiff", dir+"\\"+name+"\\"+name);
	close();
	selectWindow(windowname);
}
//Remove ROIs
roiManager("Reset");

