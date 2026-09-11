# Sierra SPT Downpatcher — Legacy Project

> **This repository contains the legacy version of the SPT downpatcher.**  
> Development has moved to the newer **Sierra Installer/Patcher**, which is the recommended version for current use.

## Looking for the current SPT installer / patcher?

### [Open the current Sierra Installer/Patcher](https://52sierra.net/patcher/)

The current installer/patcher is designed to install supported and archived SPT versions from a compatible Escape from Tarkov installation.

It replaces this older downpatcher with a more complete workflow, including automatic source detection and copying, integrity verification, resumable web delivery, archived packages, prerequisite checks, logging, and a modern GUI.

**Current source repository:**  
[github.com/52sierra-main/sierra_spt_patcher](https://github.com/52sierra-main/sierra_spt_patcher)

**Support / Discord:**  
[discord.gg/uKMW8PxE8s](https://discord.gg/uKMW8PxE8s)

---

## About this legacy repository

This project was the original **SPT downpatcher / SPT downgrader** used to create and apply binary patches between different Escape from Tarkov client versions for compatibility with older SPT releases.

It contains two main Python tools:

- `patch_generator.py` — compares source and target directory trees and produces binary patch data, additional files, and a delete list.
- `patcher.py` — applies those generated patches to a selected directory and handles additional/deleted files automatically.

This code remains available as a historical reference, but it is **not the recommended installer for current SPT use**.

For current releases, archived-version installation, troubleshooting, and support, use the Sierra Installer/Patcher linked above.

---

## Legacy patch generator

`patch_generator.py` recursively compares a source directory with a target directory and builds a patch package that mirrors the target folder structure.

For files that changed, it creates binary diff files in the corresponding relative locations. Files that exist only in the target are copied into a separate additional-files tree, while files that exist only in the source are recorded in a delete list for removal during patching.

The legacy generator requires its source/output paths to be configured manually in the script. Patch generation uses `ThreadPoolExecutor` for parallel processing.

## Legacy patcher

`patcher.py` applies the generated patch directory, copies additional files, and processes the delete list.

The user selects the directory to patch through a Tkinter folder picker, after which the patching process is automated.

The legacy package also uses a manually created `.info` metadata file for basic client-version compatibility checking. This workflow has been superseded by the newer Sierra Installer/Patcher.

The old script can be packaged as a portable executable with PyInstaller, for example:

```text
pyinstaller --onefile --console patcher.py
```

Historical package layout example:

![Legacy patcher folder layout](https://github.com/user-attachments/assets/5225de4e-e724-48d3-a2b4-dfee109d7482)

---

## Project status

This repository is retained for legacy/reference purposes. New development and releases are maintained in the current Sierra Installer/Patcher repository.

Sierra Installer/Patcher is an independent community project and is not affiliated with or endorsed by Battlestate Games or the SPT project.
