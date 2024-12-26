import cv2
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import numpy as np

def upload_image():
    global img, file_path
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.jpg *.png *.jpeg *.bmp")]
    )
    if file_path:
        img = cv2.imread(file_path)
        original_img = img.copy()
        display_image(img, original=True)
        history.append(original_img)

def convert_to_grayscale():
    global img, gray_img
    if img is None:
        messagebox.showwarning("Warning", "Please upload an image first!")
        return
    
    status_label.config(text="Processing... Please wait.")
    app.update_idletasks()

    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    display_image(gray_img, original=False)

    status_label.config(text="Conversion complete!")
    history.append(gray_img)

def apply_sharpening():
    if img is None:
        messagebox.showwarning("Warning", "Please upload an image first!")
        return
    
    kernel = np.array([[0, -1, 0], [-1, 5,-1], [0, -1, 0]])
    sharpened_img = cv2.filter2D(img, -1, kernel)
    display_image(sharpened_img, original=True)
    history.append(sharpened_img)

def adjust_contrast_brightness():
    if img is None:
        messagebox.showwarning("Warning", "Please upload an image first!")
        return
    
    alpha = 1.5
    beta = 50
    adjusted_img = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
    display_image(adjusted_img, original=True)
    history.append(adjusted_img)

def histogram_equalization():
    if gray_img is None:
        messagebox.showwarning("Warning", "Please convert the image to grayscale first!")
        return
    
    equalized_img = cv2.equalizeHist(gray_img)
    display_image(equalized_img, original=False)
    history.append(equalized_img)

def save_image():
    if gray_img is None and img is None:
        messagebox.showwarning("Warning", "No image to save!")
        return
    save_path = filedialog.asksaveasfilename(
        defaultextension=".jpg",
        filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("BMP files", "*.bmp")]
    )
    if save_path:
        if gray_img is not None:
            cv2.imwrite(save_path, gray_img)
        else:
            cv2.imwrite(save_path, img)
        messagebox.showinfo("Success", f"Image saved to {save_path}")

def undo_action():
    if history:
        last_img = history.pop()
        display_image(last_img, original=False if last_img.ndim == 2 else True)

def display_image(image, original):
    if original:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    else:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    
    img_resized = cv2.resize(image, (300, 300))
    img_pil = Image.fromarray(img_resized)
    img_tk = ImageTk.PhotoImage(img_pil)
    
    label = original_label if original else grayscale_label
    label.configure(image=img_tk)
    label.image = img_tk

img = None
gray_img = None
file_path = None
history = []

app = tk.Tk()
app.title("Image Grayscale Converter")
app.geometry("800x600")

upload_btn = tk.Button(app, text="Upload Image", command=upload_image, width=20)
upload_btn.pack(pady=10)

original_label = tk.Label(app, text="Original Image")
original_label.pack(side=tk.LEFT, padx=20)

grayscale_label = tk.Label(app, text="Grayscale Image")
grayscale_label.pack(side=tk.RIGHT, padx=20)

status_label = tk.Label(app, text="Ready", font=('Helvetica', 12), fg='green')
status_label.pack(pady=10)

convert_btn = tk.Button(app, text="Convert to Grayscale", command=convert_to_grayscale, width=20)
convert_btn.pack(pady=5)

sharpen_btn = tk.Button(app, text="Apply Sharpening", command=apply_sharpening, width=20)
sharpen_btn.pack(pady=5)

contrast_btn = tk.Button(app, text="Adjust Contrast/Brightness", command=adjust_contrast_brightness, width=20)
contrast_btn.pack(pady=5)

equalize_btn = tk.Button(app, text="Histogram Equalization", command=histogram_equalization, width=20)
equalize_btn.pack(pady=5)

undo_btn = tk.Button(app, text="Undo", command=undo_action, width=20)
undo_btn.pack(pady=5)

save_btn = tk.Button(app, text="Save Image", command=save_image, width=20)
save_btn.pack(pady=10)

app.mainloop()
