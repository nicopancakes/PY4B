import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import sys
import os
import json
import re
CONFIG_FILE = "py4b_config.json"
WINDOW_WIDTH = 358
WINDOW_HEIGHT = 415
def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {"auto_install_python": False}
def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)
def is_python_installed():
    """Check if Python is available in the system"""
    try:
        for cmd in ["python", "python3", sys.executable]:
            result = subprocess.run([cmd, "--version"], 
                                  capture_output=True, text=True, timeout=3)
            if result.returncode == 0:
                return True
    except:
        pass
    return False
def get_missing_packages(py_file):
    """Simple import scanner"""
    packages = set()
    try:
        with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        imports = re.findall(r'^\s*(?:from|import)\s+([a-zA-Z0-9_]+)', content, re.MULTILINE)
        for imp in imports:
            if imp not in {'os', 'sys', 'tkinter', 'json', 're', 'subprocess', 'threading', 
                          'datetime', 'math', 'random', 'time', 'collections', 'functools'}:
                packages.add(imp)
    except:
        pass
    return list(packages)
def install_packages(packages):
    for pkg in packages:
        try:
            print(f"Installing {pkg}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
            print(f"{pkg} installed successfully")
        except:
            print(f"Failed to install {pkg}")
class PY4BApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PY4B v.1.3.1 Built on 6/17/2026")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(False, False)
        self.root.configure(bg="white")
        
        self.config = load_config()
        self.create_widgets()
        
    def create_widgets(self):
        title = tk.Label(self.root, text="PY4B", font=("Arial", 24, "bold"), bg="white", fg="#222")
        title.pack(pady=15)
        
        tk.Label(self.root, text="Python for Beginners.", font=("Arial", 10), bg="white", fg="#555").pack(pady=(0, 20))
      
        frame = tk.Frame(self.root, bg="white")
        frame.pack(pady=10, padx=25, fill="x")
        
        tk.Label(frame, text="Select a Python or EXE file:", bg="white", anchor="w").pack(fill="x")
        
        self.entry = tk.Entry(frame, width=40, font=("Arial", 9))
        self.entry.pack(pady=8, fill="x")
        
        btn_frame = tk.Frame(frame, bg="white")
        btn_frame.pack(pady=5)
        
        tk.Button(btn_frame, text="Browse File", command=self.browse_file, width=14).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Launch", command=self.launch, bg="#4CAF50", fg="white", width=14).pack(side="left", padx=5)
        self.auto_var = tk.BooleanVar(value=self.config.get("auto_install_python", False))
        self.chk = tk.Checkbutton(self.root, text="Auto Install Python (if needed)", 
                                 variable=self.auto_var, bg="white", 
                                 command=self.on_auto_checkbox_click, anchor="w")
        self.chk.pack(pady=20, padx=30, anchor="w")
       
        info_text = "Supported formats:\n• .py files\n• .exe files"
        info = tk.Label(self.root, text=info_text, bg="white", justify="left", fg="#444", font=("Arial", 9))
        info.pack(pady=10)
        
        footer = tk.Label(self.root, text="PY4B Freezing when Installing Libraries is Normal.", 
                         bg="white", fg="#888", font=("Arial", 8))
        footer.pack(side="bottom", pady=20)
        
    def on_auto_checkbox_click(self):
        """Called when checkbox is clicked"""
        self.config["auto_install_python"] = self.auto_var.get()
        save_config(self.config)
        
        if self.auto_var.get():
            if not is_python_installed():
                if messagebox.askyesno("Python Not Found", 
                                      "Python is not detected on this system.\n\nOpen installation guide?"):
                    import webbrowser
                    webbrowser.open("https://meetniko.fyi/py4b")
    
    def browse_file(self):
        filetypes = [("Python Files & Executables", "*.py *.exe"), ("All Files", "*.*")]
        filepath = filedialog.askopenfilename(filetypes=filetypes)
        if filepath:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, filepath)
    
    def launch(self):
        path = self.entry.get().strip()
        if not path:
            messagebox.showwarning("Empty..?", "Please select a file first.")
            return
        
        if not os.path.exists(path):
            messagebox.showerror("Not Found, hmmm..", "The selected file does not exist.")
            return
        
        if path.endswith('.exe'):
            self.root.destroy()
            try:
                os.startfile(path)
            except Exception as e:
                messagebox.showerror("Error", f"Could not run exe:\n{e}")
        elif path.endswith('.py'):
            self.run_python_file(path)
        else:
            messagebox.showwarning("This file is Unsupported! :(", "Only .py and .exe files are supported.")

    def run_python_file(self, py_file):
        missing = get_missing_packages(py_file)
        
        if missing:
            if messagebox.askyesno("Missing Libraries", 
                                  f"The following packages are missing:\n\n{', '.join(missing)}\n\nInstall them now?"):
                install_packages(missing)
     
        self.root.destroy()
        try:
            subprocess.Popen([sys.executable, py_file])
        except Exception as e:
            print("Error launching script:", e)


if __name__ == "__main__":
    app = PY4BApp()
    app.root.mainloop()
