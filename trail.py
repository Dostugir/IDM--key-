import os
import sys
import tkinter as tk
from tkinter import messagebox, StringVar
import winreg
import random
import string
import ctypes
import subprocess
from datetime import datetime, timedelta

class IDMActivator:
    def __init__(self, root):
        self.root = root
        self.root.title("IDM Activator")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        self.setup_ui()
        
    def setup_ui(self):
        # Set background color
        self.root.configure(bg="#f0f0f0")
        
        # Title label
        title_label = tk.Label(self.root, text="Internet Download Manager Activator", 
                              font=("Arial", 14, "bold"), bg="#f0f0f0")
        title_label.pack(pady=15)
        
        # Serial number display
        self.serial_var = StringVar()
        self.serial_var.set(self.generate_serial())
        
        serial_frame = tk.Frame(self.root, bg="#f0f0f0")
        serial_frame.pack(pady=10)
        
        serial_label = tk.Label(serial_frame, text="Serial Number:", 
                               font=("Arial", 10), bg="#f0f0f0")
        serial_label.grid(row=0, column=0, padx=5)
        
        serial_entry = tk.Entry(serial_frame, textvariable=self.serial_var, 
                               width=30, font=("Arial", 10))
        serial_entry.grid(row=0, column=1, padx=5)
        
        # Buttons
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(pady=20)
        
        activate_button = tk.Button(button_frame, text="Activate IDM", 
                                   command=self.activate_idm, width=15,
                                   bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        activate_button.grid(row=0, column=0, padx=10)
        
        new_serial_button = tk.Button(button_frame, text="New Serial", 
                                     command=self.refresh_serial, width=15,
                                     bg="#2196F3", fg="white", font=("Arial", 10, "bold"))
        new_serial_button.grid(row=0, column=1, padx=10)
        
        # Status label
        self.status_var = StringVar()
        self.status_var.set("Ready to activate")
        status_label = tk.Label(self.root, textvariable=self.status_var, 
                               font=("Arial", 10), bg="#f0f0f0", fg="#555555")
        status_label.pack(pady=10)
        
        # Footer
        footer_label = tk.Label(self.root, text="For educational purposes only", 
                               font=("Arial", 8), bg="#f0f0f0", fg="#999999")
        footer_label.pack(side=tk.BOTTOM, pady=5)
    
    def generate_serial(self):
        """Generate a random serial number in IDM format"""
        # Format: XXXXX-XXXXX-XXXXX-XXXXX
        chars = string.ascii_uppercase + string.digits
        serial = '-'.join(''.join(random.choice(chars) for _ in range(5)) for _ in range(4))
        return serial
    
    def refresh_serial(self):
        """Generate a new serial number"""
        self.serial_var.set(self.generate_serial())
    
    def is_admin(self):
        """Check if the application is running with admin privileges"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def restart_as_admin(self):
        """Restart the application with admin privileges"""
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()
    
    def find_idm_registry_path(self):
        """Find the IDM registry path"""
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\DownloadManager") as key:
                return r"Software\DownloadManager"
        except:
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"Software\DownloadManager") as key:
                    return r"Software\DownloadManager"
            except:
                try:
                    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Internet Download Manager") as key:
                        return r"Software\Internet Download Manager"
                except:
                    return None
    
    def activate_idm(self):
        """Activate IDM with the generated serial number"""
        if not self.is_admin():
            response = messagebox.askyesno("Admin Rights Required", 
                                          "This operation requires administrator privileges. Do you want to restart as admin?")
            if response:
                self.restart_as_admin()
            return
        
        self.status_var.set("Activating IDM...")
        self.root.update()
        
        # Find IDM registry path
        reg_path = self.find_idm_registry_path()
        if not reg_path:
            messagebox.showerror("Error", "IDM registry keys not found. Is IDM installed?")
            self.status_var.set("Activation failed - IDM not found")
            return
        
        try:
            # Close IDM if running
            os.system("taskkill /f /im IDMan.exe 2>nul")
            
            # Set serial number
            serial = self.serial_var.get()
            
            # Set registry values
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_path) as key:
                winreg.SetValueEx(key, "Serial", 0, winreg.REG_SZ, serial)
                winreg.SetValueEx(key, "LstCheck", 0, winreg.REG_SZ, "")
                winreg.SetValueEx(key, "FName", 0, winreg.REG_SZ, "Registered User")
                winreg.SetValueEx(key, "LName", 0, winreg.REG_SZ, "")
                winreg.SetValueEx(key, "Email", 0, winreg.REG_SZ, "user@example.com")
                
                # Set expiration date to far future
                future_date = (datetime.now() + timedelta(days=3650)).strftime("%m/%d/%Y")
                winreg.SetValueEx(key, "ExpireDate", 0, winreg.REG_SZ, future_date)
                
                # Set registration status
                winreg.SetValueEx(key, "CheckUpdtVM", 0, winreg.REG_SZ, "")
                winreg.SetValueEx(key, "scansk", 0, winreg.REG_DWORD, 1)
            
            messagebox.showinfo("Success", f"IDM has been activated with serial:\n{serial}")
            self.status_var.set("IDM activated successfully")
            
            # Ask to start IDM
            if messagebox.askyesno("Start IDM", "Do you want to start IDM now?"):
                try:
                    subprocess.Popen("C:\\Program Files (x86)\\Internet Download Manager\\IDMan.exe")
                except:
                    try:
                        subprocess.Popen("C:\\Program Files\\Internet Download Manager\\IDMan.exe")
                    except:
                        messagebox.showwarning("Warning", "Could not start IDM automatically. Please start it manually.")
        
        except Exception as e:
            messagebox.showerror("Error", f"Activation failed: {str(e)}")
            self.status_var.set("Activation failed - Error occurred")

if __name__ == "__main__":
    root = tk.Tk()
    app = IDMActivator(root)
    root.mainloop()

