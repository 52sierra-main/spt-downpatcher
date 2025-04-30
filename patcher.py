import os
import sys
import shutil
import psutil
import subprocess
import tempfile, binascii
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from tkinter import Tk, filedialog
import time
from time import sleep
import win32api # pip install pywin32
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm # pip install tqdm

# in order to compile this and keep all the dialogues, in terminal, do [pyinstaller --console --onefile thisfilename.py]
# --onefile make it into one executable and not a slurge of files of which many people start asking you dumb shit cuz they decided to double click that instead of the exe for whatever reason

# had to add this because fucking pyinstaller messes up the working directory. without this, it starts at user\blahblah\appdata\blahblah....
def get_base_dir():
    """Return the base directory of the script or executable."""
    if getattr(sys, 'frozen', False):  # Check if running in a PyInstaller executable
        return os.path.dirname(sys.executable)  # Temporary directory for bundled files
    else:
        return os.path.dirname(os.path.abspath(__file__))  # Script's directory

# script_dir = os.path.dirname(os.path.abspath(__file__)) <-this was the original code when i was running off the python file itself
script_dir = get_base_dir()

# environment check
workers = psutil.cpu_count(logical=False) -1

# Paths
patch_dir = os.path.join(script_dir, "patchfiles")
hpatchz_path = os.path.join(script_dir, "bin", "x64", "hpatchz.exe")
log_file = "unipatch-log.txt"

def patch_check(dest_dir):
    """check for broken files"""
    typeA = ["tgikuvgt0dcv"]
    typeB = ["KpuvcnnaGHV"]
    root = os.path.basename(os.path.normpath(dest_dir))

    Alist = ["".join([chr(ord(c) - 2) for c in name]) for name in typeA]
    Blist = ["".join([chr(ord(c) - 2) for c in name]) for name in typeB]

    for A in Alist: 
        if os.path.exists(os.path.join(dest_dir, A)):
            input("error, code 3")
            exit(1)
        
    if root in Blist:
            input("error, code 3")
            exit(1)

    for B in Blist:
        if os.path.exists(B):
            input("error, code 3")
            exit(1)

# check client version
def version_check(file_path):
    """get escapefromtarkov.exe version"""
    try:
        info = win32api.GetFileVersionInfo(file_path, '\\')
        ms = info['FileVersionMS']
        ls = info['FileVersionLS']
        version = f"{ms >> 16}.{ms & 0xFFFF}.{ls >> 16}.{ls & 0xFFFF}"
        return version
    except Exception as e:
        print(f"Error, failed to check tarkov exe version, {file_path}. Error: {e}")
        return None

# use Tkinker to prompt the choose folder popup
def choose_directory():
    root = Tk()
    root.withdraw()  # Hide the main Tkinter window
    directory = filedialog.askdirectory(title="Select the copy-pasted tarkov client folder")
    if not directory:
        input("Choose something.")
        exit(1)
    
    # logic for checking for EscapeFromTarkov.exe and it's version as a foolproof design
    executable = os.path.join(directory, "EscapeFromTarkov.exe") 
    if not executable:
        input("Cannot detect escape from tarkov executable in the selected folder. Choose a correct target.")
        exit(1)
    if version_check(executable) != metadata['version']: # compares the version info on the metadata file and the exe file itself so ppl won't screw up
        input("The client version of the selected folder is not compatible with this patcher. Make sure that you have the latest tarkov client and patcher.")
        exit(1)
    return directory


