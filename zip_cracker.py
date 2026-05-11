import zipfile
import pyzipper
import os
import sys
import time

def banner():
    os.system('clear')
    print("""
    \033[1;32m
     ███████╗██╗  ██╗    ███████╗██╗██████╗ ███████╗██████╗ 
     ██╔════╝██║  ██║    ╚══███╔╝██║██╔══██╗██╔════╝██╔══██╗
     █████╗  ███████║      ███╔╝ ██║██████╔╝█████╗  ██████╔╝
     ██╔══╝  ██╔══██║     ███╔╝  ██║██╔═══╝ ██╔══╝  ██╔══██╗
     ███████╗██║  ██║    ███████╗██║██║     ███████╗██║  ██║
     ╚══════╝╚═╝  ╚═╝    ╚══════╝╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝
                    \033[1;33m[ Advanced ZIP Utility Tool ]
                    \033[1;36mCode By: AiAgent | Version: 3.0
    \033[0m""")

def pause():
    input("\n\033[1;33m[!] Press Enter to return to Menu...\033[0m")

def view_info():
    banner()
    zip_path = input("\n[+] Enter ZIP file path: ")
    if not os.path.exists(zip_path):
        print("\033[1;31m[!] File not found!\033[0m")
        pause()
        return
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            print(f"\n\033[1;34m{'File Name':<30} {'Size (Bytes)':<15} {'Compressed'}\033[0m")
            print("-" * 60)
            for info in zf.infolist():
                print(f"{info.filename:<30} {info.file_size:<15} {info.compress_size}")
            
            is_encrypted = any(info.flag_bits & 0x1 for info in zf.infolist())
            print("-" * 60)
            status = "\033[1;31mYES (Locked)\033[0m" if is_encrypted else "\033[1;32mNO (Open)\033[0m"
            print(f"[*] Password Protected: {status}")
    except Exception as e:
        print(f"\033[1;31m[!] Error: {e}\033[0m")
    pause()

def create_zip():
    banner()
    source = input("\n[+] Enter file/folder path to ZIP: ")
    if not os.path.exists(source):
        print("\033[1;31m[!] Path not found!\033[0m")
        pause()
        return
    
    zip_name = input("[+] Enter output ZIP name: ")
    if not zip_name.endswith('.zip'): zip_name += '.zip'
    password = input("[+] Set a password (leave blank for none): ")
    
    try:
        with pyzipper.AESZipFile(zip_name, 'w', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as zf:
            if password:
                zf.setpassword(password.encode())
            
            if os.path.isfile(source):
                zf.write(source, os.path.basename(source))
            else:
                for root, dirs, files in os.walk(source):
                    for file in files:
                        zf.write(os.path.join(root, file), 
                                 os.path.relpath(os.path.join(root, file), os.path.join(source, '..')))
        print(f"\n\033[1;32m[✔] Success! Created: {zip_name}\033[0m")
    except Exception as e:
        print(f"\033[1;31m[!] Error: {e}\033[0m")
    pause()

def extract_zip():
    banner()
    zip_path = input("\n[+] Enter path of the ZIP to extract: ")
    if not os.path.exists(zip_path):
        print("\033[1;31m[!] File not found!\033[0m")
        pause()
        return
    
    output_dir = input("[+] Output folder (default: extracted): ") or "extracted"
    password = input("[+] Enter password (if any): ")
    
    try:
        with pyzipper.AESZipFile(zip_path) as zf:
            if password:
                zf.setpassword(password.encode())
            zf.extractall(path=output_dir)
        print(f"\n\033[1;32m[✔] Successfully extracted to: {output_dir}\033[0m")
    except Exception as e:
        print(f"\033[1;31m[!] Error: {e}\033[0m")
    pause()

def crack_zip():
    banner()
    zip_path = input("\n[+] Enter target ZIP path: ")
    wordlist_path = input("[+] Enter wordlist path: ")
    
    if not os.path.exists(zip_path) or not os.path.exists(wordlist_path):
        print("\033[1;31m[!] Files not found!\033[0m")
        pause()
        return
    
    try:
        with open(wordlist_path, 'rb') as wl:
            passwords = wl.readlines()
            
        print(f"[*] Total passwords: {len(passwords)}")
        start_time = time.time()
        
        with zipfile.ZipFile(zip_path) as zf:
            for i, line in enumerate(passwords):
                pwd = line.strip()
                # Progress update
                sys.stdout.write(f"\r\033[1;34m[*] Testing: {pwd.decode('utf-8', errors='ignore'):<20} [{i+1}/{len(passwords)}]\033[0m")
                sys.stdout.flush()
                
                try:
                    zf.extractall(pwd=pwd, path="cracked_files")
                    end_time = time.time()
                    print(f"\n\n\033[1;32m[+] SUCCESS! Password found: {pwd.decode()}\033[0m")
                    print(f"[*] Time taken: {round(end_time - start_time, 2)} seconds")
                    
                    with open("crack_results.txt", "a") as f:
                        f.write(f"ZIP: {zip_path} | Password: {pwd.decode()}\n")
                    break
                except:
                    continue
            else:
                print("\n\n\033[1;31m[-] Password not found in wordlist.\033[0m")
    except Exception as e:
        print(f"\n\033[1;31m[!] Error: {e}\033[0m")
    pause()

def main():
    while True:
        banner()
        print(" [1] Create Password Protected ZIP")
        print(" [2] Extract ZIP File (Standard/AES)")
        print(" [3] View ZIP Info (Metadata)")
        print(" [4] Crack ZIP Password (Brute Force)")
        print(" [0] Exit")
        
        choice = input("\n[?] Select an option: ")
        
        if choice == '1':
            create_zip()
        elif choice == '2':
            extract_zip()
        elif choice == '3':
            view_info()
        elif choice == '4':
            crack_zip()
        elif choice == '0':
            print("\nGoodbye!")
            break
        else:
            print("\033[1;31mInvalid choice!\033[0m")
            time.sleep(1)

if __name__ == "__main__":
    main()
