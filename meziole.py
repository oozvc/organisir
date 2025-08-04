import os
import shutil
import argparse
import time
import random
import math
import sys

def organize_files_by_extension(path):
    """Mengorganisir file berdasarkan ekstensi ke dalam folder terpisah"""
    if not os.path.exists(path):
        print(f"Path tidak ditemukan: {path}")
        return

    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)
        
        if os.path.isfile(filepath):
            # Skip file dummy generator
            if filename.startswith("dummy_"):
                continue
                
            # Dapatkan ekstensi file
            ext = os.path.splitext(filename)[1]
            ext = ext[1:] if ext else "NoExtension"
            
            # Buat folder tujuan jika belum ada
            dest_dir = os.path.join(path, ext + "_files")
            os.makedirs(dest_dir, exist_ok=True)
            
            # Pindahkan file
            dest_path = os.path.join(dest_dir, filename)
            shutil.move(filepath, dest_path)
            print(f"Memindahkan: {filename} -> {ext}_files/")

def fill_disk_space(path, target_free_gb=1, dummy_size_mb=100):
    """Mengisi ruang disk dengan file dummy hingga mencapai batas free space yang ditentukan"""
    # Dapatkan informasi penggunaan disk
    total, used, free = shutil.disk_usage(path)
    target_free_bytes = target_free_gb * (1024 ** 3)
    
    # Hitung ruang yang perlu diisi
    space_to_fill = free - target_free_bytes
    if space_to_fill <= 0:
        print(f"Ruang disk sudah di bawah target ({target_free_gb}GB)")
        return

    # Buat folder dummy jika belum ada
    dummy_dir = os.path.join(path, "DUMMY_FILES")
    os.makedirs(dummy_dir, exist_ok=True)

    # Hitung jumlah file yang diperlukan
    dummy_size_bytes = dummy_size_mb * (1024 ** 2)
    num_files = math.ceil(space_to_fill / dummy_size_bytes)
    
    print(f"Memulai pengisian {space_to_fill / (1024**3):.2f}GB ruang kosong...")
    print(f"Buat {num_files} file @ {dummy_size_mb}MB")

    # Buat file dummy
    for i in range(num_files):
        # Hitung ukuran file (file terakhir mungkin lebih kecil)
        current_size = min(dummy_size_bytes, space_to_fill)
        if current_size <= 0:
            break

        # Generate nama file unik
        timestamp = int(time.time())
        dummy_name = f"dummy_{timestamp}_{random.randint(1000,9999)}.dat"
        dummy_path = os.path.join(dummy_dir, dummy_name)
        
        # Buat file dengan isi acak
        try:
            with open(dummy_path, 'wb') as f:
                f.write(os.urandom(current_size))
            
            # Update ruang yang tersisa
            space_to_fill -= current_size
            print(f"Dibuat: {dummy_name} ({current_size / (1024**2):.2f}MB)")
            
        except Exception as e:
            print(f"Gagal membuat file dummy: {str(e)}")
            break

def main():
    parser = argparse.ArgumentParser(description="Pengelola Disk Multi-OS")
    parser.add_argument('mode', choices=['organize', 'fill'], help="Mode operasi")
    parser.add_argument('--path', default=os.getcwd(), help="Path target (default: direktori saat ini)")
    parser.add_argument('--target-free', type=float, default=1, help="Target free space (GB) untuk mode fill")
    parser.add_argument('--dummy-size', type=int, default=100, help="Ukuran file dummy (MB) untuk mode fill")
    
    args = parser.parse_args()

    try:
        if args.mode == "organize":
            organize_files_by_extension(args.path)
            print("Organisasi file selesai!")
        else:
            fill_disk_space(
                path=args.path,
                target_free_gb=args.target_free,
                dummy_size_mb=args.dummy_size
            )
            print("Pengisian disk selesai!")
    except Exception as e:
        print(f"Terjadi kesalahan: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()