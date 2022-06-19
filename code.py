import os
import cv2
import csv
from PIL import Image
import numpy as np


# фунцкия для получения данных из файла "description.csv"
# возвращает массив трех элементов: индекс, цвет, путь до изображения
def get_imgs_data(input_dir):
    file_name = 'description.csv'
    imgs_data_dir = os.path.join(input_dir , file_name)
    imgs_data = []
    names = []
    with open(imgs_data_dir) as file_obj:
        heading = next(file_obj)
        reader_obj = csv.reader(file_obj)
        for row in list(reader_obj):
            name = row[2]
            name_idx = name.index('_')
            name = name[:name_idx]
            names.append(name)
            row[2] = os.path.join('./input/data' , row[2])
            imgs_data.append(row)
    return imgs_data, names

# функция возвращает пути до изображений
def get_imgs_dirs(input_dir):
    names = []
    dirs = []
    names = os.listdir(input_dir)
    for name in names:
        dirs.append(os.path.join(input_dir , name))
    return dirs

# функция считывает и возвращает количество изображений из файла "image_counter.txt"
def read_imgs_count(input_dir):
    file_name = 'image_counter.txt'
    count_imgs_dir = os.path.join(input_dir , file_name)
    with open(count_imgs_dir) as f:
        return int(f.read())

# функция для соединения r, g, b изображений в одно
def merge_channels(input_dir, output_dir):
    imgs_data, names = get_imgs_data(input_dir)
    count_imgs = read_imgs_count(input_dir)
    ext = '.jpg'
    imgs = []
    count = 3 * count_imgs # количество всех изображений в data
    for i in range(count):
        color_letter = imgs_data[i][1]
        path = imgs_data[i][2]
        img = cv2.imread(os.path.join(path))
        b,g,r = cv2.split(img)
        if color_letter == 'r':
            imgs.append(r)
        if color_letter == 'g':
            imgs.append(g)
        if color_letter == 'b':
            imgs.append(b)
        if len(imgs) == 3:
            merged = cv2.merge(imgs)
            cv2.imwrite(os.path.join(output_dir , f'{names[i]}{ext}' ),merged)
            imgs = []

# функция вычисляет доминирующий цвет на области изображения
# в формате (r, g, b)
def calc_metric(image, x, y, w, h):
    r_total = 0
    g_total = 0
    b_total = 0

    count = 0
    for x_coord in range(x, w):
        for y_coord in range(y, h):
            b, g, r = image.getpixel((x_coord,y_coord))
            r_total += r
            g_total += g
            b_total += b
            count += 1

    return (r_total/count, g_total/count, b_total/count)

# функция для визуализации доминирующего цвета на изображении
# результат записывается в папку 'images'
def visualize_img_with_dominant_color(img_dir, dominant_color, h, w):
    img = cv2.imread(img_dir)
    dominant_color_img = np.zeros((h,w,3), np.uint8)
    dominant_color_img[:] = dominant_color
    vis = cv2.hconcat([img, dominant_color_img])
    output_dir = './images'
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    ext = '.jpg'
    name_idx = img_dir.index('\\') + 1
    name = img_dir[name_idx:]
    cv2.imwrite(os.path.join(output_dir , f'{name}{ext}' ),vis)

# функция для вычисления и вызуализации доминирующего цвет
# на всех изображениях из папки input
def find_dominant_color(input_dir, x, y):
    output_dir = './output'
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    print("merging channels...")
    merge_channels(input_dir, output_dir)
    print("finished merge")
    count_imgs = read_imgs_count(input_dir)
    imgs_dirs = get_imgs_dirs(output_dir)

    print("finding dominant colors...")
    for i in range(count_imgs):
        img = Image.open(imgs_dirs[i])
        width, height = img.size
        dominant_color = calc_metric(img,x,y,width,height)
        visualize_img_with_dominant_color(imgs_dirs[i],dominant_color,height,100)
        print(f"picture {i} is done")
    print("see result in 'images' folder")
    
input_dir = './input'
x = 0
y = 0
find_dominant_color(input_dir, x, y)


