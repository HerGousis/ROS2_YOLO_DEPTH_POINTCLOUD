import numpy as np
import matplotlib.pyplot as plt

def show_point_cloud_with_centroids(depth_map, rgb_image, boxes, fx=525, fy=525, cx=None, cy=None, max_points=10000):
    h, w = depth_map.shape
    if cx is None:
        cx = w / 2
    if cy is None:
        cy = h / 2

    points = []
    colors = []
    centroids = []

    # Πρώτα όλα τα σημεία (όλα τα αντικείμενα μαζί)
    for v in range(h):
        for u in range(w):
            z = depth_map[v, u]
            if z <= 0:
                continue
            x = (u - cx) * z / fx
            y = -(v - cy) * z / fy
            points.append([x, y, z])
            b, g, r = rgb_image[v, u]
            colors.append([r/255, g/255, b/255])

    points = np.array(points)
    colors = np.array(colors)

    # Υπολογισμός centroid για κάθε bounding box
    for i, box in enumerate(boxes):
        x1, y1, x2, y2 = box
        xs, ys, zs = [], [], []

        for v in range(y1, y2):
            for u in range(x1, x2):
                if v >= h or u >= w:
                    continue
                z = depth_map[v, u]
                if z <= 0:
                    continue
                x = (u - cx) * z / fx
                y = -(v - cy) * z / fy
                xs.append(x)
                ys.append(y)
                zs.append(z)

        if len(xs) == 0:
            continue
        centroid = (np.mean(xs), np.mean(ys), np.mean(zs))
        centroids.append(centroid)

    # Sampling για καλύτερη απόδοση
    if len(points) > max_points:
        idx = np.random.choice(len(points), max_points, replace=False)
        points = points[idx]
        colors = colors[idx]

    # Plotting
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(points[:, 0], points[:, 1], points[:, 2], c=colors, s=0.5)

    # Plot centroids με κόκκινο X και λίγο μεγαλύτερο μέγεθος
    for c in centroids:
        ax.scatter(c[0], c[1], c[2], c='red', s=100, marker='X')
        ax.text(c[0], c[1], c[2], "Centroid", color='red')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('3D Point Cloud with Object Centroids')
    plt.show()
