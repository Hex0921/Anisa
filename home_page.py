# -*- coding: utf-8 -*-
import math
import pathlib
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext
from typing import Dict
import pandas as pd
import io
from PIL import ImageTk, Image
import aiohttp
import asyncio

from fuzzywuzzy import fuzz
from datetime import datetime

import nest_asyncio

from commons import parse_datetime, get_month_days
from config import THEME_IMAGE, GENRE_LIST, AGE_GROUP_LIST, STUDIO_LIST, SEASON_LIST, FAVORITE_FILL_IMAGE, \
    FAVORITE_IMAGE, ANIMES_FILE, ANIMES_COLUMNS

nest_asyncio.apply()

from user_manager import User


def resize(w, h, w_box, h_box, pil_image):
    """resize a pil_image object so it will fit into
    a box of size w_box times h_box, but retain aspect ratio

    :param w: image width
    :param h: image height
    :param w_box: show box width
    :param h_box: show box height
    :param pil_image: pillow image object
    :return: a reise image ojbect
    """
    f1 = 1.0 * w_box / w  # 1.0 forces float division in Python2
    f2 = 1.0 * h_box / h
    factor = min([f1, f2])
    # print(f1, f2, factor) # test
    # use best down-sizing filter
    width = int(w * factor)
    height = int(h * factor)
    return pil_image.resize((width, height), Image.LANCZOS)


