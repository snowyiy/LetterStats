import customtkinter as ctk
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


class LetterStats:
    def __init__(self):
        self.letter_freq = []
        self.dark_theme = True

        # image
        self.img_dark_light_switch_button = ctk.CTkImage(light_image=Image.open("./assets/sun.png"),
                                                         dark_image=Image.open("./assets/moon.png"))
        self.img_info = ctk.CTkImage(Image.open("./assets/info.png"))
        self.img_settings = ctk.CTkImage(Image.open("./assets/setting.png"))


    def drawGraph(self):
        pass


    def calculFreq(self):
        pass
    

    def showInfos(self):
        pass


    def showSettings(self):
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
        root.geometry("900x600")
        root.resizable(width=False, height=False)   # Optional (not to fix my laziness but a feature)
        root.grid_columnconfigure(0, weight=1)
        ctk.deactivate_automatic_dpi_awareness()
        

        btn_switch_theme = ctk.CTkButton(root,
                                         text="",
                                         width=20,
                                         height=20,
                                         image=self.img_dark_light_switch_button,
                                         fg_color="#aca6a6",
                                         hover_color="#c5bcbc",
                                         command=self.switchTheme
        ).place(x=860, y=10)

        btn_settings = ctk.CTkButton(root,
                                    text="",
                                    width=20,
                                    height=20,
                                    image=self.img_settings,
                                    fg_color="#aca6a6",
                                    hover_color="#c5bcbc",
                                    command=self.showSettings
        ).place(x=10, y=10)
        
        btn_info = ctk.CTkButton(root,
                                text="",
                                width=20,
                                height=20,
                                image=self.img_info,
                                fg_color="#aca6a6",
                                hover_color="#c5bcbc",
                                command=self.showInfos
        ).place(x=60, y=10)



        txt_text_box = ctk.CTkTextbox(root,
                                      height=425, width=350, 
                                      border_width=4,
                                      border_color="black",
                                      font=("Arial", 16)
        ).place(x=25, y=75)




        root.mainloop()



if (__name__== "__main__"):
    LetterStats().main()
