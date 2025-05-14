import os
import urllib.request

import cv2
import numpy as np
import matplotlib.pyplot as plt
from ultralytics import YOLO

# ——————————————————————————————
# 1) Helpers από monocular_depth_estimation.py
# ——————————————————————————————
def download_midas(model_path="midas_small.onnx"):
    if not os.path.exists(model_path):
        print("Κατεβάζω το MiDaS μοντέλο…")
        urllib.request.urlretrieve(
            "https://github.com/intel-isl/MiDaS/releases/download/v2_1/model-small.onnx",
            model_path
        )

def compute_depth(img_bgr, model_path="midas_small.onnx"):
    # φορτώνει και κάνει forward το ONNX MiDaS
    net = cv2.dnn.readNet(model_path)
    inp = cv2.resize(img_bgr, (256, 256))
    blob = cv2.dnn.blobFromImage(
        inp, 1/255.0, (256,256),
        mean=(0.5,0.5,0.5), swapRB=True, crop=False
    )
    net.setInput(blob)
    depth = net.forward().squeeze()
    depth = cv2.resize(depth, (img_bgr.shape[1], img_bgr.shape[0]))
    # κανονικοποίηση
    dmin, dmax = depth.min(), depth.max()
    depth_norm = ((depth - dmin) / (dmax - dmin) * 255).astype(np.uint8)
    return depth_norm

# ——————————————————————————————
# 2) Helper από detect2.py
# ——————————————————————————————
def yolo_detect(img_path, model_path="yolov8n.pt", device="cpu"):
    model = YOLO(model_path)
    results = model(img_path, device=device)
    # plot() επιστρέφει τα pixels σε RGB
    return results[0].plot()

# ——————————————————————————————
# 3) Main: όλα σε ένα figure
# ——————————————————————————————
def run_combined(image_path="image/3.jpg"):
    # --- διαβάζουμε εικόνα
    img_bgr = cv2.imread(image_path)
    if img_bgr is None:
        raise FileNotFoundError(f"Δεν βρέθηκε η εικόνα: {image_path}")
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    # --- υπολογίζουμε depth
    download_midas()
    depth_vis = compute_depth(img_bgr)

    # --- κάνουμε YOLO detection
    det_rgb = yolo_detect(image_path)

    # --- φτιάχνουμε ένα figure με 3 υποπλοκές
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    axes[0].imshow(img_rgb)
    axes[0].set_title("Original Image")
    axes[0].axis('off')

    axes[1].imshow(depth_vis, cmap='plasma')
    axes[1].set_title("Monocular Depth")
    axes[1].axis('off')

    axes[2].imshow(det_rgb)
    axes[2].set_title("YOLO Detection")
    axes[2].axis('off')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_combined("image/3.jpg")
