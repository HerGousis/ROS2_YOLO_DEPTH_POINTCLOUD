import os
import urllib.request
import cv2
import numpy as np

# === 1. Λήψη του MiDaS μοντέλου ===
def download_midas(model_path: str = 'midas_small.onnx'):
    if not os.path.exists(model_path):
        print("Κατεβάζω το MiDaS μοντέλο…")
        urllib.request.urlretrieve(
            'https://github.com/intel-isl/MiDaS/releases/download/v2_1/model-small.onnx',
            model_path
        )

# === 2. Εκτίμηση βάθους ===
def estimate_depth(image_path: str, model_path: str = 'midas_small.onnx') -> np.ndarray:
    download_midas(model_path)
    img_bgr = cv2.imread(image_path)
    if img_bgr is None:
        raise FileNotFoundError(f"Δεν βρέθηκε η εικόνα: {image_path}")
    
    net = cv2.dnn.readNet(model_path)
    inp = cv2.resize(img_bgr, (256, 256))
    blob = cv2.dnn.blobFromImage(
        inp, 1/255.0, (256, 256),
        mean=(0.5, 0.5, 0.5), swapRB=True, crop=False
    )
    net.setInput(blob)
    depth = net.forward().squeeze()
    depth = cv2.resize(depth, (img_bgr.shape[1], img_bgr.shape[0]))
    
    # Κανονικοποίηση σε float32 [0, 1]
    depth = cv2.normalize(depth, None, 0, 1.0, cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    return depth

# === 3. Εξαγωγή Point Cloud σε OBJ ===
def depth_to_obj(depth_map, rgb_image, output_file='masked_scene.obj', fx=525, fy=525, cx=None, cy=None):
    h, w = depth_map.shape
    if cx is None:
        cx = w / 2
    if cy is None:
        cy = h / 2

    with open(output_file, 'w') as f:
        for v in range(h):
            for u in range(w):
                z = depth_map[v, u]
                if z <= 0:
                    continue
                x = (u - cx) * z / fx
                y = -(v - cy) * z / fy  # Χωρίς αρνητικό, καθώς η fy μπορεί να είναι ήδη σωστά ορισμένη
                b, g, r = rgb_image[v, u]
                f.write(f"v {x:.4f} {y:.4f} {z:.4f} {r/255:.4f} {g/255:.4f} {b/255:.4f}\n")
    print(f"[✔] 3D μοντέλο αποθηκεύτηκε στο: {output_file}")

def generate_point_cloud_data(depth_map, rgb_image, fx=525.0, fy=525.0, cx=None, cy=None):
    h, w = depth_map.shape
    if cx is None:
        cx = w / 2.0
    if cy is None:
        cy = h / 2.0

    xs, ys, zs, colors = [], [], [], []

    for v in range(h):
        for u in range(w):
            z = depth_map[v, u]
            if z <= 0:
                continue
            x = (u - cx) * z / fx
            y = -(v - cy) * z / fy
            b, g, r = rgb_image[v, u]
            xs.append(x)
            ys.append(y)
            zs.append(z)
            colors.append((r / 255.0, g / 255.0, b / 255.0))

    # Υπολογισμός κέντρου βάρους
    num_points = len(xs)
    if num_points == 0:
        centroid = (0.0, 0.0, 0.0)
    else:
        centroid = (
            sum(xs) / num_points,
            sum(ys) / num_points,
            sum(zs) / num_points
        )

    
    return xs, ys, zs, colors, centroid


