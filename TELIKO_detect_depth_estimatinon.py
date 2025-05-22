import cv2
import matplotlib.pyplot as plt
from detect_kalo import detect_and_show, detect_and_get_boxes
from monocular_depth_estimation import estimate_depth, depth_to_obj, generate_point_cloud_data
import numpy as np
from pointcloud import show_point_cloud_with_centroids

# === Main ===
if __name__ == '__main__':
    image_path = 'image/12.jpg'

    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    depth_vis = estimate_depth(image_path)

    # ⬇️ Τώρα παίρνουμε και labels από την ανίχνευση
    det_rgb, boxes, labels = detect_and_get_boxes(image_path)
    det_rgb = detect_and_show(image_path)

    full_depth = estimate_depth(image_path)

    # Παράμετροι κάμερας
    fx = 525.0
    fy = 525.0
    cx = 319.5
    cy = 239.5

    centroids = []
    masked_depth = np.zeros(full_depth.shape, dtype=np.float32)

    for i, (box, label) in enumerate(zip(boxes, labels)):
        x1, y1, x2, y2 = box
        masked_depth[y1:y2, x1:x2] = full_depth[y1:y2, x1:x2]

        cropped_depth = full_depth[y1:y2, x1:x2]
        cropped_rgb = img[y1:y2, x1:x2]

        if cropped_depth.shape[0] == 0 or cropped_depth.shape[1] == 0:
            continue

        try:
            _, _, _, _, centroid = generate_point_cloud_data(
                cropped_depth, cropped_rgb,
                fx=fx, fy=fy,
                cx=cropped_rgb.shape[1] / 2,
                cy=cropped_rgb.shape[0] / 2
            )
            centroids.append((i, centroid, label))
            print(f" {label} ({i}): x={centroid[0]:.4f}, y={centroid[1]:.4f}, z={centroid[2]:.4f}")
        except:
            print(f"Απέτυχε ο υπολογισμός για αντικείμενο {i} ({label})")

    # Αποθήκευση σε αρχείο
    with open("object_centroids.txt", "w") as f:
        for i, (x, y, z), label in centroids:
            f.write(f"{label} ({i}): x={x:.4f}, y={y:.4f}, z={z:.4f}\n")

    # Εξαγωγή OBJ
    depth_to_obj(masked_depth, img, output_file='masked_scene.obj')

    # boxes είναι λίστα από bounding boxes σε μορφή [x1, y1, x2, y2]
    show_point_cloud_with_centroids(masked_depth, img, boxes, fx=fx, fy=fy, cx=cx, cy=cy)



    # === Προετοιμασία για plotting ===
    xs, ys, zs, colors, _ = generate_point_cloud_data(masked_depth, img, fx=fx, fy=fy, cx=cx, cy=cy)

    depth_normalized = cv2.normalize(masked_depth, None, 0, 255, cv2.NORM_MINMAX)
    depth_normalized = np.uint8(depth_normalized)
    masked_depth_colored = cv2.applyColorMap(depth_normalized, cv2.COLORMAP_PLASMA)

 

    # === Plotting ===
    fig = plt.figure(figsize=(18, 8))
    gs = fig.add_gridspec(2, 3)

    ax1 = fig.add_subplot(gs[0, 0])
    ax1.imshow(img_rgb)
    ax1.set_title('Original Image')
    ax1.axis('off')

    ax2 = fig.add_subplot(gs[0, 1])
    ax2.imshow(det_rgb)
    ax2.set_title('YOLO Detection')
    ax2.axis('off')

    ax3 = fig.add_subplot(gs[1, 0])
    ax3.imshow(depth_vis, cmap='plasma')
    ax3.set_title('Monocular Depth')
    ax3.axis('off')

    ax4 = fig.add_subplot(gs[1, 1])
    ax4.imshow(masked_depth_colored)
    ax4.set_title('Depth σε Αντικείμενα ')
    ax4.axis('off')

    ax5 = fig.add_subplot(gs[:, 2], projection='3d')
    ax5.scatter(xs, ys, zs, c=colors, s=0.5)
    ax5.set_title('3D Point Cloud')
    ax5.set_axis_off()

    plt.tight_layout()
    plt.show()
