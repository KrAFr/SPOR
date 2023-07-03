import cv2
import pytesseract
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk


class ImageSelection:
    def __init__(self, image_path):
        self.image_path = image_path
        self.top_left = None
        self.bottom_right = None
        self.selection_complete = False

    def on_mouse_down(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.top_left = (x, y)
        elif event == cv2.EVENT_LBUTTONUP:
            self.bottom_right = (x, y)
            self.selection_complete = True


def SPOR(image_path):
    # Create an instance of ImageSelection
    selection = ImageSelection(image_path)

    # Load image using OpenCV
    image = cv2.imread(image_path)

    # Create a window to display the image and handle mouse events
    cv2.namedWindow("Select ROI")
    cv2.setMouseCallback("Select ROI", selection.on_mouse_down)

    while not selection.selection_complete:
        # Display the image
        cv2.imshow("Select ROI", image)

        # Break the loop when 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

    if selection.selection_complete:
        # Perform OCR on the selected region
        # Load the full image
        full_image = cv2.imread(image_path)

        # Select the region of interest based on the user's selection
        roi = full_image[selection.top_left[1]:selection.bottom_right[1],
              selection.top_left[0]:selection.bottom_right[0]]

        # Preprocess the selected region
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
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

        # Update the selected file label
        selected_file_label.configure(text=file_path)

        # Run OCR on the selected image
        window.after(100, lambda: SPOR(file_path))


def select_all(event):
    text_box.tag_add("sel", "1.0", "end")
    return "break"  # Prevent default binding from executing


# Create the GUI window
window = tk.Tk()
window.title("SPOR Application")
window.geometry("360x360")

# Create a custom style for ttk widgets
style = ttk.Style(window)
style.configure("Custom.TButton", font=("Helvetica", 12), padding=5)
style.configure("Custom.TLabel", font=("Helvetica", 12))

# Add a button to select the image
select_button = ttk.Button(window, text="Select Image", style="Custom.TButton", command=select_image)
select_button.pack(pady=10)

# Add a label to display the selected file path
selected_file_label = ttk.Label(window, text="", style="Custom.TLabel")
selected_file_label.pack(pady=10)

# Add a text box to display the extracted text with a border
text_box = tk.Text(window, wrap=tk.WORD, relief=tk.SOLID, borderwidth=1)
text_box.pack(pady=10)

# Bind Ctrl+A event to select_all function
text_box.bind("<Control-a>", select_all)

# Run the GUI main loop
window.mainloop()
