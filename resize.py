from os import listdir
from PIL import Image

IMAGE_DIR = 'img_in/'
OUT_DIR = 'img_out/'

WIDTH = 800
HEIGHT = 480

def resized_dimensions(w, h):
  big_dimension = max(w, h)

  if w > h:
    new_w = int(w * (big_dimension / h))
    return (new_w, big_dimension)
  else:
    new_h = int(h * (big_dimension / w))
    return (big_dimension, new_h)

for filename in listdir(IMAGE_DIR):
  image = Image.open(IMAGE_DIR + filename)

  w, h = image.size
  new_w, new_h = resized_dimensions(w, h)

  ratio = min(WIDTH / w, HEIGHT / h)
  if ratio < 1.0:
    w = int(w * ratio)
    h = int(h * ratio)
    image = image.resize((w, h))
  scaled_w, scaled_h = (WIDTH - new_w) // 2, (HEIGHT - new_h) // 2

  image = image.resize((new_w, new_h))
  out_image = Image.new("RGB", (WIDTH, HEIGHT), color=(255, 255, 255))
  out_image.paste(image, (scaled_w, scaled_h))

  jpg_filename = filename.replace('.png', '.jpg')
  out_image.save(OUT_DIR + jpg_filename, 'jpeg')
  # image.save(OUT_DIR + jpg_filename, 'jpeg')
