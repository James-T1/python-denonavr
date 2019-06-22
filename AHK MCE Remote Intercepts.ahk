;;;;; Begin AHK excerpt. Add this to a .ahk file and run it, and for long
;;;;; term use, drop it or a shortcut to the .ahk file into your Startup
;;;;; folder so it will run when you boot.

; https://www.thegreenbutton.tv/forums/viewtopic.php?f=7&t=7555
;    Good keybinding / keysend stuff here.

#NoEnv
#LTrim
#SingleInstance force

#WinActivateForce
SendMode Input
SetTitleMatchMode 1 ; At start

return

F13:: ; [Color Red] --> Toggle DynEq
    oHttp := ComObjCreate("WinHttp.Winhttprequest.5.1")
    oHttp.open("GET","http://127.0.0.1:5557/ps/toggle_reflev")
    oHttp.send()
    return
F14:: ; [Color Green] --> Toggle DynVolume
    oHttp := ComObjCreate("WinHttp.Winhttprequest.5.1")
    oHttp.open("GET","http://127.0.0.1:5557/ps/toggle_dynvolume")
    oHttp.send()
    return
F15:: ; [Color Yellow] --> Toggle DynEq
    oHttp := ComObjCreate("WinHttp.Winhttprequest.5.1")
    oHttp.open("GET","http://127.0.0.1:5557/volume/down3")
    oHttp.send()
    return
F16:: ; [Color Blue] --> Toggle DynVolume
    oHttp := ComObjCreate("WinHttp.Winhttprequest.5.1")
    oHttp.open("GET","http://127.0.0.1:5557/volume/up3")
    oHttp.send()
    return


