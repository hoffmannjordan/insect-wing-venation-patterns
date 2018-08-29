import skfmm
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage as ndi
import scipy.ndimage
from scipy import ndimage
from PIL import Image

def rgb_to_gray(rgb):
	r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
	gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
	return 1-gray

def read_in_frame(filename):
	'''
	This function reads in an image, converts it to gray scale, and returns the data
	'''
	im = Image.open(filename)
	imarray = np.array(im)
	imarray = rgb_to_gray(imarray)
	imarray = scipy.ndimage.filters.gaussian_filter(imarray,0.55)
	print np.shape(imarray)
	dim1,dim2 = np.shape(imarray)
	data = np.zeros((dim1,dim2))
	for i in xrange(dim1):
		for j in xrange(dim2):
			data[i][j] = 1-imarray[i][j]
	data += np.abs(np.amin(data))
	return data/np.amax(data)

def expand(i,j,tmp3,dx,dy):
	'''
	Helper function for the segmentation code.
	'''
	toreturn=[]
	if i < (dx-1) and tmp3[i+1][j] == 0:
		toreturn.append((i+1,j))
	if j<(dy-1) and tmp3[i][j+1] == 0:
		toreturn.append((i,j+1))
	if i > 0 and tmp3[i-1][j] == 0:
		toreturn.append((i-1,j))
	if j > 0 and tmp3[i][j-1] == 0:
		toreturn.append((i,j-1))
	return toreturn

def segmentation3(filename,cx,cy,dx,dy,times):
	'''
	This code does the bulk of the heavy lifting. 
	'''
	iterator = 0 
	file_counter = 0
	x = np.arange(0, dy)
	y = np.arange(0, dx)
	X, Y = np.meshgrid(x, y)
	tmp = np.zeros((dx,dy))
	print 'Initilializing'
	shuffler = range(len(cx))
	shuffler = np.random.permutation(shuffler)
	for i in xrange(len(cx)):
		tmp[cy[i]][cx[i]] = shuffler[i]+1
	todo = []
	for i in xrange(len(cx)):
		todo.append(expand(int(cy[i]),int(cx[i]),tmp,dx,dy))
	print 'made to do'
	tmin= np.amin(times)
	tmax= np.amax(times)
	t = 0
	dt = 0.025*10
	#increase time step if later, if wanted. Speeds up calculation, may lose small accruacy. Not 
	# used in the manuscript segmentation.
	speed_up = True
	if speed_up == True:
		upper_t = (tmax + 1) + 5
	else:
		upper_t = tmax+1
	while t< upper_t:
		if speed_up == True:
			if t > 200: #to ensure small cells segment accurately
				dt = dt * 1.0005
		tmp2 = np.copy(tmp)
		lens = [ len(list(set(todo[i]))) for i in xrange(len(todo))]
		tmp_list = [[] for i in xrange(len(cx))]
		shuffler_for_order = range(len(cx))
		shuffler_for_order = np.random.permutation(shuffler_for_order)
		for ii in range(len(cx)):
			i = shuffler_for_order[ii]
			list_to_do = list(set(todo[i]))
			if list_to_do != []:
				for j in xrange(len(list_to_do)):
					if times[list_to_do[j][0],list_to_do[j][1]] < t and tmp[list_to_do[j][0],list_to_do[j][1]]==0:
						tmp[list_to_do[j][0],list_to_do[j][1]] = shuffler[i]+1
						addon = expand(list_to_do[j][0],list_to_do[j][1],tmp2,dx,dy)
						if addon != []:
							for k in range(len(addon)):
								tmp_list[i].append(addon[k])
					elif times[list_to_do[j][0],list_to_do[j][1]] > t:
						tmp[list_to_do[j][0],list_to_do[j][1]] = 0
						tmp_list[i].append(list_to_do[j])
		todo = tmp_list[:]
		iterator += 1
		t+=dt
		print m,t,tmax
		#can save intermediate results if wanted.
		save_int = True
		save_freq = 100
		if save_int:
			if iterator%save_freq == 0:
				np.savetxt('./'+filename+'_FMM_seg.csv',tmp.astype(int), fmt='%i',delimiter=',')
	np.savetxt('./'+filename+'_FMM_seg.csv',tmp.astype(int), fmt='%i',delimiter=',')



def read_in_centroids(filename):
	'''
	Read in centroids from the previous code. Ensure they are integers.
	'''
	cx = []
	cy = []
	with open('./'+filename+'_cents.txt') as f:
		for line in f:
			data = line.split(',')
			cx.append(int(float(data[0])))
			cy.append(int(float(data[1])))
	return cx,cy
	
					
if __name__=='__main__':
	filetodo = './Arigomphus_villosipes_LHW.png'
	filename = filetodo.split('/')[1].split('.')[0]
	slice2 = read_in_frame(filetodo)
	slice2 = scipy.ndimage.filters.gaussian_filter(slice2,2)
	a,b = np.shape(slice2)
	cx,cy = read_in_centroids(filename)
	plt.imshow(slice2,cmap='hot')
	plt.plot(cx,cy,'bo',markersize=3)
	plt.title('Raw Data and Seeds')
	plt.xlim([0,b])
	plt.ylim([0,a])
	plt.show()
	plt.savefig('./Raw_Data_and_Seeds.png', dpi=300,bbox_inches='tight')
	plt.clf()
	'''
	Use fmm packaged to set up travel time matrix
	'''
	fmm = np.ones((a, b))
	for i in xrange(len(cx)):
		x1 = int(cx[i])
		y1 = int(cy[i])
		fmm[y1][x1] = -1
	print np.sum(fmm)
	dist_mat = skfmm.distance(fmm)
	speed=np.genfromtxt('./'+filename+'_vel.csv',delimiter=',')+0.0025 #added to make veins have small velocity
	speed=scipy.ndimage.filters.gaussian_filter(speed,0.35)
	slice3 = read_in_frame(filetodo)
	print np.shape(slice3)
	dim1,dim2 = np.shape(slice3)
	for m in xrange(dim1):
		for n in xrange(dim2):
			if slice3[m][n] == 0.0:
				speed[m][n] = 1.0
	print np.amax(speed)
	print np.amin(speed)
	t = skfmm.travel_time(fmm, speed)
	plt.imshow(t,cmap='hot')
	plt.show()
	plt.plot(cx,cy,'bo',markersize=3)
	plt.title('Travel Time and Seeds')
	plt.xlim([0,b])
	plt.ylim([0,a])
	plt.show()
	plt.savefig('./Travel_Time.png', dpi=300,bbox_inches='tight')
	plt.clf()
	'''
	Segment image based on travel time matrix
	'''
	segmentation3(filename,cx,cy,a,b,t)


