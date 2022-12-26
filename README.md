# ue2rv
Takes High Res screenshot in Unreal Engine and sends it to Shotgrid RV.

## Installation
- Add the ue2rv.py script in one of the folders specified in the documentations here : https://docs.unrealengine.com/scripting-the-unreal-editor-using-python/#pythonenvironmentandpathsintheunrealeditor
- Set environement variable RVPUSH to your rvpush.exe file path. 

## Usage
in the command line window, set it to python and type the following each time you want to take a screenshot:
```py
ue2rv()
```

## How it works ?
- Takes a screenshot of the current viewport
- check for screenshot to be generated on disc
- call rvpush.exe to send the screenshot to the current RV session. (if it can't find a RV session, rvpush, will create a new rv session with the tag "unreal"). 
