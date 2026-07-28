"""
===================================================================
BUILD SCRIPT FOR STANDALONE WINDOWS EXE
===================================================================
Membuat bundle executable Windows InstagramScraper.exe mandiri.
"""

import os
import sys
import subprocess

def main():
    print("===================================================================")
    print("MEMULAI BUILD STANDALONE WINDOWS EXE (InstagramScraper.exe)")
    print("===================================================================")
    
    root_dir = os.path.dirname(os.path.abspath(__file__))
    frontend_dist = os.path.join(root_dir, "frontend", "dist")
    
    if not os.path.exists(frontend_dist):
        print("Compiling frontend production build (npm run build)...")
        subprocess.run(["npm", "run", "build"], cwd=os.path.join(root_dir, "frontend"), shell=True, check=True)

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--onedir",
        "--name=InstagramScraper",
        f"--add-data={os.path.join(root_dir, 'frontend', 'dist')};frontend/dist",
        f"--add-data={os.path.join(root_dir, 'backend')};backend",
        os.path.join(root_dir, "launcher.py")
    ]
    
    print("\nRunning PyInstaller compilation command:")
    print(" ".join(cmd))
    
    res = subprocess.run(cmd, cwd=root_dir)
    if res.returncode == 0:
        print("\n===================================================================")
        print("BUILD STANDALONE EXE SUKSES SELESAI!")
        print("===================================================================")
        print("File Executable Windows Anda dapat ditemukan di:")
        print(os.path.join(root_dir, 'dist', 'InstagramScraper', 'InstagramScraper.exe') + "\n")
    else:
        print("Build PyInstaller gagal dengan exit code:", res.returncode)

if __name__ == "__main__":
    main()
