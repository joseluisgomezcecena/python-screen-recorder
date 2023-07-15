import tkinter as tk
import tkinter.filedialog as filedialog
import threading
import pyautogui
import cv2
import numpy as np

class ScreenRecorder:
    def __init__(self):
        self.is_recording = False
        self.frames = []
        self.save_location = ""
        self.low_quality = False

    def start_recording(self):
        if self.is_recording:
            return  # Recording already in progress, ignore the click

        self.is_recording = True
        self.frames = []

        # Create a separate thread for recording
        recording_thread = threading.Thread(target=self._record)
        recording_thread.start()

    def stop_recording(self):
        if not self.is_recording:
            return  # No active recording, ignore the click

        self.is_recording = False

        # Open a file dialog to choose the save location
        self.choose_save_location()

    def choose_save_location(self):
        # Open a file dialog to choose the save location
        self.save_location = filedialog.asksaveasfilename(defaultextension=".mp4",
                                                          filetypes=[("MP4 files", "*.mp4")])

        # Save the frames as a video file
        self._save_video()

        # Clear the frames list
        self.frames = []

    def toggle_low_quality(self):
        self.low_quality = not self.low_quality

    def _record(self):
        while self.is_recording:
            # Capture the screen and add the frame to the list
            frame = pyautogui.screenshot()
            self.frames.append(frame)

            if self.low_quality:
                # Resize the frame to reduce the resolution
                frame = frame.resize((frame.width // 2, frame.height // 2))

            # Delay to adjust the frame rate
            if not self.low_quality:
                # Normal quality: delay of 0.05 seconds (20 frames per second)
                pyautogui.sleep(0.05)
            else:
                # Low quality: delay of 0.1 seconds (10 frames per second)
                pyautogui.sleep(0.1)

    def _save_video(self):
        if self.frames and self.save_location:
            # Get the dimensions of the first frame
            frame_width, frame_height = self.frames[0].size

            # Create a video writer object
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            video_writer = cv2.VideoWriter(self.save_location, fourcc, 20.0, (frame_width, frame_height))

            # Write each frame to the video file
            for frame in self.frames:
                # Convert the frame to BGR format
                frame = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
                video_writer.write(frame)

            # Release the video writer
            video_writer.release()

class App:
    def __init__(self, root):
        self.root = root
        self.screen_recorder = ScreenRecorder()

        # Create UI elements
        self.start_button = tk.Button(root, text="Start Recording", command=self.start_recording)
        self.start_button.pack()

        self.stop_button = tk.Button(root, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack()

        self.low_quality_button = tk.Button(root, text="Low Quality", command=self.toggle_low_quality)
        self.low_quality_button.pack()

    def start_recording(self):
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.screen_recorder.start_recording()

    def stop_recording(self):
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.screen_recorder.stop_recording()

    def toggle_low_quality(self):
        self.screen_recorder.toggle_low_quality()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
