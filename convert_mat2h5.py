import scipy.io as sio
import os
import h5py

all_mat = os.listdir('./tmp/')
all_mat_sorted = sorted(all_mat)
file_name = all_mat_sorted[0].split('.')[0][:-1]
cord_all = []
image_all = []
# import ipdb;ipdb.set_trace()
for i in range(1, len(all_mat_sorted)):
    data = sio.loadmat('./tmp/'+file_name+str(i)+'.mat')
    print (file_name+str(i)+'.mat')
    cord= data['cord']
    image = data['image']
    image_all.append(image)
    cord_all.append(cord)
hf = h5py.File('./data_' + str(file_name) + '.h5', 'w')
hf.create_dataset('coordinates', data=cord_all)
hf.create_dataset('images', data=image_all)
hf.close()

