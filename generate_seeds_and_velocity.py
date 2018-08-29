import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from scipy import ndimage as ndi
import scipy.ndimage
from skimage import measure
import scipy as sp


def rgb_to_gray(rgb):
	r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
	gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
	return gray

def import_data(name,threshold):
	'''
	import and then binarize data based on threshold
	'''
	im = Image.open(name)
	imarray = np.array(im)
	print np.shape(imarray)
	imarray = rgb_to_gray(imarray)
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
			if data[i][j] > threshold:
				tmp[i][j] = 1.0
	return tmp


def connected_comp(spec , matrix):
	'''
	Take binarized image and find connected components.
	Rearrange them for plotting purposes. 
	'''
	L = sp.ndimage.measurements.label(matrix)[0]
	maxv = np.amax(L)
	perm = np.random.permutation(range(1,maxv+3))
	dup = np.zeros(np.shape(L))
	dim1,dim2 = np.shape(L)
	for i in xrange(dim1):
		for j in xrange(dim2):
			if L[i][j] != 0:
				dup[i][j] = perm[L[i][j]]
	plt.imshow(L,cmap='nipy_spectral',interpolation='none')
	plt.show()
	plt.imshow(dup,cmap='nipy_spectral',interpolation='none')
	plt.title(spec)
	plt.savefig('./Connected_Components_'+spec+'.png', dpi=300,bbox_inches='tight')
	plt.clf()
	return dup

def by_size(mat,thresh):
	maxv = np.amax(mat)
	locs = [[] for i in xrange(int(maxv))]
	dim1,dim2 = np.shape(mat)
	for i in xrange(dim1):
		for j in xrange(dim2):
			if int(mat[i][j]) != 0:
				locs[int(mat[i][j]-1)].append([i,j])
	centroids = []
	for i in xrange(len(locs)):
		if len(locs[i])>thresh:
			xs,ys = np.transpose(np.array(locs[i]))
			dx = np.amax(xs) - np.amin(xs)
			dy = np.amax(ys) - np.amin(ys)
			'''
			Select a point in each component. If over a given size treat as background.
			'''
			if dx > 400 and dy > 400:
				a = range(len(xs))
				a = np.random.permutation(a)
				for j in xrange(5000):
					centroids.append([ys[a[j]],xs[a[j]]])
			else:
				r = np.random.permutation(range(len(xs)))[0]
				cx = np.mean(xs)
				cy = np.mean(ys)
				'''
				Can't use mean for some wings. Some wigns have long, curved domains [neuroptera]
				'''
				#cx = xs[r]
				#cy = ys[r]
				centroids.append([cy,cx]) 
	xt = np.transpose(centroids)[0]
	yt = np.transpose(centroids)[1]
	return np.array(centroids)		

if __name__=='__main__':
	filetodo='./Arigomphus_villosipes_LHW.png'
	spec = filetodo.split('/')[1].split('.')[0]
	data = import_data(filetodo , 0.025)
	objects = connected_comp(spec,1-data)
	np.savetxt('./'+spec+'_vel.csv',1-data,delimiter=',')
	cs = by_size(objects,10)
	np.savetxt(spec+'_cents.txt', cs, delimiter=',')

