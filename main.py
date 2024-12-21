import customtkinter as ctk
from customtkinter import *
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import webbrowser


class LetterStats:
    def __init__(self):
        self.root = ctk.CTk()
        self.letter_freq = []
        self.dark_theme = True
        self.default_dark_theme = ctk.StringVar()
        self.version = "0.0.1"   # get from config
        self.repo_url = "https://github.com/snowyiy/LetterStats"  # get from config
        self.dictionnary = {"a" : 0.0, "z" : 0.0, "e" : 0.0, "r" : 0.0, "t" : 0.0, "y" : 0.0, "u" : 0.0, "i" : 0.0, "o" : 0.0, "p" : 0.0, "q" : 0.0, "s" : 0.0, "d" : 0.0, "f" : 0.0, "g" : 0.0, "h" : 0.0,
                            "j" : 0.0, "k" : 0.0, "l" : 0.0, "m" : 0.0, "w" : 0.0, "x" : 0.0, "c" : 0.0, "v" : 0.0, "b" : 0.0, "n" : 0.0, "é" : 0.0, "ç" : 0.0, "è" : 0.0, "à" : 0.0, "ù" : 0.0, "ê" : 0.0}

        self.txt_text_box = ctk.CTkTextbox(self.root,
                                      height=425, width=350, 
                                      border_width=4,
                                      border_color="black",
                                      wrap="word",
                                      font=("Monospace", 16)
        )

        # image
        self.img_dark_light_switch_button = ctk.CTkImage(light_image=Image.open("./assets/sun.png"),
                                                         dark_image=Image.open("./assets/moon.png"))
        self.img_info = ctk.CTkImage(Image.open("./assets/info.png"))
        self.img_settings = ctk.CTkImage(Image.open("./assets/setting.png"))


    def drawGraph(self):
        x = np.arange(len(self.dictionnary))
        #plt.hist(x, density=True, bins=30)
        plt.bar(x, height=self.dictionnary.values())
        plt.xticks(x, self.dictionnary.keys())
        plt.ylabel("Frequence")
        plt.xlabel("Letters")
        plt.show()


    def calculFreq(self):
        text = self.txt_text_box.get("0.0", "end")
        
        for letter in text:
            if (letter in self.dictionnary.keys()):
                self.dictionnary[letter] += 1.0

        for letter in self.dictionnary:
            self.dictionnary[letter] /= len(text)


    def drawFromTextArea(self):
        self.calculFreq()
        self.drawGraph()


    def openGithubPage(self):
        webbrowser.open_new_tab(self.repo_url)
        

    def showInfos(self):
        top_infos = ctk.CTkToplevel(self.root)
        top_infos.title("Infos")
        top_infos.resizable(height=False, width=False)
        top_infos.geometry("360x240")

        label_name = ctk.CTkLabel(top_infos,
                                  text=f"LetterStats v{self.version}\nMade By N&ko",
                                  font=('Monospace', 16)
        ).pack(anchor=ctk.CENTER, pady=10)

        btn_github = ctk.CTkButton(top_infos,
                                   text="Github Page",
                                   fg_color="black",
                                   text_color="#568be3",
                                   corner_radius=8,
                                   border_width=0,
                                   command=self.openGithubPage,
                                   font=('Monospace', 14)
        ).pack(anchor=ctk.CENTER, pady=10)


    def setDefaultTheme(self):
        if (self.default_dark_theme == "on"):
            self.dark_theme = True
        else:
            self.dark_theme = False

        #! EDIT CONFIG FILE


    def showSettings(self):
        top_settings = ctk.CTkToplevel(self.root)
        top_settings.title("Settings")
        top_settings.resizable(height=False, width=False)
        top_settings.geometry("240x144")
        
        self.default_dark_theme = ctk.StringVar(value="on")
        checkbox_color_theme = ctk.CTkCheckBox(top_settings,
                                               text="Dark Theme by Default",
                                               command=self.setDefaultTheme,
                                               variable=self.default_dark_theme,
                                               onvalue="on",
                                               offvalue="off"
        ).pack(anchor=ctk.CENTER, pady=60)


    def switchTheme(self):
        self.dark_theme = not self.dark_theme
        if (self.dark_theme):
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")


    def main(self):
        self.root.title("Letter Stats")
        ctk.set_appearance_mode("dark")
        self.root.geometry("900x600")
        self.root.resizable(width=False, height=False)   # Optional (not to fix my laziness but a feature)
        self.root.grid_columnconfigure(0, weight=1)
        ctk.deactivate_automatic_dpi_awareness()
        

        btn_switch_theme = ctk.CTkButton(self.root,
                                         text="",
                                         width=20,
                                         height=20,
                                         image=self.img_dark_light_switch_button,
                                         fg_color="#aca6a6",
                                         hover_color="#c5bcbc",
                                         command=self.switchTheme
        ).place(x=860, y=10)

        btn_settings = ctk.CTkButton(self.root,
                                    text="",
                                    width=20,
                                    height=20,
                                    image=self.img_settings,
                                    fg_color="#aca6a6",
                                    hover_color="#c5bcbc",
                                    command=self.showSettings
        ).place(x=10, y=10)
        
        btn_info = ctk.CTkButton(self.root,
                                text="",
                                width=20,
                                height=20,
                                image=self.img_info,
                                fg_color="#aca6a6",
                                hover_color="#c5bcbc",
                                command=self.showInfos
        ).place(x=60, y=10)


        self.txt_text_box.place(x=25, y=75)

        btn_calcul_freq_text_area = ctk.CTkButton(self.root, 
                                                  text="Calcul Frequance From Text",
                                                  command=self.drawFromTextArea,
                                                  font=("Monospace", 16)
        ).place(x=60, y=525)



        self.root.mainloop()



if (__name__== "__main__"):
    LetterStats().main()
