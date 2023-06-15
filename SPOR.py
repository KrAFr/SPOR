import cv2
import pytesseract
import tkinter as tk
from tkinter import filedialog, messagebox

def SPOR(image_path):
    # Load image using OpenCV
    image = cv2.imread(image_path)

    # Preprocess the image (optional, depending on the quality of the input image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    processed_image = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # Perform OCR using pytesseract
    text = pytesseract.image_to_string(processed_image)

    # Clear previous text
    text_box.delete("1.0", tk.END)

    # Insert extracted text into the text box
    text_box.insert(tk.END, text)

def show_confirmation():
    messagebox.showinfo("Confirmation", "Image selected successfully.")

def select_image():
    # Prompt the user to select an image file
    file_path = filedialog.askopenfilename()

    if file_path:
        # Display confirmation message
        show_confirmation()

        # Run OCR on the selected image
        SPOR(file_path)

def select_all(event):
    text_box.tag_add("sel", "1.0", "end")
    return "break"  # Prevent default binding from executing

# Create the GUI window
window = tk.Tk()
window.title("SPOR Application")
window.geometry("360x360")

# Add a button to select the image
select_button = tk.Button(window, text="Select Image", command=select_image)
select_button.pack(pady=10)

# Add a text box to display the extracted text with a border
text_box = tk.Text(window, wrap=tk.WORD, relief=tk.SOLID, borderwidth=1)
text_box.pack(pady=10)

# Bind Ctrl+A event to select_all function
text_box.bind("<Control-a>", select_all)

# Run the GUI main loop
window.mainloop()