class HomeWinGUI(Tk):
    """Design home Page UI class
    """

    widget_dic: Dict[str, Widget] = {}

    def __init__(self, **kwargs):
        """ Init home page ui setting
        """
        super().__init__()
        self.__win()

        self.widget_dic["tk_frame_left"] = self.__tk_frame_left(self)

        self.widget_dic["tk_label_logo"] = self.__tk_label_logo(self.widget_dic["tk_frame_left"])

        self.widget_dic["tk_input_search"] = self.__tk_input_search(self.widget_dic["tk_frame_left"])
        self.widget_dic["tk_button_search"] = self.__tk_button_search(self.widget_dic["tk_frame_left"])

        self.widget_dic["tk_label_frame_filter"] = self.__tk_label_frame_filter(self.widget_dic["tk_frame_left"])

        self.widget_dic["tk_label_genre_filter"] = self.__tk_label_genre_filter(
            self.widget_dic["tk_label_frame_filter"])
        self.widget_dic["tk_select_box_genre_filter"] = self.__tk_select_box_genre_filter(
            self.widget_dic["tk_label_frame_filter"])

        self.widget_dic["tk_label_age_group_filter"] = self.__tk_label_age_group_filter(
            self.widget_dic["tk_label_frame_filter"])
        self.widget_dic["tk_select_box_age_group_filter"] = self.__tk_select_box_age_group_filter(
            self.widget_dic["tk_label_frame_filter"])

        # self.widget_dic["tk_label_studio_filter"] = self.__tk_label_studio_filter(
        #     self.widget_dic["tk_label_frame_filter"])
        # self.widget_dic["tk_select_box_studio_filter"] = self.__tk_select_box_studio_filter(
        #     self.widget_dic["tk_label_frame_filter"])

        self.widget_dic["tk_label_season_filter"] = self.__tk_label_season_filter(
            self.widget_dic["tk_label_frame_filter"])
        self.widget_dic["tk_select_box_season_filter"] = self.__tk_select_box_season_filter(
            self.widget_dic["tk_label_frame_filter"])

        self.widget_dic["tk_button_clear_search"] = self.__tk_button_clear_search(
            self.widget_dic["tk_label_frame_filter"])

        self.widget_dic["tk_label_frame_userinfo"] = self.__tk_label_frame_userinfo(self.widget_dic["tk_frame_left"])
        self.widget_dic["tk_label_user"] = self.__tk_label_user(self.widget_dic["tk_label_frame_userinfo"])
        self.widget_dic["tk_button_logout"] = self.__tk_button_logout(self.widget_dic["tk_label_frame_userinfo"])

        self.image_list = []

        self.favout_image = None
        self.limit = 15

        self.widget_dic["tk_tab_right"] = self.__tk_tab_right(self)

        self.widget_dic["tk_frame_page"] = self.__tk_frame_page(self.widget_dic["tk_tab_right"])

        self.widget_dic["tk_frame_page_favorite"] = self.__tk_frame_page(self.widget_dic["tk_tab_right"])

        self.widget_dic["tk_tab_right"].add(self.widget_dic["tk_frame_page"], text="Animation Library")
        self.widget_dic["tk_tab_right"].add(self.widget_dic["tk_frame_page_favorite"], text="My Favorite")

        self.widget_dic["tk_canvas_list"] = self.__tk_canvas_list(self.widget_dic["tk_frame_page"])
        self.widget_dic["tk_frame_list"] = self.__tk_frame_list(self.widget_dic["tk_canvas_list"])
        self.widget_dic["tk_canvas_list"].create_window((0, 0), window=self.widget_dic["tk_frame_list"], anchor='nw')
        self.widget_dic["tk_frame_list"].bind("<Configure>", self.frame_list_configure)

        self.widget_dic["tk_button_home_page"] = self.__tk_button_home_page(self.widget_dic["tk_frame_page"])
        self.widget_dic["tk_button_prev_page"] = self.__tk_button_prev_page(self.widget_dic["tk_frame_page"])
        self.widget_dic["tk_button_next_page"] = self.__tk_button_next_page(self.widget_dic["tk_frame_page"])
        self.widget_dic["tk_button_trail_page"] = self.__tk_button_trail_page(self.widget_dic["tk_frame_page"])
        self.widget_dic["tk_label_page_info"] = self.__tk_label_page_info(self.widget_dic["tk_frame_page"])

        self.widget_dic["tk_canvas_list_favorite"] = self.__tk_canvas_list(self.widget_dic["tk_frame_page_favorite"])
        self.widget_dic["tk_frame_list_favorite"] = self.__tk_frame_list(self.widget_dic["tk_canvas_list_favorite"])
        self.widget_dic["tk_canvas_list_favorite"].create_window((0, 0),
                                                                 window=self.widget_dic["tk_frame_list_favorite"],
                                                                 anchor='nw')
        self.widget_dic["tk_frame_list_favorite"].bind("<Configure>", self.frame_list_favorite_configure)

        self.widget_dic["tk_button_home_page_favorite"] = self.__tk_button_home_page(
            self.widget_dic["tk_frame_page_favorite"])
        self.widget_dic["tk_button_prev_page_favorite"] = self.__tk_button_prev_page(
            self.widget_dic["tk_frame_page_favorite"])
        self.widget_dic["tk_button_next_page_favorite"] = self.__tk_button_next_page(
            self.widget_dic["tk_frame_page_favorite"])
        self.widget_dic["tk_button_trail_page_favorite"] = self.__tk_button_trail_page(
            self.widget_dic["tk_frame_page_favorite"])
        self.widget_dic["tk_label_page_info_favorite"] = self.__tk_label_page_info(
            self.widget_dic["tk_frame_page_favorite"])

    def frame_list_configure(self, event):
        """ Design canvas panel scroll location

        :param event: event params
        :return: None
        """
        self.widget_dic["tk_canvas_list"].configure(scrollregion=self.widget_dic["tk_canvas_list"].bbox("all"))

    def frame_list_favorite_configure(self, event):
        """Design favorite canvas panel scroll location

        :param event: event params
        :return: None
        """
        self.widget_dic["tk_canvas_list_favorite"].configure(
            scrollregion=self.widget_dic["tk_canvas_list_favorite"].bbox("all"))

    def __win(self):
        """Design main gui params

        :return: None
        """
        self.title("Anisa  -  Home Page")
        self.config(bg='#FFEBCE')
        # Set window size and center
        # width = 1425
        # height = 740
        width = 1125
        height = 640
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)
        self.resizable(width=False, height=False)

    def scrollbar_autohide(self, bar, widget):
        """Design scrollbar auto hide

        :param bar: scrollbar object
        :param widget: widget object
        :return: None
        """
        self.__scrollbar_hide(bar, widget)
        widget.bind("<Enter>", lambda e: self.__scrollbar_show(bar, widget))
        bar.bind("<Enter>", lambda e: self.__scrollbar_show(bar, widget))
        widget.bind("<Leave>", lambda e: self.__scrollbar_hide(bar, widget))
        bar.bind("<Leave>", lambda e: self.__scrollbar_hide(bar, widget))

    def __scrollbar_show(self, bar, widget):
        """Show scrollbar

        :param bar: scrollbar object
        :param widget: widget object
        :return: None
        """
        bar.lift(widget)

    def __scrollbar_hide(self, bar, widget):
        """Hide scrollbar

        :param bar: scrollbar object
        :param widget: widget object
        :return: None
        """
        bar.lower(widget)

    def vbar(self, ele, x, y, w, h, parent):
        """Design scrollbar location

        :param ele: element control
        :param x: x place
        :param y: y place
        :param w: scrollbar width
        :param h: scrollbar height
        :param parent: where scrollbar parent control
        :return: None
        """
        sw = 15  # Scrollbar width
        x = x + w - sw
        vbar = Scrollbar(parent)
        ele.configure(yscrollcommand=vbar.set)
        vbar.config(command=ele.yview)
        vbar.place(x=x, y=y, width=sw, height=h)
        self.scrollbar_autohide(vbar, ele)

    def __tk_frame_left(self, parent):
        """Design left frame attribute

        :param parent: this control parent control
        :return: this control
        """
        frame = Frame(parent, width=200, height=620)
        frame.place(x=10, y=10, width=200, height=620)
        return frame

    def __tk_tab_right(self, parent):
        """Design right tab attribute

        :param parent: this control parent control
        :return: this control
        """
        tab = ttk.Notebook(parent, width=900, height=620)
        tab.place(x=215, y=10, width=900, height=620)
        return tab

    def __tk_frame_page(self, parent):
        """Design frame page attribute

        :param parent: this control parent control
        :return: this control
        """
        frame = Frame(parent, width=900, height=620)
        frame.place(x=0, y=0, width=900, height=620)
        return frame

    def __tk_label_logo(self, parent):
        """Design logo label attribute

        :param parent: this control parent control
        :return: this control
        """
        w_box = 190
        h_box = 90

        pil_image = Image.open(THEME_IMAGE)
        w, h = pil_image.size
        pil_image_resized = resize(w, h, w_box, h_box, pil_image)

        label = Label(parent, text="Logo", anchor="center")
        label.tk_image = ImageTk.PhotoImage(pil_image_resized)
        label.config(image=label.tk_image)
        label.place(x=5, y=5, width=w_box, height=h_box)
        return label

    def __tk_input_search(self, parent):
        """Design search input attribute

        :param parent: this control parent control
        :return: this control
        """
        input_string = StringVar()
        ipt = Entry(parent, textvariable=input_string)
        ipt.input_string = input_string
        ipt.place(x=5, y=100, width=150, height=30)
        return ipt

    def __tk_button_search(self, parent):
        """Design search button attribute

        :param parent: this control parent control
        :return: this control
        """
        btn = Button(parent, text="Search", takefocus=False, )
        btn.place(x=155, y=100, width=45, height=30)
        return btn

    def __tk_label_frame_filter(self, parent):
        """Design frame filter label attribute

        :param parent: this control parent control
        :return: this control
        """
        lfe = LabelFrame(parent, text="Filter*", width=190, height=355)
        lfe.place(x=5, y=135, width=190, height=355)
        return lfe

    def __tk_label_frame_userinfo(self, parent):
        """Design frame userinfo label attribute

        :param parent: this control parent control
        :return: this control
        """
        lfe = LabelFrame(parent, text="User info", width=190, height=100)
        lfe.place(x=5, y=515, width=190, height=100)
        return lfe

    def __tk_label_user(self, parent):
        """Design user label attribute

        :param parent: this control parent control
        :return: this control
        """
        label = Label(parent, text=f"N/A", width=260, height=30)
        label.place(x=5, y=5, width=175, height=30)
        return label

    def __tk_button_logout(self, parent):
        """Design logout button attribute

        :param parent: this control parent control
        :return: this control
        """
        btn = Button(parent, text="logout", takefocus=False, )
        btn.place(x=60, y=40, width=60, height=30)
        return btn

    def __tk_label_genre_filter(self, parent):
        """Design genre label attribute

        :param parent: this control parent control
        :return: this control
        """
        label = Label(parent, text="Genre:", anchor="w", )
        label.place(x=5, y=5, width=100, height=30)
        return label

    def __tk_select_box_genre_filter(self, parent):
        """Design genre select box attribute

        :param parent: this control parent control
        :return: this control
        """
        cb = ttk.Combobox(parent, state="readonly", )
        genre_list = [""]
        genre_list.extend(GENRE_LIST)

        cb['values'] = genre_list
        cb.place(x=5, y=40, width=175, height=30)
        return cb

    def __tk_label_age_group_filter(self, parent):
        """Design age group filter label attribute

        :param parent: this control parent control
        :return: this control
        """
        label = Label(parent, text="Age Group", anchor="w", )
        label.place(x=5, y=80, width=100, height=30)
        return label

    def __tk_select_box_age_group_filter(self, parent):
        """Design age group filter label attribute

        :param parent: this control parent control
        :return: this control
        """
        cb = ttk.Combobox(parent, state="readonly", )
        age_group_list = [""]
        age_group_list.extend(AGE_GROUP_LIST)
        cb['values'] = age_group_list
        cb.place(x=5, y=115, width=175, height=30)
        return cb

    def __tk_label_studio_filter(self, parent):
        """Design studio group filter label attribute

        :param parent: this control parent control
        :return: this control
        """
        label = Label(parent, text="Studio", anchor="w", )
        label.place(x=5, y=155, width=100, height=30)
        return label

    def __tk_select_box_studio_filter(self, parent):
        """Design sutdio select box filter label attribute

        :param parent: this control parent control
        :return: this control
        """
        cb = ttk.Combobox(parent, state="readonly", )
        studio_list = [""]
        studio_list.extend(STUDIO_LIST)

        cb['values'] = studio_list
        cb.place(x=5, y=190, width=175, height=30)
        return cb

    def __tk_label_season_filter(self, parent):
        """Design season filter label attribute

        :param parent: this control parent control
        :return: this control
        """
        label = Label(parent, text="Season", anchor="w", )
        label.place(x=5, y=155, width=100, height=30)
        return label

    def __tk_select_box_season_filter(self, parent):
        """Design season filter select box attribute

        :param parent: this control parent control
        :return: this control
        """
        cb = ttk.Combobox(parent, state="readonly", )
        season_list = [""]
        season_list.extend(SEASON_LIST)

        cb['values'] = season_list
        cb.place(x=5, y=190, width=175, height=30)
        return cb

    def __tk_button_clear_search(self, parent):
        """Design search button  attribute

        :param parent: this control parent control
        :return: this control
        """
        btn = Button(parent, text="Clear filter", takefocus=False, )
        btn.place(x=50, y=270, width=90, height=30)
        return btn

    def __tk_canvas_list(self, parent):
        """Design canvas list attribute

        :param parent: this control parent control
        :return: this control
        """
        canvas = Canvas(parent, width=880, height=540)
        canvas.place(x=10, y=10, width=880, height=540)
        myscrollbar = Scrollbar(parent, orient="vertical",
                                command=canvas.yview)
        canvas.configure(yscrollcommand=myscrollbar.set)
        myscrollbar.pack(side="right", fill="y")
        return canvas

    def __tk_frame_list(self, parent):
        """Design frame list attribute

        :param parent: this control parent control
        :return: this control
        """
        height = 255 * self.limit
        frame = Frame(parent, width=880, height=height)
        frame.place(x=0, y=0, width=880, height=height)
        return frame

    def _tk_frame_item(self, parent):
        """Design frame item attribute

        :param parent: this control parent control
        :return: this control
        """
        frame = Frame(parent, width=850, height=250, bg='black')
        frame.pack()
        return frame

    def _tk_button_favorite(self, parent, row, user: User):
        """Design favorite button attribute

        :param parent: this control parent control
        :param row: a row about animation data
        :param user: User login get this object
        :return: this control
        """
        if user.is_favorites(row):
            favorite_image = FAVORITE_FILL_IMAGE
        else:
            favorite_image = FAVORITE_IMAGE

        w_box = 30
        h_box = 30
        pil_image = Image.open(favorite_image)
        w, h = pil_image.size

        pil_image_resized = resize(w, h, w_box, h_box, pil_image)

        btn = Button(parent, text="favorite", takefocus=False, width=25, height=30)
        btn.favout_image = ImageTk.PhotoImage(pil_image_resized)
        btn.config(image=btn.favout_image)
        btn.place(x=815, y=5, width=30, height=30)
        btn.row = row
        return btn

    async def keep_update(self):
        """Keep update gui

        :return: None
        """
        while True:
            await asyncio.sleep(0)
            self.update()

    async def load_images(self, df2):
        """async load gui images

        :param df2: a dataframe about display data
        :return: None
        """
        asyncio.create_task(self.keep_update())
        self.image_list = []
        index = 1
        async with aiohttp.ClientSession() as session:
            for i, row in df2.iterrows():
                flag = index
                w_box = 160
                h_box = 200

                temp_image_file = pathlib.Path("./temp") / f'{row["uid"]}.jpg'
                if temp_image_file.exists():
                    pil_image = Image.open(temp_image_file)
                    w, h = pil_image.size

                    pil_image_resized = resize(w, h, w_box, h_box, pil_image)
                    tk_image = ImageTk.PhotoImage(pil_image_resized)
                    self.image_list.append(tk_image)
                    self.widget_dic[f"tk_label_img_{flag}"] = self._tk_label_img(
                        self.widget_dic[f"tk_frame_item_{flag}"], tk_image, w_box, h_box)
                else:
                    async with session.get(row['img_url']) as response:
                        image_bytes = await response.read()
                        data_stream = io.BytesIO(image_bytes)

                        try:
                            pil_image = Image.open(data_stream)
                            pil_image.save(temp_image_file)

                            w, h = pil_image.size

                            pil_image_resized = resize(w, h, w_box, h_box, pil_image)
                            tk_image = ImageTk.PhotoImage(pil_image_resized)
                            self.image_list.append(tk_image)
                            self.widget_dic[f"tk_label_img_{flag}"] = self._tk_label_img(
                                self.widget_dic[f"tk_frame_item_{flag}"], tk_image, w_box, h_box)
                        except:
                            pass

                index += 1

    async def load_user_images(self, df2):
        """async load user gui images

        :param df2: a dataframe about display data
        :return: None
        """
        try:
            asyncio.create_task(self.keep_update())
            self.image_user_list = []
            index = 1
            async with aiohttp.ClientSession() as session:
                for i, row in df2.iterrows():
                    flag = index
                    w_box = 160
                    h_box = 200
                    temp_image_file = pathlib.Path("./temp") / f'{row["uid"]}.jpg'
                    if temp_image_file.exists():
                        pil_image = Image.open(temp_image_file)
                        w, h = pil_image.size
                        pil_image_resized = resize(w, h, w_box, h_box, pil_image)
                        tk_image = ImageTk.PhotoImage(pil_image_resized)
                        self.image_user_list.append(tk_image)
                        self.widget_dic[f"tk_label_img_user_{flag}"] = self._tk_label_img(
                            self.widget_dic[f"tk_frame_item_user_{flag}"], tk_image, w_box, h_box)
                    else:
                        async with session.get(row['img_url']) as response:
                            image_bytes = await response.read()
                            data_stream = io.BytesIO(image_bytes)

                            try:
                                pil_image = Image.open(data_stream)
                                w, h = pil_image.size

                                pil_image_resized = resize(w, h, w_box, h_box, pil_image)
                                tk_image = ImageTk.PhotoImage(pil_image_resized)
                                self.image_user_list.append(tk_image)
                                self.widget_dic[f"tk_label_img_user_{flag}"] = self._tk_label_img(
                                    self.widget_dic[f"tk_frame_item_user_{flag}"], tk_image, w_box, h_box)
                            except:
                                pass
                    index += 1
        except:
            pass


    def _tk_label_title(self, parent, title):
        """Design title label

        :param parent: this control parent control
        :param title: display content
        :return: this control
        """
        text = Text(parent, width=805, height=30, font=("", 18))
        text.insert(INSERT, title)
        text.place(x=5, y=5, width=805, height=30)
        text.config(state=DISABLED)
        return text

    def _tk_label_img(self, parent, tk_image, w_box, h_box):
        """Design image label

        :param parent: this control parent control
        :param tk_image: will display tkinger image object
        :param w_box: show box widht
        :param h_box: show box height
        :return: this control
        """

        label = Label(parent, text="img", anchor="center", image=tk_image)
        label.place(x=5, y=40, width=w_box, height=h_box)
        return label

    def invalid_convert(self, input):
        """Convet input content to a special value

        :param input:
        :return:
        """
        if pd.isna(input) or pd.isnull(input):
            return "N/A"
        else:
            return input

    def _tk_label_genre(self, parent, genre):
        """Design genre label

        :param parent: this control parent control
        :param genre: will display value
        :return: this control
        """
        genre = self.invalid_convert(genre)
        text = Text(parent, width=400, height=40)
        text.insert(INSERT, f"Genre：{str(genre)}")
        text.place(x=170, y=40, width=400, height=40)
        text.config(state=DISABLED)
        return text

    def _tk_label_aired(self, parent, aired):
        """Design aired label

        :param parent: this control parent control
        :param aired: will display value
        :return: this control
        """
        aired = self.invalid_convert(aired)
        text = Text(parent, width=400, height=30)
        text.insert(INSERT, f"Aired: {aired}")
        text.place(x=170, y=82, width=400, height=30)
        text.config(state=DISABLED)
        return text

    def _tk_label_episodes(self, parent, episodes):
        """Design episodes label

        :param parent: this control parent control
        :param episodes: will display value
        :return: this control
        """
        episodes = self.invalid_convert(episodes)
        text = Text(parent, width=400, height=30)
        text.insert(INSERT, f"Episodes: {episodes}")
        text.place(x=170, y=114, width=400, height=30)
        text.config(state=DISABLED)
        return text

    def _tk_label_link(self, parent, link):
        """Design link label

        :param parent: this control parent control
        :param link: will display value
        :return: this control
        """
        link = self.invalid_convert(link)
        text = Text(parent, width=400, height=40)
        text.insert(INSERT, f"Link：{link}")
        text.place(x=170, y=146, width=400, height=40)
        text.config(state=DISABLED)
        return text

    def _tk_label_score(self, parent, score):
        """Design score label

        :param parent: this control parent control
        :param score: will display value
        :return: this control
        """
        score = self.invalid_convert(score)
        text = Text(parent, font=("", 20), width=400, height=52)
        text.insert(INSERT, f"Score: {score}")
        text.place(x=170, y=188, width=400, height=52)
        text.config(state=DISABLED)
        return text

    def _tk_label_synopsis(self, parent, synopsis):
        """Design synopsis label

        :param parent: this control parent control
        :param synopsis: will display value
        :return: this control
        """
        scr = scrolledtext.ScrolledText(parent, width=270, height=200, )
        scr.place(x=575, y=40, width=270, height=200)
        synopsis = self.invalid_convert(synopsis)
        synopsis = str(synopsis).replace("_x000D_", "\r")
        scr.insert('end', synopsis, "center")
        scr.config(state=DISABLED)
        return scr

    def __tk_button_home_page(self, parent):
        """Design home button

        :param parent: this control parent control
        :return: this control
        """
        btn = Button(parent, text="Home", takefocus=False, )
        btn.place(x=235, y=555, width=50, height=30)
        return btn

    def __tk_button_prev_page(self, parent):
        """Design prev button

        :param parent: this control parent control
        :return: this control
        """
        btn = Button(parent, text="Prev", takefocus=False, )
        btn.place(x=295, y=555, width=50, height=30)
        return btn

    def __tk_button_next_page(self, parent):
        """Design next button

        :param parent: this control parent control
        :return: this control
        """
        btn = Button(parent, text="Next", takefocus=False, )
        btn.place(x=355, y=555, width=50, height=30)
        return btn

    def __tk_button_trail_page(self, parent):
        """Design trail button

        :param parent: this control parent control
        :return: this control
        """
        btn = Button(parent, text="Trail", takefocus=False, )
        btn.place(x=415, y=555, width=50, height=30)
        return btn

    def __tk_label_page_info(self, parent):
        """Design page label

        :param parent: this control parent control
        :return: this control
        """
        label = Label(parent, text="", anchor="center", )
        label.place(x=500, y=555, width=400, height=30)
        return label


