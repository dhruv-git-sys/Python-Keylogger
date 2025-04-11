import keyboard
import datetime
import os
from tkinter import *
from tkinter import messagebox

class KeyLogger:
    def __init__(self):
        self.is_recording = False
        self.log_file = None
        self.setup_gui()
        
    def setup_gui(self):
        self.root = Tk()
        self.root.title("Personal Keylogger")
        self.root.geometry("300x150")
        
        self.status_label = Label(
            self.root, 
            text="Status: Not Recording",
            fg="red"
        )
        self.status_label.pack(pady=10)
        
        self.toggle_button = Button(
            self.root,
            text="Start Recording",
            command=self.toggle_recording
        )
        self.toggle_button.pack(pady=10)
        
        self.exit_button = Button(
            self.root,
            text="Exit",
            command=self.cleanup_and_exit
        )
        self.exit_button.pack(pady=10)
        
    def start_recording(self):
        try:
            # Create logs directory if it doesn't exist
            if not os.path.exists("logs"):
                os.makedirs("logs")
            
            # Create new log file with timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            self.log_file = open(f"logs/keylog_{timestamp}.txt", "w")
            
            # Setup keyboard hook
            keyboard.on_release(callback=self.on_key_press)
            
            self.is_recording = True
            self.status_label.config(text="Status: Recording", fg="green")
            self.toggle_button.config(text="Stop Recording")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start recording: {str(e)}")
            self.cleanup()
    
    def stop_recording(self):
        try:
            keyboard.unhook_all()
            if self.log_file:
                self.log_file.close()
                self.log_file = None
            
            self.is_recording = False
            self.status_label.config(text="Status: Not Recording", fg="red")
            self.toggle_button.config(text="Start Recording")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop recording: {str(e)}")
    
    def toggle_recording(self):
        if self.is_recording:
            self.stop_recording()
        else:
            self.start_recording()
    
    def on_key_press(self, event):
        try:
            if self.log_file and not self.log_file.closed:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                key_name = event.name if hasattr(event, 'name') else 'unknown'
                log_entry = f"{timestamp}: {key_name}\n"
                self.log_file.write(log_entry)
                self.log_file.flush() 
                
        except Exception as e:
            print(f"Error logging keystroke: {str(e)}")
    
    def cleanup(self):
        if self.log_file and not self.log_file.closed:
            self.log_file.close()
        keyboard.unhook_all()
    
    def cleanup_and_exit(self):
        self.cleanup()
        self.root.quit()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    logger = KeyLogger()
    logger.run()
