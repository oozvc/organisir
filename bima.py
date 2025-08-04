import os
import shutil
import argparse
import time
import random
import math
import sys
import platform

def organize_files_by_extension(path):
    """Mengorganisir file berdasarkan ekstensi ke dalam folder terpisah"""
    print(f"\nMemulai organisasi file di: {path}")
    if not os.path.exists(path):
        print(f"✖ Path tidak ditemukan: {path}")
        return

    file_count = 0
    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)
        
        if os.path.isfile(filepath) and not filename.startswith("dummy_"):
            ext = os.path.splitext(filename)[1]
            ext = ext[1:] if ext else "NoExtension"
            
            dest_dir = os.path.join(path, ext.upper() + "_FILES")
            os.makedirs(dest_dir, exist_ok=True)
            
            try:
                shutil.move(filepath, os.path.join(dest_dir, filename))
                file_count += 1
                print(f"✓ Memindahkan: {filename} -> {ext.upper()}_FILES/")
            except Exception as e:
                print(f"✖ Gagal memindahkan {filename}: {str(e)}")
    
    print(f"\n✅ Organisasi selesai! {file_count} file dipindahkan.")

def fill_disk_space(path, target_free_gb=1, dummy_size_mb=100):
    """Mengisi ruang disk dengan file dummy"""
    print(f"\nMemulai pengisian disk di: {path}")
    
    try:
        total, used, free = shutil.disk_usage(path)
    except Exception as e:
        print(f"✖ Gagal membaca penggunaan disk: {str(e)}")
        return

    free_gb = free / (1024 ** 3)
    print(f"Ruang kosong saat ini: {free_gb:.2f}GB")
    
    target_free_bytes = target_free_gb * (1024 ** 3)
    space_to_fill = free - target_free_bytes
    
    if space_to_fill <= 0:
        print(f"✓ Ruang sudah cukup (target: {target_free_gb}GB)")
        return

    dummy_dir = os.path.join(path, "DUMMY_FILES")
    os.makedirs(dummy_dir, exist_ok=True)
    
    dummy_size_bytes = dummy_size_mb * (1024 ** 2)
    num_files = math.ceil(space_to_fill / dummy_size_bytes)
    
    print(f"➤ Akan membuat {num_files} file dummy @ {dummy_size_mb}MB")
    print(f"➤ Total ruang yang akan diisi: {space_to_fill/(1024**3):.2f}GB")

    for i in range(num_files):
        current_size = min(dummy_size_bytes, space_to_fill)
        if current_size <= 0:
            break

        timestamp = int(time.time())
        dummy_name = f"dummy_{timestamp}_{random.randint(1000,9999)}.dat"
        dummy_path = os.path.join(dummy_dir, dummy_name)
        
        try:
            with open(dummy_path, 'wb') as f:
                f.write(os.urandom(current_size))
            
            space_to_fill -= current_size
            print(f"✓ Berhasil membuat: {dummy_name} ({current_size/(1024**2):.2f}MB)")
        except Exception as e:
            print(f"✖ Gagal membuat file dummy: {str(e)}")
            if 'disk full' in str(e).lower():
                print("! Ruang disk penuh, proses dihentikan")
                break
    
    new_free = shutil.disk_usage(path).free / (1024 ** 3)
    print(f"\n✅ Pengisian selesai! Ruang kosong sekarang: {new_free:.2f}GB")

def main():
    print(f"\n{'='*50}")
    print(f"DISK MANAGER TOOL (Multi-OS v1.2) by bhimantara")
    print(f"OS: {platform.system()} {platform.release()}")
    print(f"{'='*50}")
    
    parser = argparse.ArgumentParser(description="Pengelola Disk Multi-OS")
    parser.add_argument('mode', choices=['organize', 'fill'], help="Mode operasi")
    parser.add_argument('--path', default=os.getcwd(), help="Path target (default: direktori saat ini)")
    parser.add_argument('--target-free', type=float, default=1, help="Target free space (GB) untuk mode fill")
    parser.add_argument('--dummy-size', type=int, default=100, help="Ukuran file dummy (MB) untuk mode fill")
    
    args = parser.parse_args()

    try:
        if args.mode == "organize":
            organize_files_by_extension(args.path)
        else:
            fill_disk_space(
                path=args.path,
                target_free_gb=args.target_free,
                dummy_size_mb=args.dummy_size
            )
    except KeyboardInterrupt:
        print("\n⚠ Program dihentikan oleh pengguna")
    except Exception as e:
        print(f"\n✖ Error fatal: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