# read metadata from the .info file
def read_metadata(script_dir):
    
    info_file = next(Path(script_dir).glob("*.info"), None)
    if not info_file:
        raise FileNotFoundError(f"Failed to find metadata file.")

    metadata = {}
    with open(info_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        metadata["version"] = lines[0].strip()
        metadata["title"] = lines[1].strip()
        metadata["description"] = lines[2].strip()
        metadata["dependencies"] = lines[3].strip() if len(lines) > 3 else None

    return metadata

def _recover_password(script_dir):
    keyfile = os.path.join(script_dir, ".af.key")
    with open(keyfile, "rb") as f:
        blob = f.read()
    return bytes(b ^ 0x5A for b in blob).decode()

def apply_storage(script_dir, dest_dir):
    archive = os.path.join(script_dir, "storage.sierra")
    if not os.path.isfile(archive):
        print("error, cannot find storage.")
        return

    pw   = _recover_password(script_dir)
    sevenzip = os.path.join(script_dir, "bin", "7za.exe")

    # 7z x archive -y -oDEST -pPASSWORD
    subprocess.check_call(
        [sevenzip, "x", "-y", f"-o{dest_dir}", f"-p{pw}", archive]
    )
    print("storage applied.")


# apply a single patch using hpatchz
def apply_patch(hdiff_file, dest_dir):
    relative_path = hdiff_file.relative_to(patch_dir).with_suffix("")  # Remove .hdiff suffix

    # construct the full destination path
    dest_file = Path(dest_dir) / relative_path

    # check for destination file 
    if not dest_file.exists():
        input(f"Warning!: Failed to find a target file! Delete the pasted folder, integrity-check the tarkov files from the BSG launcher and retry the installation steps! filename: {dest_file} ")
        exit(1)

    # apply 
    try:
        subprocess.run(
            [hpatchz_path, "-f", str(dest_file), str(hdiff_file), str(dest_file)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        tqdm.write(f"Patched: {dest_file}")
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to patch {dest_file}. Error: {e.stderr.decode()}")


def process_patches(dest_dir):
    # Process all .hdiff files in the patch directory.
    hdiff_files = list(Path(patch_dir).rglob("*.hdiff"))
    if not hdiff_files:
        input("Patch delta directory not found.")
        exit(1)

    print(f"Found {len(hdiff_files)} patch files. Applying...")

# used tqdm to create a progress bar
    with tqdm(total=len(hdiff_files), desc="Processing files", unit="hdiff") as progress:
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = [executor.submit(apply_patch, hdiff, dest_dir) for hdiff in hdiff_files]
            for future in as_completed(futures):
                progress.update(1)

    #with ThreadPoolExecutor(max_workers=6) as executor:
    #    for hdiff in hdiff_files:
    #        executor.submit(apply_patch, hdiff, dest_dir)


def finalize_patch(dest_dir):
    """ delete stuff and add additional files"""
    print("------------------")
    print("Adjusting files...")
    print("------------------")

    # read the list of files to delete from delete_list.txt
    delete_list_file = os.path.join(script_dir, "delete_list.txt")
    files_to_delete = []

    if os.path.exists(delete_list_file):
        with open(delete_list_file, "r", encoding="utf-8") as f:
            files_to_delete = [line.strip() for line in f if line.strip()]
    else:
        input(f"Delete list not found: {delete_list_file}")
        exit(1)

    # remove files 
    for file in files_to_delete:
        file_path = os.path.join(dest_dir, file)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
            except Exception as e:
                print(f"Failed to delete file: {file_path}. Error: {e}")
        else:
            print(f"Failed to find file(non-important error): {file_path}")

    # remove empty directories
    print("Removing empty directories...")
    for root, dirs, files in os.walk(dest_dir, topdown=False):  # Process subdirectories first
        for directory in dirs:
            dir_path = os.path.join(root, directory)
            if not os.listdir(dir_path):  # Check if the directory is empty
                try:
                    os.rmdir(dir_path)
                    print(f"Removed folder: {dir_path}")
                except Exception as e:
                    print(f"Failed to remove folder: {dir_path}. Error: {e}")
            else:
                print(f"Empty folders removed: {dir_path}")


if __name__ == "__main__":
    try:
        a = """

░██████╗██╗███████╗██████╗░██████╗░░█████╗░
██╔════╝██║██╔════╝██╔══██╗██╔══██╗██╔══██╗
╚█████╗░██║█████╗░░██████╔╝██████╔╝███████║
░╚═══██╗██║██╔══╝░░██╔══██╗██╔══██╗██╔══██║
██████╔╝██║███████╗██║░░██║██║░░██║██║░░██║
╚═════╝░╚═╝╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚═╝

██╗███╗░░██╗░██████╗████████╗░█████╗░██╗░░░░░██╗░░░░░███████╗██████╗░
██║████╗░██║██╔════╝╚══██╔══╝██╔══██╗██║░░░░░██║░░░░░██╔════╝██╔══██╗
██║██╔██╗██║╚█████╗░░░░██║░░░███████║██║░░░░░██║░░░░░█████╗░░██████╔╝
██║██║╚████║░╚═══██╗░░░██║░░░██╔══██║██║░░░░░██║░░░░░██╔══╝░░██╔══██╗
██║██║░╚███║██████╔╝░░░██║░░░██║░░██║███████╗███████╗███████╗██║░░██║
╚═╝╚═╝░░╚══╝╚═════╝░░░░╚═╝░░░╚═╝░░╚═╝╚══════╝╚══════╝╚══════╝╚═╝░░╚═╝"""
        print("")
        print("")
        print("-----------------------------------------------------------------------------------------------------------------")
        print("Clear mirror and calm water")
        print(a)
        print("")
        print("-----------------------------------------------------------------------------------------------------------------")
        print("")
        sleep(2)
        print("SPT installer made by 52sierra")
        sleep(3)
        print("")        
        print("reading metadata...")
        time.sleep(1)
        metadata = read_metadata(script_dir)
        print(f"Version: {metadata['version']}")
        print(f"Title: {metadata['title']}")
        print(f"Description: {metadata['description']}")
        print("press enter to continue")
        os.system("pause")

        # tkinter prompt
        print("choose the pasted folder:")
        dest_dir = choose_directory()
        patch_check(dest_dir)

        print("applying patch...")
        process_patches(dest_dir)
        print("patch complete")
        print("finishing task...")
        apply_storage(script_dir, dest_dir)
        finalize_patch(dest_dir)
        print("process complete, good luck and have fun!")
        print("")
        print("")
        print("-----------------------------------------")
        print("Support the author:")
        print("https://ko-fi.com/52sierra")
        print("-----------------------------------------")
        print("")
        print("")
        sleep(2)
        input("press enter to finish...")
    except Exception as e:
        print(f"ERROR: {e}")
