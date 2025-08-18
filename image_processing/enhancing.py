# ================================== All Libraries ==================================
# ===================================================================================

# Other Necessary Libraries
import numpy as np

# ================================= Image Enhancing =================================
# ===================================================================================

########################################################## Hist Equalization
########################################################## For Global
def histEqualization(channel: np.ndarray) -> np.ndarray:
    hist, _ = np.histogram(channel.flatten(), 256, [0, 255])
    cdf = hist.cumsum()
    cdf_norm = ((cdf - cdf.min()) * 255) / (cdf.max() - cdf.min())
    channel_new = cdf_norm[channel.flatten()]
    channel_new = np.reshape(channel_new, channel.shape)
    return channel_new

########################################################## For Adaptive
def hist_equalization(img):
    """ Normal Histogram Equalization

    Args:
        img : image input with single channel

    Returns:
        : Equalized Image
    """
    array = np.asarray(img)
    bin_cont = np.bincount(array.flatten(), minlength=256)
    pixels = np.sum(bin_cont)
    bin_cont = bin_cont / pixels
    cumulative_sumhist = np.cumsum(bin_cont)
    map = np.floor(255 * cumulative_sumhist).astype(np.uint8)
    arr_list = list(array.flatten())
    eq_arr = [map[p] for p in arr_list]
    arr_back = np.reshape(np.asarray(eq_arr), array.shape)
    return arr_back


def ahe(img, rx=193, ry=199): # Tested through trial and error on the spine image
    """ Adaptive Histogram Equalization

    Args:
        img : image input with single channel
        rx (int, optional): to divide horizontal regions, Note: Should be divisible by image size in x . Defaults to 136.
        ry (int, optional): to divide vertical regions, Note: Should be divisible by image size in y. Defaults to 185.

    Returns:
        : Equalized Image
    """
    v = img
    img_eq = np.empty((v.shape[0], v.shape[1]), dtype=np.uint8)
    for i in range(0, v.shape[1], rx):
        for j in range(0, v.shape[0], ry):
            t = v[j:j + ry, i:i + rx]
            c = hist_equalization(t)
            img_eq[j:j + ry, i:i + rx] = c
    return img_eq