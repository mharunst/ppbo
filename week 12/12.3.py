import tkinter as tk
from tkinter import messagebox

class KonversiSuhuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Konversi Suhu")
        self.root.geometry("300x200")
        
        # Label input
        self.label_input = tk.Label(root, text="Masukkan suhu (°C):")
        self.label_input.pack(pady=5)
        
        # Entry input
        self.entry_suhu = tk.Entry(root)
        self.entry_suhu.pack(pady=5)
        
        # Tombol konversi
        self.btn_konversi = tk.Button(root, text="Konversi ke Fahrenheit", command=self.konversi_suhu)
        self.btn_konversi.pack(pady=10)
        
        # Label hasil
        self.label_hasil = tk.Label(root, text="Hasil:")
        self.label_hasil.pack(pady=5)

    def konversi_suhu(self):
        try:
            celsius = float(self.entry_suhu.get())
            fahrenheit = (celsius * 9/5) + 32
            self.label_hasil.config(text=f"Hasil: {fahrenheit:.2f} °F")
        except ValueError:
            messagebox.showerror("Error", "Masukkan angka yang valid!")

# Membuat window dan menjalankan aplikasi

root = tk.Tk()
app = KonversiSuhuApp(root)
root.mainloop()

