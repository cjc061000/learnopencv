import random
import os
import subprocess
import sys
from PIL import Image

def add_bound_box_data(image_file,label_file):
    im=Image.open(image_file)
    width,height = im.size
    with open(label_file, 'r') as f:
        output = ' '
        for line in f:
            vals = line.split()
            vals = [float(a) for a in vals[1:]]+vals[:1]
            bb = [(vals[0]-vals[2]/2)*width,(vals[1]-vals[3]/2)*height,(vals[0]+vals[2]/2)*width,(vals[1]+vals[3]/2)*height,vals[4]]
            output += ','.join([str(a) for a in bb])
            output += ' '
    return output

def split_data_set(image_dir):

    labels_dir = image_dir.replace('JPEGImages','labels')

    f_val = open("shoe_test.txt", 'w')
    f_train = open("shoe_train.txt", 'w')
    
    path, dirs, files = next(os.walk(image_dir))
    data_size = len(files)

    ind = 0
    data_test_size = int(0.1 * data_size)
    test_array = random.sample(range(data_size), k=data_test_size)
    
    for f in os.listdir(image_dir):
        if(f.split(".")[1] == "jpg"):
            ind += 1
            
            if ind in test_array:
                f_val.write(image_dir+'/'+f+add_bound_box_data(image_dir+'/'+f,labels_dir+'/'+f.replace('jpg','txt'))+'\n')
            else:
                f_train.write(image_dir+'/'+f+add_bound_box_data(image_dir+'/'+f,labels_dir+'/'+f.replace('jpg','txt'))+'\n')


split_data_set(sys.argv[1])