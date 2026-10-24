---
title: "Windows Subsystem for Linux"
weight: 20
---

The Windows Subsystem for Linux (WSL) runs Linux distributions on Windows. Under WSL 2, every installed distribution runs on one Linux kernel inside a lightweight utility virtual machine, which `wsl --shutdown` stops along with every running distribution. Each distribution has its own file system, reached from Windows at `\\wsl.localhost\<distribution>\`, while the Windows drives appear inside Linux under `/mnt/`, so `C:\` is `/mnt/c`.

[Git on WSL Ubuntu 26.04](/wiki/git/wsl-setup) installs a distribution from scratch and sets it up for Git and GitHub.

## External references

- Microsoft, [What is the Windows Subsystem for Linux?](https://learn.microsoft.com/en-us/windows/wsl/about)
- Microsoft, [Install WSL](https://learn.microsoft.com/en-us/windows/wsl/install) and [basic commands](https://learn.microsoft.com/en-us/windows/wsl/basic-commands)
- Microsoft, [Working across Windows and Linux file systems](https://learn.microsoft.com/en-us/windows/wsl/filesystems)
- [microsoft/WSL](https://github.com/microsoft/WSL) on GitHub, for releases and issues
- Wikipedia, [Windows Subsystem for Linux](https://en.wikipedia.org/wiki/Windows_Subsystem_for_Linux)
