import tkinter as tk
import h5py
from PIL import Image, ImageTk
import numpy as np
import imageio
import scipy.io as sio

frame_index = 0

def make_square(im, min_size=256, fill_color=(0, 0, 0, 0)):
    x, y = im.size
    size = max(min_size, x, y)
    new_im = Image.new('RGBA', (size, size), fill_color)
    new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))
    return new_im

cord_all = []
frame_image_resize_array_all = []

def stream(label, offset=0):
    global frame_index
    try:

        image = video.get_data(frame_index+offset)
        image_frame = Image.fromarray(image)
        frame_image_resize = make_square(image_frame)
        frame_image_resize_squared = frame_image_resize.resize((512, 512), Image.ANTIALIAS)
        frame_image = ImageTk.PhotoImage(frame_image_resize_squared)
        label.config(image=frame_image)
        label.image = frame_image
        canvas.create_image(0, 0, image=frame_image, anchor="nw")
        frame_index += offset
        if frame_index>0:
            abs_coord_x = root.winfo_pointerx() - root.winfo_rootx()
            abs_coord_y = root.winfo_pointery() - root.winfo_rooty()
            if abs_coord_y <=10:
                abs_coord_y = 0
            if abs_coord_x<=10:
                abs_coord_x = 0

            print ('pipe coordinate:', abs_coord_x, abs_coord_y)
            cord = [abs_coord_x, abs_coord_y]
            cord_all.append(cord)
            frame_image_resize_array = np.asarray(frame_image_resize_squared)
            frame_image_resize_array_all.append(frame_image_resize_array)
            vid_name = video_name.split('.mp4')[0]
            file_to_save = vid_name.split('/')[-1]
            hf = h5py.File('./data_' + str(file_to_save) + '.h5', 'w')
            hf.create_dataset('coordinates', data=cord_all)
            hf.create_dataset('frames', data=frame_image_resize_array_all)
            hf.close()
            save_file_name = './tmp/data_' + str(file_to_save)+'_'+str(frame_index) + '.mat'
            data = {}
            data['image'] = frame_image_resize_array
            data['cord'] = cord
            sio.savemat(save_file_name, data)

    except Exception as ex:
        print('Error loading frame:', ex)

if __name__ == "__main__":
    print ('If you do not see any pipe in the image,' '\nplease click on the top left side of the image')
    video_name = './' # path to the video
    video = imageio.get_reader(video_name, fps = 2)
    root = tk.Tk()
    my_label = tk.Label(root,  width=512, height=512)
    canvas = tk.Canvas(my_label, width=511, height=511, bg='white')
    canvas.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
    my_label.bind("<Button-1>", lambda e: stream(my_label, +1))
    my_label.bind("<Button-3>", lambda e: stream(my_label, -1))
    canvas.bind("<Button-1>", lambda e: stream(my_label, +1))
    my_label.pack()
    stream(my_label)
    root.mainloop()
    video.close()
