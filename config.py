# -*- coding: utf-8 -*-
import pathlib

# The basic path for the program to run
BASE_PATH = pathlib.Path(__file__).parent

# system picture
THEME_IMAGE = str(BASE_PATH / r'res/AnisaLogo.png')
FAVORITE_FILL_IMAGE = str(BASE_PATH / r'res/favorites-fill.png')
FAVORITE_IMAGE = str(BASE_PATH / r'res/favorites.png')

# anime list
GENRE_LIST = [
    'Action',
    'Adventure',
    'Avant Garde',
    'Award Winning',
    'Comedy',
    'Drama',
    'Fantasy',
    'Gourmet',
    'Horror',
    'Mystery',
    'Romance',
    'Sci-fi',
    'Slice of Life',
    'Sports',
    'Supernatural',
    'Suspense',
    'Childcare',
    'Combat Sports',
    'Detective',
    'Educational',
    'Gag humor',
    'Isekai',
    'Martial Arts',
    'Mecha',
    'Medical',
    'Military',
    'Music',
    'Mythology',
    'Otaku Culture',
    'Parody',
    'Performing Arts',
    'Pets',
    'Psychological',
    'Racing',
    'Reincarnation',
    'Samurai',
    'School',
    'Space',
    'Strategy Game',
    'Super Power',
    'Survival',
    'Team Sports',
    'Time Travel',
    'Vampire',
    'Video Game',
    'Visual Arts',
    'Workplace']

# age group list
AGE_GROUP_LIST = ['Josei', 'Kids', 'Seinen', 'Shoujo', 'Shounen']

# studio list
STUDIO_LIST = [
    'Sentai Filmworks',
    'Aniplex',
    'Discotek Media',
    'TMS Entertain',
    'Madhouse',
    'Studio Deen',
    'Pierrot',
    'OLM',
    'AIC',
    'TBS',
    'A-1 Pictures',
    'Shin-Ei Animation',
    'Bandai Entertainment',
    'Bandai Entertainment',
    'DLE',
    'bilibili',
    'Tatsunoko Production',
    'Tencent Penguin',
    'Xebec',
    'Shogakukan-Shueisha Productions',
    'Nihon Ad System',
    'Nippon Television Network',
    'Shaft',
    'Gonzo',
    'Group TAC',
    'Showgate',
    'Warner Bros. Japan',
    'SILVER LINK.',
    'Satelight',
    'LIDENFILMS',
    'Doga Kobo',
    'Seven',
    'Ashi Productions',
    'Studio Mausu',
    'Geidai Animation',
    'Wit Studio',
    'Gallop',
    'Gainax',
    'BS Fuji',
    'MAPPA',
    'Mushi Production',
    'Studio 4Â°C',
    'Hololive Production',
    'Zexcs',
    'AQUA ARIS',
    'ufotable',
    'feel.',
    'Studio Hibari',
    'Studio Comet',
    'Haoliners Animation League']

# season list
SEASON_LIST = [
    'Winter 2024',
    'Fall 2023',
    'Summer 2023',
    'Spring 2023',
    'Winter 2023',
    'Fall 2022',
    'Summer 2022',
    'Spring 2022',
    'Winter 2022',
    'Fall 2021',
    'Summer 2021',
    'Spring 2021',
    'Winter 2021',
    'Fall 2020',
    'Summer 2020',
    'Spring 2020',
    'Winter 2020',
    'Fall 2019',
    'Summer 2019',
    'Spring 2019',
    'Winter 2019',
    'Fall 2018',
    'Summer 2018',
    'Spring 2018']
# season month range
# Winter = [12,1,2]
# Summer = [6,7,8]
# Fall = [9,10,11]
# Spring = [3,4,5]

# animes file
ANIMES_FILE = str(BASE_PATH / r'archive\animes.xlsx')

# animes colums
ANIMES_COLUMNS = [
    'title',
    'synopsis',
    'genre',
    'episodes',
    'img_url',
    'uid',
    'link',
    'aired',
    'score']
