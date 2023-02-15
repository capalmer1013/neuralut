import rawpy
import imageio

path = 'tests/assets/600A9641.CR3'
with rawpy.imread(path) as raw:
    rgb = raw.postprocess()
imageio.imsave('cr3-to.tiff', rgb)
