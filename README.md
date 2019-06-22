
# python-denonavr
#    forked from toebsen/python-denonavr

#   James-T1 fork - Includes Audyssey DynEq Reference Level + Dynamic Volume toggles:
#     * Autohotkey script to capture F13-F16 keys
#     * Windows 10 Registry key to remap MCE Remote red/green/yellow/blue buttons to F13-F16
#     * Fork changes _main_.py code to add in the Audyssey toggles.  Works on Denon AVR-X3400h and should work on x3500h and comparable Denon receivers as well.


`denonavr` is a Python 3.x package that provides state information and some control of an `Denon AVR X1000` device over a network.
This is achieved via a telnet connection and the [public protocol][1]

It includes `denonavr_server`, an HTTP server to facilitate RESTful access to a denon devices.

# Installing
1. Via source 
```
    Download & extract zip archive of the code from the "Clone or Download" button at the top right
        - Or using git:    git clone https://github.com/toebsen/python-denonavr.git
    cd python-denonavr
    pip install -r requirements.txt
    Modify _main_.py to include the IP address of your Denon receiver.  
        - You will also want to set the MAC address of your Denon up as a static DHCP assignment in your router
    Run:  python setup.py install
        - This will compile and create the executable
    Browse to the folder:   C:\Users\<USER NAME>\AppData\Local\Programs\Python\Python37-32\Scripts\
        - Run:  denonavr_server.exe
        - Folder name may vary depending on which version of Python3 you have installed.
        - Once you have everything working add a shortcut to this executable in your Startup folder
    Run the Autohotkey script included in the original python-denonavr folder:  AHK MCE Remote Intercepts.ahk
        - Once you have everything working add a shortcut to this AHK script in your Startup folder
    Run the registry key change to remap the Red and Green buttons on the MCE remote:
        - Back up the registry key first:  [HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\HidIr\Remotes\745a17a0-74d3-11d0-b6fe-00a0c90f57da]
        - Run file:   Registry- MCE Remote - v2 Color buttons to F13 on.reg
    You should now be able to use the Green and Red MCE buttons to toggle the Audyssey settings.
        - You can also use your web browser to toggle them from:  
        -   http://127.0.0.1:5557/ps/toggle_dynvolume
        -   http://127.0.0.1:5557/ps/toggle_reflev
```



2. Via docker
```
    docker run --rm -p 5567:5567 toebsen/python-denonavr:latest
```
# Running
Copy the denonavr.service file to /etc/systemd/system/. Modify the ExecStart path and arguments as necessary.

    systemctl enable denonavr.service  # Enable on boot
    systemctl start denonavr.service   # Start server
    systemctl stop denonavr.service    # Stop server

# Routes
All routes return JSON. 

## Power
- GET */power/state* - will return the current power state
- GET */power/turnon* - will turn on the device
- GET */power/turnoff* - will turn off the device
## Volume
- GET */volume/level* - get the current volume level
- GET */volume/set/<int:level_id>* - set the current volume (*level_id* is in DB)
## Input Source
- GET */input/state* - returns the current input source
- GET */input/switch/<source_id>* - will switch to the given source (*source_id* is one of "dvd", "bd, "game", "satcbl")


inspired by https://github.com/happyleavesaoc/python-firetv

[1]: https://www.denon.de/de/product/hometheater/avreceivers/avrx1000?docname=AVRX1000_E300_PROTOCOL(1000)_V01.pdf

