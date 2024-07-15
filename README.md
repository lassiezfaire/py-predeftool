# py-predeftool

Cross-platform CLI tool for extracting preinstalled content from cellphone firmware packages.

py-predeftool is heavily based on and inspired by gtrxAC's [predeftool](https://github.com/gtrxAC/predeftool) scripts, but meant to work on more computers with more firmware types.

## Compatibility
Tool supports only Nokia DCT-4 for now. Tool is work-in-progress for now, so feel free to contact me if you have something to add. List of devices tool was tested on is below. Note that if your device is not on the list, it's not mandatory tool is not working with it.

### Nokia
#### Nokia DCT-4
- RM-394 (Nokia 1680 classic)

# System requirments
Tool is meant to be cross-platform and was tested on such operating systems:
- Windows 11 23H2
- Ubuntu 24.04 LTS

# Dependencies
- Python 3
- Wine 9.0 or higher (GNU/Linux)
- WSL 2.0 or higher (Windows)

Tool also uses some old software to unarchive firmware packages. I don't if I can distribute it here so find it somewhere online:
- i6comp.exe
- IsXunpack.exe
- ZD51145.DLL

Then put it in `tools` folder in root directory of the tool(where `main.py` is located by).
# How to use
1. Find firmware packages somewhere online ([here](https://archive.org/details/Nokia_DCT4_firmwares), for example) and put them in `packages` folder in root directory of the tool.
2. Run `python main.py` (in cmd.exe, Windows) or `python3 main.py` (bash, GNU/Linux).
3. Extracted content will be located in `content` folder in root directory of the tool.
# To Do
- [ ] Clear code
- [ ] Test if tool can handle multiple packages at once 
- [ ] Add parameters
- [ ] Add check if dependecies are installed
- [ ] Write script to install dependencies at once
- [ ] Test the tool on more systems