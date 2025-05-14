from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt

# YOLO detection module
def detect_and_show(
    image_path: str,
    model_path: str = 'yolov8n.pt',
    device: str = 'cpu',
    figsize=(5, 5),
    save_result: bool = False,
    result_path: str = 'result.jpg'
):
    """
    Κάνει ανίχνευση αντικειμένων με YOLOv8 και εμφανίζει μόνο το αποτέλεσμα.

    Returns:
      Η εικόνα αποτελέσματος σε μορφή RGB numpy array.
    """
    # Φορτώνουμε το μοντέλο
    model = YOLO(model_path)
    # Εκτέλεση ανίχνευσης
    results = model(image_path, device=device)
    # Αποθήκευση/επιστροφή εικόνας με πλαίσια
    out_rgb = results[0].plot()
    if save_result:
        out_bgr = cv2.cvtColor(out_rgb, cv2.COLOR_RGB2BGR)
        cv2.imwrite(result_path, out_bgr)
    return out_rgb





def detect_and_get_boxes(
    image_path: str,
    model_path: str = 'yolov8n.pt',
    device: str = 'cpu'
):
    model = YOLO(model_path)  # Φορτώνουμε το μοντέλο
    results = model(image_path, device=device)  # Εκτελούμε την ανίχνευση

    boxes = []  # Λίστα για τα boxes
    labels = []  # Λίστα για τα labels (ονόματα)
    
    for r in results:
        # Εξάγουμε τα boxes και τα labels για κάθε ανίχνευση
        for box, conf, cls in zip(r.boxes.xyxy.cpu().numpy(), r.boxes.conf.cpu().numpy(), r.boxes.cls.cpu().numpy()):
            box = box.astype(int)
            label = r.names[int(cls)]  # Ανάκτηση της ετικέτας από το `r.names`
            boxes.append(box)
            labels.append(label)

    # Παίρνουμε την εικόνα με τα plotted bounding boxes
    result_img = results[0].plot()

    return result_img, boxes, labels

