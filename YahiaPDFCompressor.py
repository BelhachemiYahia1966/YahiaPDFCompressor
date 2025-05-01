import os
import shutil
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk

class PDFCompressorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Yahia PDF Compressor")
        self.root.geometry("500x400")
        self.root.resizable(True, True)
        
        # Set icon (optional)
        try:
            self.root.iconbitmap("faviconnn.ico")  
        except:
            pass
        
        # Style configuration
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=("Arial", 10))
        self.style.configure("TButton", font=("Arial", 10))
        self.style.configure("TEntry", font=("Arial", 10))
        self.style.configure("Header.TLabel", font=("Arial", 12, "bold"))
        
        # Main frame
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        # Header
        self.header = ttk.Label(self.main_frame, text="Yahia PDF Compressor", style="Header.TLabel")
        self.header.pack(pady=(0, 20))
        
        # Input file selection
        self.input_frame = ttk.Frame(self.main_frame)
        self.input_frame.pack(fill=tk.X, pady=5)
        
        self.input_label = ttk.Label(self.input_frame, text="Input PDF File:")
        self.input_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.input_entry = ttk.Entry(self.input_frame, width=30)
        self.input_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        self.input_button = ttk.Button(self.input_frame, text="Browse Pc", command=self.browse_input)
        self.input_button.pack(side=tk.LEFT, padx=(10, 0))
        
        # Output file selection
        self.output_frame = ttk.Frame(self.main_frame)
        self.output_frame.pack(fill=tk.X, pady=5)
        
        self.output_label = ttk.Label(self.output_frame, text="Output PDF File:")
        self.output_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.output_entry = ttk.Entry(self.output_frame, width=30)
        self.output_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        self.output_button = ttk.Button(self.output_frame, text="Browse Pc", command=self.browse_output)
        self.output_button.pack(side=tk.LEFT, padx=(10, 0))
        
        # Compression level
        self.compression_frame = ttk.Frame(self.main_frame)
        self.compression_frame.pack(fill=tk.X, pady=10)
        
        self.compression_label = ttk.Label(self.compression_frame, text="Compression Level:")
        self.compression_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.compression_level = tk.IntVar(value=2)  # Default to medium compression
        self.compression_options = [
            ("Minimum (Large File)", 0),
            ("Low (Better Quality)", 1),
            ("Medium (Balanced)", 2),
            ("High (Good Compression)", 3),
            ("Maximum (Smallest File)", 4)
        ]
        
        for text, value in self.compression_options:
            rb = ttk.Radiobutton(
                self.compression_frame,
                text=text,
                variable=self.compression_level,
                value=value
            )
            rb.pack(side=tk.LEFT, padx=5)
        
        # Results display
        self.results_frame = ttk.Frame(self.main_frame)
        self.results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.results_label = ttk.Label(self.results_frame, text="Compression Results:")
        self.results_label.pack(anchor=tk.W)
        
        self.results_text = tk.Text(
            self.results_frame,
            height=6,
            width=50,
            state=tk.DISABLED,
            bg="#f9f9f9",
            relief=tk.FLAT,
            font=("Consolas", 9)
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Compress button
        self.compress_button = ttk.Button(
            self.main_frame,
            text="Compress PDF",
            command=self.compress_pdf
        )
        self.compress_button.pack(pady=10)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(
            root,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def browse_input(self):
        file_path = filedialog.askopenfilename(
            title="Select PDF File",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")]
        )
        if file_path:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, file_path)
            
            # Suggest output filename
            if not self.output_entry.get():
                base, ext = os.path.splitext(file_path)
                output_path = f"{base}_compressed{ext}"
                self.output_entry.delete(0, tk.END)
                self.output_entry.insert(0, output_path)
    
    def browse_output(self):
        file_path = filedialog.asksaveasfilename(
            title="Save Compressed PDF As",
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")]
        )
        if file_path:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, file_path)
    
    def update_results(self, text):
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, text)
        self.results_text.config(state=tk.DISABLED)
    
    def compress_pdf(self):
        input_path = self.input_entry.get()
        output_path = self.output_entry.get()
        power = self.compression_level.get()
        
        if not input_path:
            messagebox.showerror("Error", "Please select an input PDF file")
            return
        
        if not output_path:
            messagebox.showerror("Error", "Please specify an output PDF file")
            return
        
        try:
            self.status_var.set("Compressing...")
            self.root.update_idletasks()
            
            # Get Ghostscript path
            gs_path = self.get_ghostscript_path()
            
            # Compression quality settings
            quality = {
                0: "/default",
                1: "/prepress",
                2: "/printer",
                3: "/ebook",
                4: "/screen"
            }
            
            # Validate input
            if not os.path.isfile(input_path):
                messagebox.showerror("Error", f"Input file not found:\n{input_path}")
                return
            
            if input_path.split('.')[-1].lower() != 'pdf':
                messagebox.showerror("Error", "Input file is not a PDF")
                return
            
            # Get initial size
            initial_size = os.path.getsize(input_path)
            
            # Compress using Ghostscript
            subprocess.run(
                [
                    gs_path,
                    "-sDEVICE=pdfwrite",
                    "-dCompatibilityLevel=1.4",
                    "-dPDFSETTINGS={}".format(quality[power]),
                    "-dNOPAUSE",
                    "-dQUIET",
                    "-dBATCH",
                    "-sOutputFile={}".format(output_path),
                    input_path,
                ],
                check=True
            )
            
            # Get final size and calculate compression ratio
            final_size = os.path.getsize(output_path)
            ratio = 1 - (final_size / initial_size)
            
            # Format results
            result_text = f"Original Size: {self.format_file_size(initial_size)}\n"
            result_text += f"Compressed Size: {self.format_file_size(final_size)}\n"
            result_text += f"Size Reduction: {ratio:.1%}\n\n"
            result_text += f"Input: {input_path}\n"
            result_text += f"Output: {output_path}\n"
            result_text += f"Compression Level: {self.compression_options[power][0]}"
            
            self.update_results(result_text)
            self.status_var.set("Compression complete!")
            
            # Ask if user wants to open the file
            if messagebox.askyesno("Success", "Compression completed successfully!\nOpen the file now?"):
                if sys.platform == "win32":
                    os.startfile(output_path)
                elif sys.platform == "darwin":
                    subprocess.run(["open", output_path])
                else:
                    subprocess.run(["xdg-open", output_path])
            
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to compress PDF:\n{e}")
            self.status_var.set("Error during compression")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred:\n{e}")
            self.status_var.set("Error")
    
    def get_ghostscript_path(self):
        gs_names = ["gs", "gswin32", "gswin64", "gswin32c", "gswin64c"]
        for name in gs_names:
            if shutil.which(name):
                return shutil.which(name)
        raise FileNotFoundError(
            "GhostScript not found. Please install GhostScript and ensure it's in your PATH."
        )
    
    def format_file_size(self, size):
        """Convert file size to human-readable format"""
        for unit in ['bytes', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"

def main():
    root = tk.Tk()
    app = PDFCompressorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
