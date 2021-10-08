import winreg
import inquirer
import malclient
from os import scandir
from textwrap import fill
from bs4 import BeautifulSoup
from tabulate import tabulate
from urllib.parse import urlencode
from re import sub, compile, escape
from urllib3 import PoolManager, request


class ahframework:
    def __init__(self):
        self.client = malclient.Client()
        self.client.init(
            refresh_token="def502007b613dc7114efb6b2e0dc50593a060fbfedda409cea33a2eb409824edc6c95a1e1d5c6c7c0eeb40e7f5ec3f8b9fe1a249248b7a73b352efa1526ad20405b2611b1608ac1f1cd60d7e8445e0879fa35928a90b5b82129f8a6360e212e84cf7b9ef4aed3f4387e708b1e5c5f83dc43c9e43aa8e0dfd24d4e6c9a2559b929b73af4bed8499c2255f22b130ee491ccd0212b3f14505b5c25624dded5b72c71427540b0b08b8b2d696470ac83f4b48db6053b2a74cc757e53c37fa6b16d73049572c69c09012d9687208a9c1ff9f91d2f34e46d1e376ba97d34834db68a6e6aa1c4adf28f37d2e7f305c3b4b54010309119a32f6a55d56afb8b751210ecce2a667f45cd8750caf6d506167c220bf97eb35ffd3c2f9d9a4011819968892be95905e678ecffc34e42ccce8727198179c84e19a054b92b33cd1553d1c281e020e69c298a25912f1b9b697fe43bd81e9008c88d53d17206f73001a7b5b0212194f2ee00e8f46ca49d8752e9749cdfcdfb17c1315fea22edf0f04e117ccabbe3322851e34510d35dfa1e")

        self.auth = self.client.refresh_bearer_token(
            client_secret='',
            client_id="421a09b495c9559a458eb06c8c5f41c1",
            refresh_token="def502007b613dc7114efb6b2e0dc50593a060fbfedda409cea33a2eb409824edc6c95a1e1d5c6c7c0eeb40e7f5ec3f8b9fe1a249248b7a73b352efa1526ad20405b2611b1608ac1f1cd60d7e8445e0879fa35928a90b5b82129f8a6360e212e84cf7b9ef4aed3f4387e708b1e5c5f83dc43c9e43aa8e0dfd24d4e6c9a2559b929b73af4bed8499c2255f22b130ee491ccd0212b3f14505b5c25624dded5b72c71427540b0b08b8b2d696470ac83f4b48db6053b2a74cc757e53c37fa6b16d73049572c69c09012d9687208a9c1ff9f91d2f34e46d1e376ba97d34834db68a6e6aa1c4adf28f37d2e7f305c3b4b54010309119a32f6a55d56afb8b751210ecce2a667f45cd8750caf6d506167c220bf97eb35ffd3c2f9d9a4011819968892be95905e678ecffc34e42ccce8727198179c84e19a054b92b33cd1553d1c281e020e69c298a25912f1b9b697fe43bd81e9008c88d53d17206f73001a7b5b0212194f2ee00e8f46ca49d8752e9749cdfcdfb17c1315fea22edf0f04e117ccabbe3322851e34510d35dfa1e")

        self._usr_inp = None
        self._sel_ani = None
        self._anime_search_result = None
        self._anime_search_result_string = None

        self.title = None
        self.alt_title = None
        self.year_aired = None
        self.score = None
        self.score_count = None
        self.media = None
        self.status = None
        self.genres = None
        self.episodes = None
        self.synopsis = None
        self.my_list = None

    def aninfo(self):

        while True:
            self._usr_inp = input('[+] Search Anime: ')

            if len(self._usr_inp) == 0:
                print('[!] Please enter a valid input!')
                continue

            else:
                self._anime_search_result = self.client.search_anime(self._usr_inp)
                for _index, _anime in enumerate(self._anime_search_result):
                    del self._anime_search_result[_index + 1]

                self._anime_search_result_string = [fill(_anime.title, 80) for _anime in self._anime_search_result]
                self._anime_search_result_string.append('[CANCEL]')
                self._anime_search_result_string.append('[CHANGE SEARCH ENGINE]')

                _anime_selected = inquirer.prompt([inquirer.List('selected anime', message="Which one?",
                                                                 choices=list(self._anime_search_result_string))])[
                    'selected anime']

                if _anime_selected == '[CANCEL]':
                    self.aninfo()

                elif _anime_selected == '[CHANGE SEARCH ENGINE]':
                    _usr_inp = self._usr_inp
                    html = PoolManager()

                    _search_engine = inquirer.prompt([inquirer.List('selected engine', message="Which anime provider you'd like to use?", choices=['MyAnimeList', 'AnimeKisa', 'GogoAnime'])])['selected engine']
                    print(f'[+] Search engine {_search_engine} selected!')
                    if _search_engine == 'MyAnimeList':
                        self.aninfo()

                    elif _search_engine == 'AnimeKisa':
                        print('[+] Changed search engine to AnimeKisa\n')
                        def aksearch():
                            _initial_search = html.request('GET', 'https://animekisa.tv/search?q=' + str(
                                (urlencode({'q': f'{_usr_inp}'}).split('='))[-1]))
                            _initial_search_result = (
                                BeautifulSoup(_initial_search.data, features='html.parser')).select(
                                '.lisbox22 .similarbox .centered div')

                            if _initial_search.status != 200:
                                print(
                                    f'[!] AnimeKisa error code {_initial_search.status}! Please try again in several '
                                    f'minutes!')
                                quit()
                            elif len(_initial_search_result) == 0:
                                print('[!] Could not find anything. Please try again.   ')
                                print('fail')
                                self.aninfo()

                            else:
                                title_name = (inquirer.prompt([inquirer.List('Selected', message="Which one?",
                                                                             choices=[_item.text.replace('\n', '') for
                                                                                      _index, _item in
                                                                                      enumerate(_initial_search_result)
                                                                                      if _index % 2 == 0])]))[
                                    'Selected']

                                if list(title_name)[-1] == ' ':
                                    title_name = title_name[:-1]
                                if list(title_name)[0] == ' ':
                                    title_name = title_name[0:]

                                rep = {" ": "-", ":": "", "’": "-", "?": "", "!": "", ".": "", "/": "-", '★': '',
                                       '%': '', '+': '', '=': '',
                                       '³': '-'}
                                rep = dict((escape(k), v) for k, v in rep.items())
                                pattern = compile("|".join(rep.keys()))

                                program_friendly_name = pattern.sub(lambda m: rep[escape(m.group(0))],
                                                                    title_name.casefold())
                                # program_friendly_name = pattern.sub(f'[^\w]', title_name.casefold())
                                return title_name, program_friendly_name

                        def akdetails():
                            anime_link = aksearch()
                            anime_info = BeautifulSoup(
                                (html.request('GET', f'https://animekisa.tv/{anime_link[1]}')).data,
                                features='html.parser')

                            anime_details = [("".join(c.find_all(text=True))) for c in
                                             anime_info.find_all('div', {'class': 'textc'}, text=True)]
                            anime_details.append(
                                str(anime_info.find('div', {'class': 'infodes2'}).getText()).replace('\'', '’'))
                            genre = [("".join(g.find_all(text=True))) for g in
                                     anime_info.find_all('a', {'class': 'infoan'}) if
                                     not g.has_attr('target')]
                            if len(anime_details) == 3:
                                anime_details.insert(0, anime_link[0])

                            alias = anime_details[0]
                            status = anime_details[1]
                            episodes = anime_details[2]
                            synopsis = anime_details[3]
                            title = anime_link[0]
                            program_safe_title = anime_link[1]

                            if episodes == '?':
                                episodes = anime_info.find('div', {'class': 'infoept2'}).getText()
                                return episodes

                            print('\n' + tabulate([['Title', alias],
                                                   ['Alias', alias],
                                                   ['Category', ", ".join(genre)],
                                                   ['Episodes', episodes],
                                                   ['Status', status]],
                                                  tablefmt='orgtbl'), '\n\n', fill(synopsis, 100), '\n\n')
                            return alias, status, episodes, synopsis, program_safe_title, title

                        akdetails()

                    elif _search_engine == 'GogoAnime':
                        print('[+] Changed search engine to GogoAnime\n')
                        def ggasearch():

                            _initial_requests = html.request('GET', 'https://gogoanime.pe//search.html?keyword=' + str(
                                (urlencode({'q': f'{_usr_inp}'}).split('='))[-1]))

                            if _initial_requests.status != 200:
                                print(
                                    f'[!] Gogoanime error code {_initial_requests.status}! Please try again in '
                                    f'several minutes!')
                                quit()

                            _search_result = BeautifulSoup(_initial_requests.data, features='html.parser')
                            _search_result = _search_result.select('.last_episodes .items .name a')

                            _title_list = []
                            _href_list = []

                            if len(_search_result) == 0:
                                print('[!] Could not find anything. Please try again!')
                                print('fail')
                                ggadetails()

                            else:
                                for _index, _item in enumerate(_search_result):
                                    _title_list.append(_item.text)
                                    _href_list.append(_item['href'])

                                _title_list.append('Cancel')

                                selection = [inquirer.List('Selected', message="Which one?", choices=_title_list)]
                                title_name = (inquirer.prompt(selection))['Selected']

                                if title_name == 'Cancel':
                                    self.aninfo()

                                _index_bridge = int(_title_list.index(f"{title_name}"))
                                title_link = _href_list[_index_bridge]

                                return title_name, title_link

                        def ggadetails():
                            _search_result = ggasearch()
                            _title = ""
                            try:
                                _title = _search_result[0]
                            except TypeError:
                                ggadetails()

                            _link = _search_result[1]
                            _details_result = html.request('GET', 'https://gogoanime.pe/' + _link)
                            _details_result = BeautifulSoup(_details_result.data, features='html.parser')

                            infodes = [_details.text.replace('\n', '') for _details in
                                       _details_result.find_all('p', {'class': 'type'})]
                            infodes = [_det if ':' not in _det else (_det.split(': ')[-1]) for _det in infodes]
                            infodes.append(_details_result.find('a', {'class': 'active'}).text.split('-')[-1])

                            print(tabulate([['Title', _title],
                                            ['Alternative Title', infodes[5]],
                                            ['Genre', infodes[2]],
                                            ['Type', infodes[0]],
                                            ['Status', infodes[4]],
                                            ['Released', infodes[3]],
                                            ['Episodes', infodes[6]]], tablefmt='orgtbl'),
                                  '\n\n' + fill(infodes[1], 80), '\n')

                            return infodes[-1], _link, _title
                        ggadetails()
                #
                # _anime_details = self.client.get_anime_details(
                #     self._anime_search_result[int(self._anime_search_result_string.index(_anime_selected))].id)
                #
                # self.title = _anime_details.title
                # self.alt_title = _anime_details.alternative_titles.en
                #
                # try:
                #     self.year_aired = _anime_details.start_season.year
                # except AttributeError:
                #     self.year_aired = '?'
                #
                # self.year_aired = _anime_details.start_season.year
                # self.score = _anime_details.mean
                # self.media = _anime_details.media_type
                # self.status = _anime_details.status
                # self.genres = ", ".join(
                #     [_anime_details.genres[gen_index].name for gen_index in range(0, len(_anime_details.genres))])
                # self.episodes = _anime_details.num_episodes
                # self.synopsis = _anime_details.synopsis
                #
                # try:
                #     self.my_list = _anime_details.my_list_status
                # except AttributeError:
                #     self.my_list = '-'
                #
                # print(tabulate([['Title', self.title],
                #                 ['Alternative Title', self.alt_title],
                #                 ['Scpre', self.score],
                #                 ['Genre', self.genres],
                #                 ['Type', str(self.media).upper()],
                #                 ['Status', (str(self.status).replace("_", ' ')).title()],
                #                 ['Released', self.year_aired],
                #                 ['Episodes', self.episodes]], tablefmt='orgtbl'), '\n\n' + fill(self.synopsis, 80),
                #       '\n')


if __name__ == '__main__':
    print(
        '=' * 55 + '\n _ _ _         _   \n| | | |___ ___| |_   AnimeHub Framework by Neek0tine\n| | | | -_| -_| . '
                   '|  Version 0.1\n|_____|___|___|___|  https://github.com/neek0tine\n' + '=' * 55)
    ahf = ahframework()

    main_selection = \
        (inquirer.prompt([inquirer.List('Main Menu', message="What to do?", choices=['Search Anime', 'Cancel'])]))[
            'Main Menu']

    if main_selection == 'Cancel':
        quit()
    else:
        ahf.aninfo()
