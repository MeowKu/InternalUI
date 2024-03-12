# InternalUI - Reworked
import sys
import subprocess
import pkg_resources

import requests
import os

internalVersion = "v3 - Reworked"
transparent_colour = None

# Load Config
try:
    import sys
    import json
    with open('./InternalFiles/theme.json', 'r') as handle:
        config = json.load(handle)
        fristRun = config['fristRun']
        banner = config['banner']

except Exception:
    pass

def download_file(url, save_path):
    response = requests.get(url)
    with open(save_path, 'wb') as f:
        f.write(response.content)

def checker():
    # Check if any module is missing.
    required = {'PySimpleGUI'}
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = required - installed

    if missing:
        print("[InternalUI]: PySimpleGUI is not install, Do you want to install it? (yes/no)")
        ans = input("")
        if (ans != "yes" or ans != "Yes"):
            return
        else:
            print("[InternalUI]: Installing PySimpleGUI...")
            python = sys.executable
            subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)

def Frist_Run():
    checker()
    import PySimpleGUI as sg
    layout = [
            [sg.Image(data=fristRun, pad=((0, 0), 0))]
        ]
    
    window = sg.Window("InternalUI {} | Loading...".format(internalVersion), no_titlebar=True, grab_anywhere=True, margins=(0,0)).Layout(layout)
    window.Read(timeout=5000)

    # download an internal updater
    url = 'https://github.com/MeowKu/InternalUI/blob/main/build.bat'
    save_path = 'setup.bat'
    download_file(url, save_path)
    os.system(save_path)
    os.system('cls')
    print(f"Setup successfully!")
    window.close()
    # TODO: delete batch after run it
    with open("InternalUI", "w") as file:
        file.write("InternalUI")

import time
file_path = "InternalUI"
if os.path.isfile(file_path):
    print(f"Skipping setting up...")
    time.sleep(1)
    os.system('cls')
else:
    os.system('cls')
    print(f"InternalUI is missing some file, Starting to automatic setup.")
    time.sleep(1)
    os.system('cls')
    Frist_Run()


def Main_Menu():
    import PySimpleGUI as sg
    #window = sg.Window("InternalUI {} | Main menu".format(internalVersion), transparent_color=transparent_colour).Layout(layout)
    #window.Read()
    #sg.change_look_and_feel("Tan")
    tab2_layout = [
        [sg.Text('Token Generator'),sg.Button('Token Gen', key="TG", border_width=0)],
        [sg.Text('Nitro Generator'),sg.Button('Nitro Gen', key="NG", border_width=0)]
               ]

    tab1_layout = [[sg.Text('Internal Token checker'),sg.Button('Token Checker', key="Checker", border_width=0)]]

    tab3_layout = [
        [sg.Button('[M] Mass', key="M", border_width=0)],
        [sg.Button('[M] Spammer', key="S", border_width=0)],
        [sg.Button('[M] Server', key="SE", border_width=0)],
        [sg.Button('[M] Voice', key="VC", border_width=0)],
        [sg.Button('Server Nuker', key="SN", border_width=0)]
                ]

    tab4_layout = [
        [sg.Text("Input something: "), sg.InputText("", key='-INPUT-'), sg.Button("Send")],
        [sg.Text("don't know what to input? try typing 'help' in the Input")]
                ]
    
    tab5_layout = [[sg.Text('Watch this window')],
                    [sg.Output(size=(40,5))]]       # generally better to use a Multline, but for super-simple examples, Output is OK
    tab6_layout = [[sg.Text('This is inside tab 6')]]

    layout = [
        [sg.Image(data=banner, pad=((0, 0), 0))],
        [sg.Text('InternalUI v3!')],
        [
        # Discord Tabs
        sg.Frame('Discord Tools', layout= [[sg.TabGroup([[sg.Tab('Token Stuff', tab1_layout, border_width=0), sg.Tab('Gen Stuff', tab2_layout, border_width=0), sg.Tab('Raid Stuff', tab3_layout, border_width=0), sg.Tab('Misc', tab4_layout, border_width=0)]]) ]]),
        # Changelogs
        sg.Frame('Internal Changelogs', layout= [[sg.Text("InternalUI - v3")], [sg.Text("[+]: Change the whole UI to make it easier to use")], [sg.Text("[+]: Improve some features")], [sg.Text("[+]: Removed in-game executor due to the tons of bugs (Will be add back soon!)")], [sg.Text("More infomation at Github")]])
        ],
        # In-Built Console
        [
        sg.Frame('Misc', layout= [[sg.TabGroup([[sg.Tab('Console', tab5_layout), sg.Tab('Soon...', tab6_layout)]]) ]])
        # Crypto Bot
        #sg.Frame('Crypto Miner (Beta)', layout= [[sg.Text("Input the address in config file.", sg.Button("Start", key="Crypto"))]])
        ],

        [sg.Col(layout=[[sg.Text('In a column')],
        #[sg.TabGroup([[sg.Tab('Tab 5', tab5_layout), sg.Tab('Tab 6', tab6_layout)]])],
        [sg.Button('Click me')]])],
            ]

    window = sg.Window("InternalUI {} | Main menu".format(internalVersion), transparent_color=transparent_colour, default_element_size=(12,1), finalize=True).Layout(layout)

    while True:
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED:           # always,  always give a way out!
            break

        if event == 'Send':
            if values["-INPUT-"] == "help":
                sg.popup("Internal Infomation\n\n[M] is for 'Multiple Token'\n\nMass - Send something to every person include 'Image, Text, Embed'\n\nSpammer - Spam something that you want to someone or random person\n\nServer - About the Server option like let the token in ur list join the server by using invite (proxy required)\n\nVoice - Join the voice channel by using id and yeah! you can make the token play something too!")
                print("Internal Infomation\n\n[M] is for 'Multiple Token'\n\nMass - Send something to every person include 'Image, Text, Embed'\n\nSpammer - Spam something that you want to someone or random person\n\nServer - About the Server option like let the token in ur list join the server by using invite (proxy required)\n\nVoice - Join the voice channel by using id and yeah! you can make the token play something too!")
        
        elif event == "Checker":
                p = subprocess.Popen([sys.executable,'InternalFiles/InternalFunction.py','checker',sys.executable], stderr=subprocess.STDOUT)
                
        elif event == "TG":
                p = subprocess.Popen([sys.executable,'InternalFiles/InternalFunction.py','TokenGen',sys.executable], stderr=subprocess.STDOUT)

        elif event == "M":
                p = subprocess.Popen([sys.executable,'InternalFiles/InternalFunction.py','Mass',sys.executable], stderr=subprocess.STDOUT)    
        
        elif event == "S":
                p = subprocess.Popen([sys.executable,'InternalFiles/InternalFunction.py','Mass',sys.executable], stderr=subprocess.STDOUT)  

        elif event == "SN":
                p = subprocess.Popen([sys.executable,'InternalFiles/InternalFunction.py','Nuker',sys.executable], stderr=subprocess.STDOUT)    

        elif event == "VC":
                p = subprocess.Popen([sys.executable,'InternalFiles/InternalFunction.py','Voice',sys.executable], stderr=subprocess.STDOUT)

        elif event == "Crypto":
                p = subprocess.Popen([sys.executable,'InternalFiles/InternalFunction.py','Crypto',sys.executable], stderr=subprocess.STDOUT)
            
    window.close()

Main_Menu()