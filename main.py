import customtkinter as ctk
from customtkinter import *
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import webbrowser
import sqlite3
from CTkMessagebox import CTkMessagebox
import json
import os


from database_handler import DatabaseHandler
databasehandler = DatabaseHandler("data.db")


class LetterStats:
    def __init__(self):
        self.root = ctk.CTk()
        self.letter_freq = []
        self.dark_theme = True
        self.config_file = "config.json"
        self.database_file = "language.json"
        self.update = True
        self.version = None   # get from config
        self.repo_url = None   # get from config
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


    def updateJsonDatabase(self, lang):
        with open(self.database_file, "r+") as data_file:
            for letter in self.dictionnary.keys():
                # Read
                freq = json.load(data_file)[lang][letter]["freq"]
                freq_num = json.load(data_file)[lang][letter]["freq_num"]
                new_freq = (float(self.dictionnary[letter]) + float(freq)) / freq_num + 1 
                # Write
                
            config_file.close()



    def drawGraph(self) -> None:
        x = np.arange(len(self.dictionnary))

        plt.bar(x, height=self.dictionnary.values())
        plt.xticks(x, self.dictionnary.keys())
        plt.ylabel("Frequence")
        plt.xlabel("Letters")
        plt.show()


    def calculFreq(self, text) -> None:
        for letter in text:
            if (letter in self.dictionnary.keys()):
                self.dictionnary[letter] += 1.0


        for letter in self.dictionnary:
            self.dictionnary[letter] /= len(text)
        
        if (self.update):
            dialog = ctk.CTkInputDialog(text="Type in the language :", title="Language")
            lang = dialog.get_input()
            self.updateJsonDatabase(lang)

        
    def checkLettersCount(self, text) -> bool:
        size = 0
        for i in text:
            if (i in self.dictionnary.keys()):
                size += 1
        if (size < 150):
            CTkMessagebox(title="Error ! Not Enough Characters",
                          message="There must be at least 150 characters",
                          icon="cancel",
                          font=("Monospace", 16))
            return False
        else:
            return True


    def drawFromTextArea(self) -> None:
        text = self.txt_text_box.get("0.0", "end")

        if (self.checkLettersCount(text)):
            self.calculFreq(text)
            self.drawGraph()

    def drawFromFile(self) -> None:
        file_text = filedialog.askopenfilename()
        text = open(file_text, "r+").read()

        if (self.checkLettersCount(text)):
            self.calculFreq(text)
            self.drawGraph()


    def openGithubPage(self) -> None:
        webbrowser.open_new_tab(self.repo_url)
        

    def showInfos(self) -> None:
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


    def showSettings(self) -> None:
        top_settings = ctk.CTkToplevel(self.root)
        top_settings.title("Settings")
        top_settings.resizable(height=False, width=False)
        top_settings.geometry("240x144")
        

    def changeDefaultTheme(self):
        with open(self.config_file, "r+") as config_r:
            data = json.load(config_r)
            data["Settings"]["dark_theme"] = self.dark_theme
            config_r.close()
        with open(self.config_file, "w+") as config_w:
            json.dump(data, config_w)
            config_w.close()

    
    def loadTheme(self):
        with open(self.config_file, "r+") as config:
            data = json.load(config)
            config.close()
        self.dark_theme = data["Settings"]["dark_theme"]
        if (self.dark_theme):
            return "dark"
        else:
            return "light"


    def switchTheme(self) -> None:
        self.dark_theme = not self.dark_theme
        if (self.dark_theme):
            ctk.set_appearance_mode("dark")
            self.changeDefaultTheme()
        else:
            ctk.set_appearance_mode("light")
            self.changeDefaultTheme()


    def loadConfig(self):
        if not os.path.exists(self.config_file):
            jsonwrite = ''' 
            {
                "App": {
                    "name": "LettersStats",
                    "version": "0.0.1",
                    "author": "N&ko",
                    "Repo": "https://github.com/snowyiy/LetterStats"
                },
                "Settings": {
                    "dark_theme": true
                }
            }
            '''
            jsonwrite = json.loads(jsonwrite)

            with open(self.config_file, "w+") as config_file:
                json.dump(jsonwrite, config_file)
                config_file.close()


    def main(self) -> None:
        self.root.title("Letter Stats")
        ctk.set_appearance_mode(self.loadTheme())
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

        btn_calcul_freq_file = ctk.CTkButton(self.root, 
                                            text="Calcul Frequance From File",
                                            command=self.drawFromFile,
                                            font=("Monospace", 16)
        ).place(x=460, y=250)


        self.root.mainloop()



if (__name__== "__main__"):
    LetterStats().main()
