import PySimpleGUI as sg

sg.theme("white")
layout = [[sg.T("")], 
            [sg.Text("Please upload day 1 file in .edf format "),
             sg.Input(key="-IN01-" ,change_submits=True), 
             sg.FileBrowse(file_types = (("Edf files", "*.edf")), key="-IN1-")],     

            [sg.Text("Please upload day 2 file in .edf format "),
             sg.Input(key="-IN02-" ,change_submits=True), 
             sg.FileBrowse(file_types = (("Edf files", "*.edf")), key="-IN2-")],

            [sg.Text("Please upload day 2 file in .edf format "),
             sg.Input(key="-IN03-" ,change_submits=True), 
             sg.FileBrowse(file_types = (("Edf files", "*.edf")), key="-IN3-")],



            [sg.Button("Submit")]]

###Building Window
window = sg.Window('My File Browser', layout, size=(1200,300))
    
while True:
    event, values = window.read()
    print(values["-IN02-"])
    if event == sg.WIN_CLOSED or event=="Exit":
        break
    elif event == "Submit":
        print(values["-IN01-"])    



