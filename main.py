import customtkinter as ctk
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


class LetterStats:
    def __init__(self):
        self.letter_freq = []
        self.dark_theme = True

        # image
        self.img_dark_light_switch_button = ctk.CTkImage(light_image=Image.open("./assets/sun.png"), dark_image=Image.open("./assets/moon.png"))


    def drawGraph(self):
        pass


    def calculFreq(self):
        pass
    

    def switchTheme(self):
        self.dark_theme = not self.dark_theme
        if (self.dark_theme):
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")


    def main(self):
        root = ctk.CTk()
        root.title("Letter Stats")
        ctk.set_appearance_mode("dark")
        root.geometry("1080x720")
        root.grid_columnconfigure(0, weight=1)
        ctk.deactivate_automatic_dpi_awareness()
        

        btn_switch_theme = ctk.CTkButton(root, text="", image=self.img_dark_light_switch_button, fg_color="#aca6a6", hover_color="#c5bcbc", command=self.switchTheme).grid(row=0, column=10, padx=10, pady=10)



        root.mainloop()



if (__name__== "__main__"):
    LetterStats().main()
