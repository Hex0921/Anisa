# -*- coding: utf-8 -*-
import pathlib
import shutil
import pandas as pd
from commons import read_json, write_json, mkdir
from config import ANIMES_COLUMNS


class User:
    """User relate content
    about user favorites and user home setting
    """

    def __init__(self, username, password):
        """Init User object

        :param username: user name
        :param password: user password
        """
        self.home = "./home"
        self.username = username
        self.password = password
        self.df_format = pd.DataFrame(columns=ANIMES_COLUMNS, dtype=str)

    def get_user_home(self):
        """Get user home directory

        :return: format path
        """
        user_home = pathlib.Path(self.home) / self.username
        return user_home

    def get_user_favorites_file(self):
        """Get user favorites file

        :return: format path
        """
        favorites = pathlib.Path(self.home) / self.username / "favorites.xlsx"
        return favorites

    def get_user_favorites(self):
        """Get user favorites dataframe

        :return: favorites dataframe
        """
        if not self.get_user_favorites_file().exists():
            return self.df_format
        else:
            df_favorites = pd.read_excel(self.get_user_favorites_file())
            return df_favorites

    def is_favorites(self, row):
        """Determines whether the user favorites the item

        :param row: a row record in animate dataframe
        :return: is favorites, True or False
        """
        if not self.get_user_favorites_file().exists():
            return False
        else:
            df = pd.read_excel(self.get_user_favorites_file())
            result = df["uid"].isin([row["uid"]]).any()
            return result

    def add_favorites(self, row):
        """Add record to user favorites

        :param row: a record in animation dataframe
        :return: None
        """
        if not self.get_user_favorites_file().exists():
            # df_favorites = self.df_format.append(row)

            df_favorites = pd.concat(
                [self.df_format, row.to_frame().T], axis=0)

            df_favorites = df_favorites.loc[:,
                                            ~df_favorites.columns.str.contains('Unnamed')]
            df_favorites.to_excel(self.get_user_favorites_file())
        else:
            df = pd.read_excel(self.get_user_favorites_file())
            # df_favorites = df.append(row)
            # df_favorites = df.append(row)
            df_favorites = pd.concat([df, row.to_frame().T], axis=0)

            df_favorites = df_favorites.loc[:,
                                            ~df_favorites.columns.str.contains('Unnamed')]
            df_favorites.to_excel(self.get_user_favorites_file())

    def remove_favorites(self, row):
        """Remove a animation item from user favorites

        :param row: a record in animation dataframe
        :return: None
        """
        if not self.get_user_favorites_file().exists():
            df_favorites = self.df_format
            # df_favorites = pd.DataFrame(row)
            df_favorites = df_favorites.loc[:,
                                            ~df_favorites.columns.str.contains('Unnamed')]
            df_favorites.to_excel(self.get_user_favorites_file())
        else:
            df_favorites = pd.read_excel(self.get_user_favorites_file())
            df_favorites.drop(
                df_favorites[df_favorites['uid'] == row["uid"]].index, inplace=True)

            df_favorites = df_favorites.loc[:,
                                            ~df_favorites.columns.str.contains('Unnamed')]
            df_favorites.to_excel(self.get_user_favorites_file())


class UserManager:
    """Manager user info, record user register, login or modify password etc.

    """

    def __init__(self):
        """Init UserManager and some setting

        """
        self.home = "./home"
        self.user_info_file = "./home/user_info.json"
        self.user_remember_file = "./home/user_remember.json"

    def get_user_info(self):
        """Get user info

        :return: a json fromat info
        """
        user_info = read_json(self.user_info_file)
        return user_info

    def get_user_remember(self):
        """Get remember user password data

        :return: a json fromat data
        """
        user_remember = read_json(self.user_remember_file)
        return user_remember

    def register(self, username, password):
        """Register user

        :param username: user name
        :param password: passwrod
        :return: if register success ,Otherwise throw a Exception
        """
        user_info = self.get_user_info()
        if username not in user_info.keys():
            user_info[username] = password
            write_json(self.user_info_file, user_info)
            self.make_user_home(username)
        else:
            raise Exception("User already exists")

    def login(self, username, password):
        """User login system

        :param username: user name
        :param password: password
        :return: if lgoin success return a User object, Otherwise throw a Exception
        """
        user_info = self.get_user_info()
        if username in user_info.keys() and user_info[username] == password:
            self.make_user_home(username)
            return User(username, password)
        else:
            raise Exception("Invalid email or password!")

    def modify_password(self, username, password):
        """Modify password

        :param username: user name
        :param password: user password
        :return:
        """
        user_info = self.get_user_info()
        if username in user_info.keys():
            user_info[username] = password
            write_json(self.user_info_file, user_info)
        else:
            raise Exception("User already exists")

    def add_user_remember(self, username, password):
        """Remember user password, so next login user can't input passowrd

        :param username: user name
        :param password: user password
        :return: None
        """
        user_remember = self.get_user_remember()
        # user_remember_order = OrderedDict(user_remember)
        user_remember[username] = password
        write_json(self.user_remember_file, user_remember)

    def delete_user_remember(self, username):
        """Delete remember user password, so next login user need input passowrd

        :param username: user name
        :return: None
        """
        user_remember = self.get_user_remember()
        if username in user_remember.keys():
            user_remember.pop(username, None)
            write_json(self.user_remember_file, user_remember)

    def delete(self, username):
        """Delete user and user info

        :param username: user name
        :return: if delete success return 'None', Otherwise throw a Exception
        """
        user_info = self.get_user_info()
        if username in user_info.keys():
            del user_info[username]
            write_json(self.user_info_file, user_info)
            self.delete_user_home(username)
        else:
            raise Exception("User does not exist")

        user_remember = self.get_user_remember()
        if username in user_remember.keys():
            del user_remember[username]
            write_json(self.user_remember_file, user_remember)

    def get_user_home(self, username):
        """Get login user home path

        :param username: user name
        :return: a user home path
        """
        user_home = pathlib.Path(self.home) / username
        return user_home

    def make_user_home(self, username):
        """Create user home directory

        :param username: user name
        :return: None
        """
        mkdir(self.get_user_home(username))

    def delete_user_home(self, username):
        """Delete user home directory

        :param username: user name
        :return: None
        """
        shutil.rmtree(self.get_user_home(username))


if __name__ == '__main__':
    pass