class HomeWin(HomeWinGUI):
    """Home page Controller, Process event or data display

    """
    def __init__(self, user: User):
        """Init Class

        :param user: user object
        """
        super().__init__()
        self.__event_bind()

        self.user = user

        self.widget_dic["tk_label_user"]['text'] = f"{self.user.username}"

        self.anime_list = []
        self.anime_user_list = []

        anime_data = pd.read_excel(ANIMES_FILE)
        self.df_anime = pd.DataFrame(anime_data,
                                     columns=['title', 'synopsis', 'genre', 'episodes', 'img_url', 'uid', 'link',
                                              'aired', 'score'])

        self.df_anime_user = pd.DataFrame(user.get_user_favorites(),
                                          columns=['title', 'synopsis', 'genre', 'episodes', 'img_url', 'uid', 'link',
                                                   'aired', 'score'])

        self.update_cur_df_anime(self.df_anime)
        self.make_list(self.min_page)

        self.update_cur_df_anime_user(self.df_anime_user)
        self.make_list_user(self.min_page_user)

    def update_cur_df_anime(self, df):
        """Update current anime dataframe

        :param df:  anime dataframe
        :return: None
        """
        self.cur_df_anime = df
        self.min_page = 1
        self.max_page = math.ceil(self.cur_df_anime.shape[0] / self.limit)
        self.cur_page = 1

    def update_cur_df_anime_user(self, df):
        """Update current user anime dataframe

        :param df:  anime dataframe
        :return: None
        """
        self.cur_df_anime_user = df
        self.min_page_user = 1
        self.max_page_user = math.ceil(self.cur_df_anime_user.shape[0] / self.limit)
        self.cur_page_user = 1

    def get_df_by_page(self, df, page):
        """Get Dataframe data by page

        :param df: anime dataframe
        :param page: page count
        :return: anime dataframe of Assigned page
        """
        df2 = df[(int(page) - 1) * int(self.limit): (int(page) * int(self.limit))]
        return df2

    def favorite_user_click(self, event):
        """Click favourite control event, record user favorite or not

        :param event: event object
        :return: None
        """
        if self.user.is_favorites(event.widget.row):
            favorite_image = FAVORITE_IMAGE
            self.user.remove_favorites(event.widget.row)
        else:
            favorite_image = FAVORITE_FILL_IMAGE
            self.user.add_favorites(event.widget.row)

        w_box = 30
        h_box = 30
        pil_image = Image.open(favorite_image)
        w, h = pil_image.size

        pil_image_resized = resize(w, h, w_box, h_box, pil_image)

        event.widget.favout_image = ImageTk.PhotoImage(pil_image_resized)
        event.widget.config(image=event.widget.favout_image)

        self.df_anime_user = pd.DataFrame(self.user.get_user_favorites(),
                                          columns=ANIMES_COLUMNS)
        self.update_cur_df_anime_user(self.df_anime_user)
        self.make_list_user(self.min_page_user)
        self.make_list(self.cur_page)

    def favorite_click(self, event):
        """Click favourite control event, record user favorite or not

        :param event: event object
        :return: None
        """
        if self.user.is_favorites(event.widget.row):
            favorite_image = FAVORITE_IMAGE
            self.user.remove_favorites(event.widget.row)
        else:
            favorite_image = FAVORITE_FILL_IMAGE
            self.user.add_favorites(event.widget.row)

        w_box = 30
        h_box = 30
        pil_image = Image.open(favorite_image)
        w, h = pil_image.size

        pil_image_resized = resize(w, h, w_box, h_box, pil_image)

        event.widget.favout_image = ImageTk.PhotoImage(pil_image_resized)
        event.widget.config(image=event.widget.favout_image)

        self.df_anime_user = pd.DataFrame(self.user.get_user_favorites(),
                                          columns=ANIMES_COLUMNS)
        self.update_cur_df_anime_user(self.df_anime_user)
        self.make_list_user(self.min_page_user)

    def make_list(self, page):
        """Create diplay animation list

        :param page: page count
        :return: None
        """
        df2 = self.get_df_by_page(self.cur_df_anime, page)

        for item in self.anime_list:
            item.destroy()
        self.anime_list.clear()

        index = 1
        for i, row in df2.iterrows():
            flag = index

            self.widget_dic[f"tk_frame_item_{flag}"] = self._tk_frame_item(self.widget_dic["tk_frame_list"])

            self.widget_dic[f"tk_button_favorite_{flag}"] = self._tk_button_favorite(
                self.widget_dic[f"tk_frame_item_{flag}"], row, self.user)
            self.widget_dic[f"tk_button_favorite_{flag}"].bind('<Button>', self.favorite_click)

            # self.widget_dic[f"tk_label_img_{flag}"] = self._tk_label_img(self.widget_dic[f"tk_frame_item_{flag}"], row['img_url'])
            self.widget_dic[f"tk_label_title_{flag}"] = self._tk_label_title(self.widget_dic[f"tk_frame_item_{flag}"],
                                                                             row['title'])
            self.widget_dic[f"tk_label_genre_{flag}"] = self._tk_label_genre(self.widget_dic[f"tk_frame_item_{flag}"],
                                                                             row['genre'])
            self.widget_dic[f"tk_label_episodes_{flag}"] = self._tk_label_episodes(
                self.widget_dic[f"tk_frame_item_{flag}"],
                row['episodes'])
            self.widget_dic[f"tk_label_link_{flag}"] = self._tk_label_link(self.widget_dic[f"tk_frame_item_{flag}"],
                                                                           row['link'])
            self.widget_dic[f"tk_label_aired_{flag}"] = self._tk_label_aired(self.widget_dic[f"tk_frame_item_{flag}"],
                                                                             row['aired'])

            self.widget_dic[f"tk_label_score_{flag}"] = self._tk_label_score(self.widget_dic[f"tk_frame_item_{flag}"],
                                                                             row['score'])
            self.widget_dic[f"tk_label_synopsis_{flag}"] = self._tk_label_synopsis(
                self.widget_dic[f"tk_frame_item_{flag}"], row['synopsis'])

            self.widget_dic[f"tk_frame_item_{flag}"].update_idletasks()

            index += 1
            self.anime_list.append(self.widget_dic[f"tk_frame_item_{flag}"])

        self.widget_dic["tk_label_page_info"][
            "text"] = f"Current {self.cur_page} page, {self.limit} Per page, Total {self.max_page} pages"

        # update images
        # asyncio.run(self.load_images(df2))
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.load_images(df2))

        if len(df2) == 0:
            search_string = self.widget_dic["tk_input_search"].get()
            if search_string == "":
                messagebox.showinfo("search", "search count is 0, please change other filters.")
            else:
                askback = messagebox.askyesno('search', 'Search count is 0, Would you like to see a recommendation?')
                if not askback:
                    return
                else:
                    self.update_animes_list(self.df_anime, is_fuzz=True)

    def make_list_user(self, page):
        """Create user diplay animation list

        :param page: page count
        :return: None
        """
        df2 = self.get_df_by_page(self.cur_df_anime_user, page)

        for item in self.anime_user_list:
            item.destroy()
        self.anime_user_list.clear()

        index = 1
        for i, row in df2.iterrows():
            flag = index

            self.widget_dic[f"tk_frame_item_user_{flag}"] = self._tk_frame_item(
                self.widget_dic["tk_frame_list_favorite"])

            self.widget_dic[f"tk_button_favorite_user_{flag}"] = self._tk_button_favorite(
                self.widget_dic[f"tk_frame_item_user_{flag}"], row, self.user)
            self.widget_dic[f"tk_button_favorite_user_{flag}"].bind('<Button>', self.favorite_user_click)

            # self.widget_dic[f"tk_label_img_{flag}"] = self._tk_label_img(self.widget_dic[f"tk_frame_item_{flag}"], row['img_url'])
            self.widget_dic[f"tk_label_title_user_{flag}"] = self._tk_label_title(
                self.widget_dic[f"tk_frame_item_user_{flag}"], row['title'])
            self.widget_dic[f"tk_label_genre_user_{flag}"] = self._tk_label_genre(
                self.widget_dic[f"tk_frame_item_user_{flag}"], row['genre'])
            self.widget_dic[f"tk_label_episodes_user_{flag}"] = self._tk_label_episodes(
                self.widget_dic[f"tk_frame_item_user_{flag}"],
                row['episodes'])
            self.widget_dic[f"tk_label_link_user_{flag}"] = self._tk_label_link(
                self.widget_dic[f"tk_frame_item_user_{flag}"], row['link'])
            self.widget_dic[f"tk_label_aired_user_{flag}"] = self._tk_label_aired(
                self.widget_dic[f"tk_frame_item_user_{flag}"], row['aired'])

            self.widget_dic[f"tk_label_score_user_{flag}"] = self._tk_label_score(
                self.widget_dic[f"tk_frame_item_user_{flag}"], row['score'])
            self.widget_dic[f"tk_label_synopsis_user_{flag}"] = self._tk_label_synopsis(
                self.widget_dic[f"tk_frame_item_user_{flag}"], row['synopsis'])

            self.widget_dic[f"tk_frame_item_user_{flag}"].update_idletasks()

            index += 1
            self.anime_user_list.append(self.widget_dic[f"tk_frame_item_user_{flag}"])

        self.widget_dic["tk_label_page_info_favorite"][
            "text"] = f"Current  {self.cur_page_user} page, {self.limit} Per page, Total {self.max_page_user} pages"

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.load_user_images(df2))

    def home_page_click(self, evt):
        """Click home page button, to load home page animation data

        :param evt: evt object
        :return: None
        """
        if self.cur_page > 1:
            self.cur_page = self.min_page
            self.make_list(self.min_page)

    def prev_page_click(self, evt):
        """Click prev page button, to load prev page animation data

        :param evt: evt object
        :return: None
        """
        if self.cur_page > 1:
            self.cur_page -= 1
            self.make_list(self.cur_page)

    def next_page_click(self, evt):
        """Click next page button, to load next page animation data

        :param evt: evt object
        :return: None
        """
        if self.cur_page < self.max_page:
            self.cur_page += 1
            self.make_list(self.cur_page)

    def trail_page_click(self, evt):
        """Click trail page button, to load trail page animation data

        :param evt: evt object
        :return: None
        """
        if self.cur_page < self.max_page:
            self.cur_page = self.max_page
            self.make_list(self.max_page)

    def home_page_favorite_click(self, evt):
        """Click favorite home page button, to load home page animation data

        :param evt: evt object
        :return: None
        """
        if self.cur_page_user > 1:
            self.cur_page_user = self.min_page_user
            self.make_list_user(self.cur_page_user)

    def prev_page_favorite_click(self, evt):
        """Click favorite prev page button, to load prev page animation data

        :param evt: evt object
        :return: None
        """
        if self.cur_page_user > 1:
            self.cur_page_user -= 1
            self.make_list_user(self.cur_page_user)

    def next_page_favorite_click(self, evt):
        """Click favorite next page button, to load next page animation data

        :param evt: evt object
        :return: None
        """
        if self.cur_page_user < self.max_page_user:
            self.cur_page_user += 1
            self.make_list_user(self.cur_page_user)

    def trail_page_favorite_click(self, evt):
        """Click favorite trail page button, to load trail page animation data

        :param evt: evt object
        :return: None
        """
        if self.cur_page_user < self.max_page_user:
            self.cur_page_user = self.max_page_user
            self.make_list_user(self.cur_page_user)

    def logout_click(self, evt):
        """Click logout, to logout

        :param evt: evt object
        :return: None
        """
        askback = messagebox.askyesno('logout', 'Are you sure logout?')
        if not askback:
            return
        else:
            self.destroy()
            from login import Registration
            Registration()

    def search_click(self, evt):
        """Click search, to search filter content

        :param evt: evt object
        :return: None
        """
        self.update_animes_list(self.df_anime)

    def clear_search_click(self, evt):
        """Click clearn, to clear all filter

        :param evt: evt object
        :return: None
        """
        self.widget_dic["tk_select_box_genre_filter"].set('')
        self.widget_dic["tk_select_box_age_group_filter"].set('')
        # self.widget_dic["tk_select_box_studio_filter"].set('')
        self.widget_dic["tk_select_box_season_filter"].set('')
        self.widget_dic["tk_input_search"].input_string.set('')
        self.update_animes_list(self.df_anime)

    def update_animes_list(self, df_animes, is_fuzz=False):
        """Update display animation list

        :param df_animes: animes dataframe data
        :param is_fuzz: is user fuzzy seach
        :return: None
        """

        genre_filter_string = self.widget_dic["tk_select_box_genre_filter"].get()
        age_group_filter_string = self.widget_dic["tk_select_box_age_group_filter"].get()
        studio_filter_string = ""
        # studio_filter_string = self.widget_dic["tk_select_box_studio_filter"].get()
        season_filter_string = self.widget_dic["tk_select_box_season_filter"].get()
        search_string = self.widget_dic["tk_input_search"].get()

        search_df = self.filter_animes(df_animes, genre_filter_string, age_group_filter_string,
                                       studio_filter_string, season_filter_string, search_string, is_fuzz)
        self.update_cur_df_anime(search_df)
        self.make_list(self.min_page)

    def filter_animes(self, df_animes, genre_filter_string, age_group_filter_string, studio_filter_string,
                      season_filter_string, search_string, is_fuzz=False):
        """Filter animes by some condition

        :param df_animes: will filter anime dataframe
        :param genre_filter_string: genre filter condition
        :param age_group_filter_string: age filter condition
        :param studio_filter_string: studio filter condition
        :param season_filter_string: season filter condition
        :param search_string: search condition
        :param is_fuzz: is user fuzzy seach
        :return: a filter anime dataframe
        """
        filter_content = None
        if genre_filter_string != "":
            filter_content = df_animes["genre"].astype(str).str.contains(genre_filter_string, case=False)

        if age_group_filter_string != "":
            if filter_content is None:
                filter_content = df_animes["genre"].astype(str).str.contains(age_group_filter_string, case=False)
            else:
                filter_content = filter_content & df_animes["genre"].astype(str).str.contains(age_group_filter_string, case=False)
        #
        # if studio_filter_string != "":
        #     if filter_content is None:
        #         filter_content = df_animes["genre"].astype(str).str.contains(studio_filter_string,
        #                                                                             case=False)
        #     else:
        #         filter_content = filter_content & df_animes["genre"].astype(str).str.contains(
        #             studio_filter_string,
        #             case=False)
        #

        def season_filter(input_string:str):
            season, year = season_filter_string.split(' ')
            if 'Winter' == season:
                begin_fiter = datetime(int(year), 12, 1)
                end_filter = datetime(int(year)+1, 2, get_month_days(int(year)+1, 2))
            elif 'Summer' == season:
                begin_fiter = datetime(int(year), 6, 1)
                end_filter = datetime(int(year), 8, get_month_days(int(year), 8))
            elif 'Fall' == season:
                begin_fiter = datetime(int(year), 9, 1)
                end_filter = datetime(int(year), 11, get_month_days(int(year), 11))
            else:
                begin_fiter = datetime(int(year), 3, 1)
                end_filter = datetime(int(year), 5, get_month_days(int(year), 5))

            try:
                if "to" in input_string.lower():
                    begin = input_string.lower().split('to')[0]
                    end = input_string.lower().split('to')[1]

                    begin_input = parse_datetime(begin)
                    end_input = parse_datetime(end)

                    if begin_input > end_filter or end_input < begin_fiter:
                        return False
                    else:
                        return True
                else:
                    date_input = parse_datetime(input_string)
                    if date_input > begin_fiter and date_input < end_filter:
                        return True
                    else:
                        return False
            except:
                return False

        if season_filter_string != "":
            if filter_content is None:
                filter_content = df_animes["aired"].map(season_filter)
            else:
                filter_content = filter_content & df_animes["aired"].map(season_filter)

        if filter_content is None:
            df_animes_filter = df_animes
        else:
            df_animes_filter = df_animes[filter_content]


        search_ratio = 50

        def fuzzy_match(x):
            ratio = fuzz.partial_ratio(str(x), search_string)
            if ratio < search_ratio:
                return False
            else:
                return True

        search_content = None
        if search_string != "":
            if is_fuzz:
                search_content = df_animes["title"].map(fuzzy_match) | \
                                 df_animes["genre"].map(fuzzy_match) | \
                                 df_animes["episodes"].map(fuzzy_match)
            else:
                search_content = df_animes["title"].astype(str).str.contains(search_string, case=False) | \
                                 df_animes["genre"].astype(str).str.contains(search_string, case=False) | \
                                 df_animes["episodes"].astype(str).str.contains(search_string, case=False)

        if search_content is None:
            df = df_animes_filter
        else:
            df = df_animes_filter[search_content]
        return df

    def genre_filter_selected(self, event):
        """Select filter to update display list

        :param event: event object
        :return: None
        """
        self.update_animes_list(self.df_anime)

    def age_group_filter_selected(self, event):
        """Select filter to update display list

        :param event: event object
        :return: None
        """
        self.update_animes_list(self.df_anime)

    def studio_filter_selected(self, event):
        """Select filter to update display list

        :param event: event object
        :return: None
        """
        self.update_animes_list(self.df_anime)

    def season_filter_selected(self, event):
        """Select filter to update display list

        :param event: event object
        :return: None
        """
        self.update_animes_list(self.df_anime)

    def on_mousewheel(self, event):
        """Causes the scroll bar to respond to mouse scroll events

        :param event: event object
        :return: None
        """
        self.widget_dic["tk_canvas_list"].yview("scroll", int(-1 * (event.delta / 120)), "units")
        return "break"

    def on_mousewheel_user(self, event):
        """Causes the scroll bar to respond to mouse scroll events

        :param event: event object
        :return: None
        """
        self.widget_dic["tk_canvas_list_favorite"].yview("scroll", int(-1 * (event.delta / 120)), "units")
        return "break"

    def tab_changed(self, event):
        """Tab change then bind mouse scroll events

        :param event: event object
        :return: None
        """
        t_nos = str(self.widget_dic["tk_tab_right"].index(self.widget_dic["tk_tab_right"].select()))
        if t_nos == '0':
            self.widget_dic["tk_canvas_list"].bind_all('<MouseWheel>', self.on_mousewheel)
        elif t_nos == '1':
            self.widget_dic["tk_canvas_list_favorite"].bind_all('<MouseWheel>', self.on_mousewheel_user)

    def __event_bind(self):
        """All control band need put it here

        :return: None
        """
        self.widget_dic["tk_select_box_genre_filter"].bind('<<ComboboxSelected>>', self.genre_filter_selected)
        self.widget_dic["tk_select_box_age_group_filter"].bind('<<ComboboxSelected>>', self.age_group_filter_selected)
        # self.widget_dic["tk_select_box_studio_filter"].bind('<<ComboboxSelected>>', self.studio_filter_selected)
        self.widget_dic["tk_select_box_season_filter"].bind('<<ComboboxSelected>>', self.season_filter_selected)

        self.widget_dic["tk_button_search"].bind('<Button>', self.search_click)
        self.widget_dic["tk_button_clear_search"].bind('<Button>', self.clear_search_click)

        self.widget_dic["tk_button_logout"].bind('<Button>', self.logout_click)

        self.widget_dic["tk_button_home_page"].bind('<Button>', self.home_page_click)
        self.widget_dic["tk_button_prev_page"].bind('<Button>', self.prev_page_click)
        self.widget_dic["tk_button_next_page"].bind('<Button>', self.next_page_click)
        self.widget_dic["tk_button_trail_page"].bind('<Button>', self.trail_page_click)

        self.widget_dic["tk_button_home_page_favorite"].bind('<Button>', self.home_page_favorite_click)
        self.widget_dic["tk_button_prev_page_favorite"].bind('<Button>', self.prev_page_favorite_click)
        self.widget_dic["tk_button_next_page_favorite"].bind('<Button>', self.next_page_favorite_click)
        self.widget_dic["tk_button_trail_page_favorite"].bind('<Button>', self.trail_page_favorite_click)

        self.widget_dic["tk_canvas_list"].bind_all('<MouseWheel>', self.on_mousewheel)
        # self.widget_dic["tk_canvas_list_favorite"].bind('<MouseWheel>', self.on_mousewheel_user)

        self.widget_dic["tk_tab_right"].bind('<<NotebookTabChanged>>', self.tab_changed)

        pass


if __name__ == "__main__":
    pass
    # user = User("test@qq.com", "123123")
    # win = HomeWin(user)
    # win.mainloop()
