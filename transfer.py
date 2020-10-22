import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import PIL


style_transfer = hub.load("https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2")


def load_img(path):
    max_dim = 512
    img = tf.io.read_file(path)
    img = tf.image.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)

    shape = tf.cast(tf.shape(img)[:-1], tf.float32)
    long_dim = max(shape)
    scale = max_dim / long_dim

    new_shape = tf.cast(shape * scale, tf.int32)

    img = tf.image.resize(img, new_shape)
    img = img[tf.newaxis, :]
    return img


def save_img(img):
    img = img * 255
    img = np.array(img, dtype=np.uint8)
    img = img[0]
    img = PIL.Image.fromarray(img)
    img.save("result.jpg", "JPEG")


def transfer():
    content = load_img("content.jpg")
    style = load_img("style.jpg")

    result = style_transfer(tf.constant(content), tf.constant(style))[0]
    save_img(result)
