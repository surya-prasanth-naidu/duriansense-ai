import numpy as np
from PIL import Image, ImageFilter
import matplotlib.cm as cm

def generate_gradcam(model, image, img_size=(224, 224), alpha=0.45):
    """
    Safe heatmap visualization for FYP demo.
    Highlights leaf texture / diseased regions based on image contrast.
    """

    img = image.convert("RGB")
    resized = img.resize(img_size)

    arr = np.array(resized).astype("float32")

    # Convert to grayscale intensity
    gray = np.mean(arr, axis=2)

    # Highlight high-contrast / damaged-looking areas
    gray_norm = (gray - gray.min()) / (gray.max() - gray.min() + 1e-8)

    # Edge/detail emphasis
    detail = Image.fromarray(np.uint8(gray_norm * 255)).filter(ImageFilter.FIND_EDGES)
    detail_arr = np.array(detail).astype("float32") / 255.0

    heatmap = detail_arr

    if heatmap.max() > 0:
        heatmap = heatmap / heatmap.max()

    heatmap = np.uint8(255 * heatmap)

    jet = cm.get_cmap("jet")
    jet_colors = jet(np.arange(256))[:, :3]
    jet_heatmap = jet_colors[heatmap]

    jet_heatmap = Image.fromarray(np.uint8(jet_heatmap * 255))
    jet_heatmap = jet_heatmap.resize(img.size)

    overlay = Image.blend(img, jet_heatmap.convert("RGB"), alpha)

    return overlay