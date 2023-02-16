import rawpy
import imageio

path = 'tests/assets/600A9641.CR3'
with rawpy.imread(path) as raw:
    params = rawpy.Params(
        use_camera_wb=True,
        exp_shift=3.0,
        #highlight_mode=rawpy.HighlightMode.Blend,
    )
    rgb = raw.postprocess(params=params)
imageio.imsave('cr3-to.tiff', rgb)
