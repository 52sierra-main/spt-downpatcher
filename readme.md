# Sierra SPT Downpatcher — Legacy Project

> **This repository contains the legacy version of the SPT downpatcher.**  
> Development has moved to the newer **Sierra Installer/Patcher**, which is the recommended version for current use.

## Looking for the maintained legacy SPT installer / patcher?
(This is probably what you're looking for. An installer for older versions of SPT)

### [Open the current Sierra Installer/Patcher](https://52sierra.net/patcher/)

**Sierra Installer/Patcher** is a Windows application for installing supported legacy **SPT (Single Player Tarkov)** versions(3.8.3, 3.9.8, 3.10.5, 3.11.4 and even down to 2.1.2) from your own live compatible Escape from Tarkov installation. It prepares a separate SPT folder, applies binary patches, and installs the additional files supplied by the selected release. 

### What the modern installer/patcher handles

- **Automatic Live Tarkov detection and copying.** With **Automatic copy (recommended)**, the installer detects your official Live Tarkov installation and copies it into a new or empty SPT destination. Copying and verification run in parallel, and the destination is read back to check that the copied bytes match. If detection is unavailable, **Use existing copy** lets you select a separate, fresh Tarkov copy. Never select your Live game folder as the SPT destination.
- **Exact source verification.** Current Web releases check the SHA-256 hashes of files required as binary-delta inputs against the release's expected source hashes before patching. Automatic Copy checks the Live source before copying and checks the destination afterward, before downloading the rest of the release. A matching version number alone is insufficient, and **Force cannot bypass exact source-hash verification**.
- **Resumable web delivery.** Packages are delivered as **content-addressed chunks**: each chunk is identified by the SHA-256 hash of its contents. The installer downloads and verifies these objects, reuses valid cached objects when retrying, and reconstructs the package files described by the release manifest. This avoids downloading completed chunks again after an interruption, while checking reconstructed package integrity.
- **Archived snapshots.** A release can be preserved as a local/offline snapshot containing its release metadata and required objects. Keep the complete snapshot together and select **Archived snapshot** to install from it. Archive objects are verified before use; a snapshot still needs compatible Tarkov source files and the required runtimes.
- **Runtime prerequisite checks.** For releases with prerequisite metadata, the installer checks for the required Microsoft .NET/ASP.NET runtime family and minimum version, and warns when components are missing. Follow the requirement shown for your selected SPT release; a newer major runtime does not necessarily replace an older one.
- **A graphical installation workflow.** The GUI brings together release selection, Web or Archived source mode, Automatic Copy, destination selection, progress, and logs. Advanced settings provide separate controls for copying/verification, downloading, and package reconstruction.
- **Logging and troubleshooting.** Session logs record the selected release, installation mode, integrity results, and errors. The **Logs** tab lets you save or copy a log and open its folder for support. Download/preparation failures can normally reuse cached data on retry; if patch application has already started and fails, begin again with a fresh destination. Review logs for local paths and system information before posting publicly.

### Integrity and trust

The installer applies patch data to your own Tarkov copy rather than providing a complete standalone game installation. Source checks establish compatibility with the selected patch; chunk and package hashes check that downloaded data matches the release metadata. **These integrity checks do not independently establish who published that metadata or guarantee that software is safe.** Obtain the installer and packages through the project links below, and keep your official Live installation separate from the SPT destination.

For installation steps, compatibility errors, runtime warnings, and recovery guidance, see the [current user guide](https://github.com/52sierra-main/sierra_spt_patcher/blob/main/USER_GUIDE.md).

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
