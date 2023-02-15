import rawpy
import imageio

path = 'image.nef'
with rawpy.imread(path) as raw:
    rgb = raw.postprocess()
imageio.imsave('default.tiff', rgb)
