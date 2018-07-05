MANUSCRIPT NAME
Jordan Hoffmann, Seth Donoughe, Kathy Li, Mary Salcedo, L. Mahadevan, Chris H. Rycroft
***************************************************************
Wing Segmentation and Circularity Optimization Code
Code Written By Jordan Hoffmann, Seth Donoughe, Kathy Li
===============================================================



Contents
===============================================================
All code used in the manuscript is available upon request. Here we provide
basic code that segments and runs out routine on an example wing.

Segment Wing Image 
	-Code and example wing used to segment wings in the manuscript.
Optimization
	-Code used to perform area-weighted circularity optimization



Code Requirements
===============================================================
	All Python Code Python v 2.7
	Anaconda makes installing all packages easy.
	All Mathematica code works in Mathematica 10 and 11
	Dependencies:
		numy, scipy, Pillow, matplotlib
		scikit-fmm [https://github.com/scikit-fmm/scikit-fmm]
		scikit-image [http://scikit-image.org/]
	Installation of dependencies on clean Ubuntu build
		pip install numpy
		pip install scipy
		pip install Pillow
		pip install matplotlib
		pip install scikit-fmm
		pip install scikit-image
	Code can be easily parallelized to run on many wing images simultaneously using
		mpi4py
		glob


Running the code
===============================================================
Once dependencies installed:
>>> cd Segment_Wing_Image
>>> python generate_seeds_and_velocity.py
>>> python segment.py
>>> python mask_image.py
>>> cd ..
Open Mathematica Notebook for Polygonization and Optimization routines.





