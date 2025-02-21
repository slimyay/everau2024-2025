import cv2
import numpy as np
from tkinter import Tk, filedialog
from tkinter import messagebox

def adjust_exposure(input_path, output_path, gamma=0.8):
    """
    Adjust the exposure of a video using Gamma correction.

    Parameters:
    - input_path: Path to the input video.
    - output_path: Path to save the output video.
    - gamma: Gamma correction factor (<1 to darken, >1 to brighten).
    """
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        messagebox.showerror("Error", "Failed to open the input video.")
        return

    # Get video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for output video

    # Create video writer
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # Precompute gamma correction lookup table
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in range(256)]).astype("uint8")

    # Process frames
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Processing {frame_count} frames...")

    for i in range(frame_count):
        ret, frame = cap.read()
        if not ret:
            break
        # Apply gamma correction
        corrected_frame = cv2.LUT(frame, table)
        out.write(corrected_frame)
        if i % 100 == 0:
            print(f"Processed frame {i}/{frame_count}")

    cap.release()
    out.release()
    messagebox.showinfo("Success", f"Exposure correction completed!\nOutput saved to: {output_path}")

def select_input_file():
    """Open a file dialog to select the input video."""
    input_path = filedialog.askopenfilename(title="Select Input Video", filetypes=[("Video Files", "*.mp4 *.avi *.mov")])
    if input_path:
        return input_path
    else:
        messagebox.showwarning("Warning", "No file selected.")
        return None

def select_output_file():
    """Open a file dialog to select the output video path."""
    output_path = filedialog.asksaveasfilename(title="Save Output Video", defaultextension=".mp4", filetypes=[("MP4 Files", "*.mp4")])
    if output_path:
        return output_path
    else:
        messagebox.showwarning("Warning", "No output path selected.")
        return None

def main():
    # Initialize the GUI
    Tk().withdraw()  # Hide the root Tkinter window
    input_path = select_input_file()
    if not input_path:
        return

    output_path = select_output_file()
    if not output_path:
        return

    gamma = 0.8  # Default gamma correction factor
    adjust_exposure(input_path, output_path, gamma)

if __name__ == "__main__":
    main()
