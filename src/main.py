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



class LetterStats:
    def __init__(self):
        self.root = ctk.CTk()
        self.letter_freq = []
        self.dark_theme = None   # get from settings file
        self.config_file = "config.json"
        self.settings_file = "settings.json"
        self.database_file = "language.json"
        self.update_db = None   # get from settings file
        self.app_name = None   # get from config file
        self.version = None   # get from config file
        self.repo_url = None   # get from config file
        self.author = None   # get from config file
        self.dictionnary = {"a" : 0.0, "z" : 0.0, "e" : 0.0, "r" : 0.0, "t" : 0.0, "y" : 0.0, "u" : 0.0, "i" : 0.0, "o" : 0.0, "p" : 0.0, "q" : 0.0, "s" : 0.0, "d" : 0.0, "f" : 0.0, "g" : 0.0, "h" : 0.0,
                            "j" : 0.0, "k" : 0.0, "l" : 0.0, "m" : 0.0, "w" : 0.0, "x" : 0.0, "c" : 0.0, "v" : 0.0, "b" : 0.0, "n" : 0.0, "é" : 0.0, "ç" : 0.0, "è" : 0.0, "à" : 0.0, "ù" : 0.0, "ê" : 0.0}

        self.txt_text_box = ctk.CTkTextbox(self.root,
                                      height=425, width=350, 
                                      border_width=4,
                                      border_color="black",
                                      wrap="word",
                                      font=("Monospace", 16)
        )

        self.btnswitch_update_db = ctk.CTkSwitch(self.root,
                                                text="Update Lang database",
                                                command=lambda: self.changeUpdateDb(),
                                                font=('Monospace', 16)
        ).pack(anchor=ctk.CENTER, pady=60)


        # image
        self.img_dark_light_switch_button = ctk.CTkImage(light_image=Image.open("./assets/sun.png"),
                                                         dark_image=Image.open("./assets/moon.png"))
        self.img_info = ctk.CTkImage(Image.open("./assets/info.png"))
        self.img_settings = ctk.CTkImage(Image.open("./assets/setting.png"))


    def updateJsonDatabase(self, lang):
        with open(self.database_file, "r+") as data_file_r:
            for letter in self.dictionnary.keys():
                data = json.load(data_file_r)
                freq = float(data[lang][letter]["freq"])
                freq_num = float(data[lang][letter]["freq_num"]) + 1.0
                new_freq = self.dictionnary[letter] + freq / freq_num 
                
                data[lang][letter]["freq"] = new_freq
                data[lang][letter]["freq_num"] = freq_num
            data_file_r.close()
            
        with open(self.database_file, "w+") as data_file_w:
            for letter in self.dictionnary.keys():
                json.dump(data, data_file_w)
            data_file_w.close()


    def drawGraph(self) -> None:
        x = np.arange(len(self.dictionnary))

        plt.bar(x, height=self.dictionnary.values())
        plt.xticks(x, self.dictionnary.keys())
        plt.ylabel("Frequence")
        plt.xlabel("Letters")
        plt.show()


    def calculFreq(self, text) -> None:
        for letter in text:
            if (letter.lower() in self.dictionnary.keys()):
                self.dictionnary[letter.lower()] += 1.0

        for letter in self.dictionnary:
            self.dictionnary[letter.lower()] /= len(text)
        
        if (self.update_db):
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
                                  text=f"{self.app_name} v{self.version}\nMade By {self.author}",
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
        with open(self.settings_file, "r+") as settings_r:
            data = json.load(settings_r)
            data["dark_theme"] = self.dark_theme
            settings_r.close()
        with open(self.settings_file, "w+") as settings_w:
            json.dump(data, settings_w)
            settings_w.close()

    
    def changeUpdateDb(self):
        self.update_db = not self.update_db
        with open(self.settings_file, "r+") as settings_r:
            data = json.load(settings_r)
            settings_r.close()
        data["update_db"] = self.update_db
        with open(self.settings_file, "w+") as settings_w:
            json.dump(data, settings_w)
            settings_w.close()


    def loadTheme(self) -> str:
        with open(self.settings_file, "r+") as settings:
            data = json.load(settings)
            settings.close()
        self.dark_theme = data["dark_theme"]
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


    def loadSettings(self):
        if not os.path.exists(self.settings_file):
            jsonwrite = ''' 
            {
                "dark_theme": true,
                "update_db": false
            }
            '''
            jsonwrite = json.loads(jsonwrite)

            with open(self.settings_file, "w+") as settings:
                json.dump(jsonwrite, settings)
                settings.close()
        else:
            with open(self.settings_file, "r+") as settings:
                data = json.load(settings)
                settings.close()
            self.update_db = data["update_db"]
            if self.update_db:
                self.btnswitch_update_db.select()


    def loadConfig(self):
        with open(self.config_file, "r+") as config:
            data = json.load(config)
            config.close()
        self.app_name = data["App"]["name"]
        self.version = data["App"]["version"]
        self.author = data["App"]["author"]
        self.repo_url = data["App"]["repo_url"]



    def main(self) -> None:
        self.loadSettings()
        self.loadConfig()

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
