import tkinter as tk
import customtkinter
import cv2
from PIL import Image, ImageTk
import os
import time


class CameraApp:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.window.geometry("900x600")
        self.window.iconbitmap("camera.ico")

        self.cam = cv2.VideoCapture(video_source)
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.output = cv2.VideoWriter("output.avi", self.fourcc, 20.0, (1030, 650))

        self.output_dir = "captured_photos"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        self.canvas = tk.Canvas(window, width=1095, height=650, bg='white', highlightthickness=3, highlightbackground="grey" )
        self.canvas.pack(side=tk.LEFT)

        self.btn_snapshot = customtkinter.CTkButton(window, text="Snapshot", width=160, height=180, command=self.snapshot, hover=True, hover_color ="#1a4f76", border_width = 2, border_color= 'grey', fg_color = "#4a8bad", font=("Monsterat", 30), text_color = "white")
        self.btn_snapshot.place(x = 1110, y = 200)

        self.photo_count = 0  # Initialize photo_count

        self.update()

    def snapshot(self):
        ret, frame = self.cam.read()
        if ret:
            frame = cv2.flip(frame, 1)
            frame = cv2.resize(frame, (1050, 670))
            # Save the captured photo
            photo_filename = os.path.join(self.output_dir, f"photo_{self.photo_count + 1}.jpg")
            cv2.imwrite(photo_filename, frame)
            print(f"Photo {self.photo_count + 1} saved as {photo_filename}")

            # Increment the photo counter
            self.photo_count += 1
            # Wait for a short time to prevent multiple captures from a single press
            time.sleep(0.5)
            
    def update(self):
        ret, frame = self.cam.read()
        if ret:
            frame = cv2.flip(frame, 1)  
            frame = cv2.resize(frame, (1100, 645))
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.window.after(10, self.update)


if __name__ == "__main__":
    window = tk.Tk()
    app = CameraApp(window, "Camera App")
    window.mainloop()
    app.cam.release()
    app.output.release()
    cv2.destroyAllWindows()
