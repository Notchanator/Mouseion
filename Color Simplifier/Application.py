#AS PRACTICE REFACTOR TO OBJECT ORIENTED WHEN FINISHED
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename
from PIL import ImageTk, Image
from Color_Simplifier_Cats import main
from Color_Simplifier import main
from Helpers import *

def path_enter(event):
    global image_name
    global image_pixels
    valid = valid_path(path.get())
    if valid != "FileNotFoundError":
        image_pixels = Image.open(valid)
        image_name = ImageTk.PhotoImage(image_pixels.resize((600, 800), Image.ANTIALIAS).rotate(270, expand = True))
        image = ttk.Label(frame, image = image_name)
    else:
        image_name = ImageTk.PhotoImage(Image.open("Unkown_File.jpg"))
        image = ttk.Label(frame, image = image_name)
    image.grid(row = 0, column = 0)


def num_colors(event):
    global not_number_color
    value = color_num.get()
    if value == "" or value.isnumeric():
        try:
            not_number_color.grid_remove()
        except:
            pass
    else:
        not_number_color = ttk.Label(variables, text = "Must be an INTEGER", style = "Error.TLabel")
        not_number_color.grid(row = 4, column = 2)

def num_distance(event):
    global not_number_distance
    value = distance_num.get()
    if value == "" or value.isnumeric():
        try:
            not_number_distance.grid_remove()
        except:
            pass
    else:
        not_number_distance = ttk.Label(variables, text = "Must be an INTEGER", style = "Error.TLabel")
        not_number_distance.grid(row = 6, column = 2)

def simplifying_type():
    global color_num
    global color_num_lbl
    global distance_num
    global distance_num_lbl
    if check_var.get() == 0:
        color_num = ttk.Entry(variables, width = 3)
        color_num.bind("<Return>", num_colors)
        color_num_lbl = ttk.Label(variables, text = "Number of Colors")
        distance_num = ttk.Entry(variables, width = 5)
        distance_num.bind("<Return>", num_distance)
        distance_num_lbl = ttk.Label(variables, text = "Distance between Colors")
        color_num.grid(row = 3, column = 2, sticky = (E), padx = 98)
        color_num_lbl.grid(row = 3, column = 2, sticky = (W), padx = 15)
        distance_num.grid(row = 5, column = 2, sticky = (E), padx = 80)
        distance_num_lbl.grid(row = 5, column = 2, sticky = (W), padx = 15)
    else:
        try:
            color_num.grid_remove()
            color_num_lbl.grid_remove()
            distance_num.grid_remove()
            distance_num_lbl.grid_remove()            
        except:
            pass

#CANT SELECT FILETYPE IDK WHY SEEMS WEIRD
def save_file(): 
    save_imagename = asksaveasfilename(initialdir="/", title="Select file", 
    filetypes=[('JPEG', ('*.jpg', '*.jpeg', '*.jpe')), ('PNG', '*.png'), ('BMP', ('*.bmp', '*.jdib')), ('GIF', '*.gif')])
    image_pixels.show()
    image_pixels.save(save_imagename)

root = Tk()
root.title("Color Simplifier")
root.geometry("1200x700")

#(Width, Height)
style = ttk.Style()
style.configure("Error.TLabel", foreground = "red")
style.configure("Bottom.TButton", font = ("Helvetica", "32"))

variables = ttk.Frame(root)
frame = ttk.Frame(root, borderwidth = 10, relief = "ridge", width = 800, height = 600)
path = ttk.Entry(variables, width = 30)
path.bind("<Return>", path_enter)
path_lbl = ttk.Label(variables, text = "Image Path", width = 10)
check_var = IntVar()
checkbox = ttk.Checkbutton(variables, text = "Color Categories", variable = check_var, command = simplifying_type)
simplifying_type() #Get the right commands up
transform = ttk.Button(root, text = "Transform Image", style = "Bottom.TButton")
savefile = ttk.Button(root, text = "Save File", style = "Bottom.TButton", command = lambda : save_file())

variables.grid(row = 0, column = 2)
frame.grid(row = 0, column = 0, columnspan = 2, rowspan = 6)
path_lbl.grid(row = 0, column = 2, sticky = (N, W), padx = 15)
path.grid(row = 1, column = 2, sticky = (N, W), padx = 15, pady = 10)
checkbox.grid(row = 2, column = 2, sticky = (E))
transform.grid(row = 7, column = 1, sticky = (E), pady = 30, padx = 70)
savefile.grid(row = 7, column = 0, sticky = (W), pady = 30, padx = 90)


root.mainloop()


