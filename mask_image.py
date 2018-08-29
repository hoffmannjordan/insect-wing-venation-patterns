import numpy as np
from PIL import Image
#from scipy import ndimage as ndi
import scipy.ndimage
from scipy import ndimage
from skimage import measure


def rgb2gray(rgb):
	r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
	gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
	return gray

	
def import_data(name,cutoff):
	'''
	Import the data.
	'''
	im = Image.open(name)
	imarray = np.array(im)
	print np.shape(imarray)
	imarray = rgb2gray(imarray)
	imarray = scipy.ndimage.filters.gaussian_filter(imarray,0.55)
	print np.shape(imarray)
	dim1,dim2 = np.shape(imarray)
	data = np.zeros((dim1,dim2))
	for i in xrange(dim1):
		for j in xrange(dim2):
			data[i][j] = 1-imarray[i][j]
	data += np.abs(np.amin(data))
	data = data/np.amax(data)
	tmp = np.zeros(np.shape(data))
	for i in xrange(dim1):
		for j in xrange(dim2):
			if data[i][j] > cutoff:
				tmp[i][j] = 1.0
	return tmp


def grow_mask(start_positionx, start_positiony):
	'''
	Grow the mask.
	'''
	a,b = np.shape(tmp)
	checked = {}
	to_check = []
	to_check.append([start_positionx, start_positiony])
	while len(to_check) != 0:
		next_to_checkx, next_to_checky = to_check.pop(0)
		if not (checked.get(tuple([next_to_checkx, next_to_checky]), None)) and (tmp[next_to_checkx, next_to_checky] == 0):
			if next_to_checkx+1 < a:
				to_check.append([next_to_checkx+1, next_to_checky])
			if next_to_checky+1 < b:
				to_check.append([next_to_checkx, next_to_checky+1])
			if next_to_checkx-1 >= 0:
				to_check.append([next_to_checkx-1, next_to_checky])
			if next_to_checky-1 >= 0:
				to_check.append([next_to_checkx, next_to_checky-1])
			checked[tuple([next_to_checkx, next_to_checky])] = True
			tmp2[next_to_checkx, next_to_checky] = 0
			print "length of to check:", len(to_check)
			print "length of checked:", len(checked)
	return tmp2

def refine_mask(data, mask):
	'''
	Ensure that all pixels of removed points.
	'''
	mask2 = np.copy(mask)
	xs,ys = np.where(mask == 0)
	print 'STARTED WITH '+str(len(xs))
	tocheck = []
	for i in xrange(len(xs)):
		tocheck.append(data[xs[i]][ys[i]])
	tocheck = np.unique(tocheck)
	print 'to check is: \n'
	print 'tocheck ids:', tocheck
	dim1 , dim2 = np.shape(data)
	for i in xrange(dim1):
		for j in xrange(dim2):
			if data[i][j] in tocheck:
				mask2[i][j] = 0
	xs,ys = np.where(mask2 == 0)
	print 'ENDED WITH '+str(len(xs))
	return mask2

if __name__=='__main__':
	filetodo = './Arigomphus_villosipes_LHW_FMM_seg.csv'
	orig_data_scan = np.genfromtxt(filetodo, delimiter=',')
	orig_data_scan = np.asarray(orig_data_scan)
	orig_data_scan = orig_data_scan.astype(int)
	grayscale_data_scan = import_data('./Arigomphus_villosipes_LHW.png',0.025)
	tmp = grayscale_data_scan
	tmp2 = np.ones(np.shape(orig_data_scan))
	mask = grow_mask(0, 0)
	print "DID MASK"
	mask = refine_mask(orig_data_scan,mask)
	new_file = np.multiply(mask, orig_data_scan)
	np.savetxt('./L_HW_masked.csv', new_file.astype(int), fmt='%i', delimiter=',')