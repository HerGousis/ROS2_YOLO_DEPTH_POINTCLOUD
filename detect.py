from ultralytics import YOLO
import matplotlib.pyplot as plt
import cv2

# Φόρτωσε το μικρότερο μοντέλο (nano version)
model = YOLO('yolov8n.pt')

foto = 'image/3.jpg'

# Ανάγνωση της εικόνας με OpenCV για εμφάνιση με matplotlib
image = cv2.imread(foto)

# Μετατροπή από BGR σε RGB (OpenCV φορτώνει εικόνες σε BGR, ενώ το matplotlib θέλει RGB)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Εμφάνιση της εικόνας πριν την ανίχνευση
plt.figure(figsize=(10, 8))
plt.subplot(1, 2, 1)  # 1 σειρά, 2 στήλες, 1ο subplot
plt.imshow(image_rgb)
plt.title("Πριν την Ανίχνευση")
plt.axis('off')  # Απενεργοποίηση των αξόνων

# Ανίχνευση αντικειμένων με CPU
results = model(foto, device='cpu')

# Εμφάνιση των αποτελεσμάτων με τις ανιχνευμένες περιοχές
result_image = results[0].plot()  # Αυτό δημιουργεί την εικόνα με τα ανιχνευμένα αντικείμενα

# Εμφάνιση της εικόνας μετά την ανίχνευση
plt.subplot(1, 2, 2)  # 1 σειρά, 2 στήλες, 2ο subplot
plt.imshow(result_image)
plt.title("Μετά την Ανίχνευση")
plt.axis('off')  # Απενεργοποίηση των αξόνων

# Εμφάνιση του παραθύρου με τις εικόνες
plt.show()

print("Detection completed! Δες το αρχείο result.jpg")
