import flet as ft

import controller


class View(object):
    def __init__(self, page: ft.Page):
        # Page
        self.btnSearch = None
        self.sentence = None
        self.ddSearch = None
        self.lvOut = None
        self.ddLanguage = None
        self.page = page
        self.page.title = "TdP 2024 - Lab 04 - SpellChecker ++"
        self.page.horizontal_alignment = 'CENTER'
        self.page.theme_mode = ft.ThemeMode.LIGHT
        # Controller
        self.__controller = None
        # UI elements
        self.__title = None
        self.__theme_switch = None

        # define the UI elements and populate the page

    def add_content(self):
        """Function that creates and adds the visual elements to the page. It also updates
        the page accordingly."""
        # title + theme switch
        self.__title = ft.Text("TdP 2024 - Lab 04 - SpellChecker ++", size=24, color="blue")
        self.__theme_switch = ft.Switch(label="Light theme", on_change=self.theme_changed)
        self.page.controls.append(
            ft.Row(spacing=30, controls=[self.__theme_switch, self.__title, ],
                   alignment=ft.MainAxisAlignment.START)
        )
        # Row1
        self.lvOut = ft.ListView(expand=1,spacing=10,padding=20,auto_scroll=True)
        self.ddLanguage = ft.Dropdown(label="Language", width=150, on_change=self.verifyLanguage)
        self.fillDdLanguage()
        row1 = ft.Row([self.ddLanguage])

        # Row2
        self.ddSearch = ft.Dropdown(label="Search Modality", width=200, on_change=self.verifySearch)
        self.fillSearch()
        self.sentence = ft.TextField(label="Add your text here", width=400)
        self.btnSearch = ft.ElevatedButton(text="Spell Check", on_click=self.handleSpellCheck)
        row2 = ft.Row([self.ddSearch, self.sentence, self.btnSearch])

        # Row3
        row3 = ft.Row([self.lvOut])
        self.page.add(row1, row2, row3)
        self.page.update()

    def update(self):
        self.page.update()

    def setController(self, controller):
        self.__controller = controller

    def theme_changed(self, e):
        """Function that changes the color theme of the app, when the corresponding
        switch is triggered"""
        self.page.theme_mode = (
            ft.ThemeMode.DARK
            if self.page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        self.__theme_switch.label = (
            "Light theme" if self.page.theme_mode == ft.ThemeMode.LIGHT else "Dark theme"
        )
        # self.__txt_container.bgcolor = (
        #     ft.colors.GREY_900 if self.page.theme_mode == ft.ThemeMode.DARK else ft.colors.GREY_300
        # )
        self.page.update()

    def fillDdLanguage(self):
        self.ddLanguage.options.append(ft.dropdown.Option("italian"))
        self.ddLanguage.options.append(ft.dropdown.Option("english"))
        self.ddLanguage.options.append(ft.dropdown.Option("spanish"))

    def verifyLanguage(self, e):
        self.lvOut.controls.append(ft.Text(controller.printLanguage(self.ddLanguage.value)))
        self.page.update()

    def fillSearch(self):
        self.ddSearch.options.append(ft.dropdown.Option("Default"))
        self.ddSearch.options.append(ft.dropdown.Option("Linear"))
        self.ddSearch.options.append(ft.dropdown.Option("Dichotomic"))

    def verifySearch(self, e):
        self.lvOut.controls.append(ft.Text(controller.printSearch(self.ddSearch.value)))
        self.page.update()

    def handleSpellCheck(self, e):
        sc = controller.SpellChecker(self)
        if self.ddLanguage.value is None:
            self.lvOut.controls.append(ft.Text("Select Language!", color="red"))
            self.page.update()
            return
        elif self.ddSearch.value is None:
            self.lvOut.controls.append(ft.Text("Select modality!", color="red"))
            self.page.update()
            return
        result,time = sc.handleSentence(self.sentence.value, self.ddLanguage.value, self.ddSearch.value)
        self.lvOut.controls.append(ft.Text(f"'{self.sentence.value}':", color="green"))
        self.lvOut.controls.append(ft.Text(f"{result}; Time:{time}.", color="green"))
        self.sentence.value = ""
        self.page.update()
