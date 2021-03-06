import winreg
from os import scandir, makedirs, getenv
from re import sub, compile, escape
from textwrap import fill
from time import sleep
from urllib.parse import urlencode
import inquirer
import malclient
import pyloader
from bs4 import BeautifulSoup
from msedge.selenium_tools import Edge, EdgeOptions
from tabulate import tabulate
from urllib3 import PoolManager
import selenium_installer


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
        self.query_title = None
        self.file_title = None

        self.gogoanime = False

    def downloader(self, mode):

        def progress_callback(progress):
            print(f'\rDownloading File: {progress.dlable.file_name}  Progress: ' + '{0:.2f}%'.format(
                progress.percent), end='')
            # `return True` if the download should be canceled
            return False

        loader = pyloader.Loader.get_loader()

        loader.configure(
            max_concurrent=1,
            progress_cb=progress_callback,
            update_interval=3,
            daemon=False
        )

        loader.start()

        options = EdgeOptions()
        options.use_chromium = True
        options.headless = False
        options.add_argument(f"--user-data-dir={getenv('LOCALAPPDATA')}\\Microsoft\\Edge\\Generated Data")
        options.add_argument("--profile-directory=Default")
        options.add_argument("--disable-extensions")
        options.add_argument("--headless")
        options.add_argument('--log-level=3')
        driver = Edge(options=options)

        _custom_episode = int()
        _queue = list()

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                            'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders') as key:
            download_location = winreg.QueryValueEx(key, '{374DE290-123F-4565-9164-39C4925E467B}')[0]

        if mode == 'Single':
            while _custom_episode == 0:
                try:
                    _custom_episode = int(input(f'[+] Which episode you wish to download? (1-{self.episodes}): '))
                except ValueError:
                    print(f'[!] Please enter a valid episode (1 - {self.episodes}')

        else:
            _file_list = scandir(download_location + '/Downloader')
            try:
                makedirs(f'{download_location}\\Downloader\\{self.file_title}')
                _queue = [ep for ep in list(range(1, self.episodes + 1))]

            except FileExistsError:
                _queue = [ep for ep in list(range(1, self.episodes + 1)) if
                          ep not in ([int(((str(entry)).split(' '))[-1].split('.')[0]) for entry in (scandir(
                              download_location + '/Downloader/' + self.file_title))])]
                # _queue = [ep for ep in list(range(1, self.episodes + 1)) if ep not in [int((list(str(
                # ep.name).split(' '))[-1].split('.'))[0]) for ep in scandir(download_location + '/Downloader/' +
                # self.file_title)]]
                if len(_queue) == 0:
                    print('[+] File already exists without missing an episode. Please look for a new series!')
                    mainmenu()

                print('[+] Found existing folder in the directory, checking for episodes ... ')
                print(f'[+] Downloading missing episodes: {", ".join(str(v) for v in _queue)}.')

        def get_files(url, episode):
            print(fill(
                f'\n\n[+] Getting download link from {url} for {self.title} Episode {episode}/{self.episodes}',
                80))
            driver.get(url)
            try:
                driver.find_element_by_css_selector("#main > div:nth-child(7) > div").click()
                window_after = driver.window_handles[1]
                driver.close()
                driver.switch_to.window(window_after)
                _download_link = driver.find_element_by_css_selector(
                    '#main > div > div.content_c > div > div:nth-child(5) > div:nth-child(3) > a').get_attribute('href')

                target = pyloader.DLable(url=_download_link,
                                         target_dir=f'{download_location}\\Downloader\\{self.file_title}',
                                         file_name=f'{self.file_title} Episode {str(episode)}.mp4')
                loader.download(target)
            except:
                print('[+] Ouch, I missed the download button. Care to try again?')
                self.aninfo()

            while loader.is_active():
                sleep(2)

        def get_files_gogo(url, episode):
            print(fill(
                f'\n\n[+] Getting download link from {url} for {self.title} Episode {episode}/{self.episodes}',
                80))
            driver.get(url)
            try:
                driver.find_element_by_xpath(
                    '#wrapper_bg > section > section.content_left > div:nth-child(1) > div.anime_video_body > '
                    'div.anime_video_body_cate > div.favorites_book > ul > li.dowloads > a').click()
                window_after = driver.window_handles[1]
                driver.close()
                driver.switch_to.window(window_after)
                _download_link = driver.find_element_by_css_selector(
                    '#main > div > div.content_c > div > div:nth-child(5) > div:nth-child(3) > a').get_attribute('href')

                target = pyloader.DLable(url=_download_link,
                                         target_dir=f'{download_location}\\Downloader\\{self.file_title}',
                                         file_name=f'{self.file_title} Episode {str(episode)}.mp4')
                loader.download(target)
            except:
                print('[+] Ouch, I missed the download button. Care to try again?')
                self.aninfo()

            while loader.is_active():
                sleep(2)

        if _custom_episode != 0 and not self.gogoanime:
            link = ('https://animekisa.tv/' + (str(self.query_title).split('/'))[-1] + '-episode-' + str(
                _custom_episode))
            get_files(link, _custom_episode)
            print('[+] Download complete!\n')
            mainmenu()

        elif _custom_episode == 0 and not self.gogoanime:
            link = [('https://animekisa.tv/' + (str(self.query_title).split('/'))[-1] + '-episode-' + str(x)) for x in
                    _queue]
            _index = int(_queue[0])
            for _item in link:
                get_files(_item, _index)
                print()
                _index += 1
            print('[+] Download complete!\n')
            mainmenu()

        elif _custom_episode != 0 and self.gogoanime:
            link = ('https://gogoanime.pe/' + (str(self.query_title).split('/'))[-1] + '-episode-' + str(
                _custom_episode))
            get_files_gogo(link, _custom_episode)
            print('[+] Download complete!\n')
            mainmenu()

        elif _custom_episode == 0 and self.gogoanime:
            link = [('https://gogoanime.pe/' + (str(self.query_title).split('/'))[-1] + '-episode-' + str(x)) for x in
                    _queue]
            _index = int(_queue[0])
            for _item in link:
                get_files(_item, _index)
                print()
                _index += 1
            print('[+] Download complete!\n')
            mainmenu()

    def aninfo(self):
        while True:
            self._usr_inp = input('[+] Search Anime: ')

            if len(self._usr_inp) == 0:
                print('[!] Goodbye!')
                sleep(0.3)
                mainmenu()

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
                    mainmenu()

                elif _anime_selected == '[CHANGE SEARCH ENGINE]':
                    html = PoolManager()

                    _search_engine = inquirer.prompt([inquirer.List('selected engine',
                                                                    message="Which anime provider you'd like to use?",
                                                                    choices=['MyAnimeList', 'AnimeKisa',
                                                                             'GogoAnime'])])['selected engine']
                    print(f'[+] Search engine {_search_engine} selected!')
                    if _search_engine == 'MyAnimeList':
                        pass

                    elif _search_engine == 'AnimeKisa':
                        print('[+] Changed search engine to AnimeKisa!\n')

                        _title_name = None
                        _initial_search = html.request('GET', 'https://animekisa.tv/search?q=' + str(
                            (urlencode({'q': f'{self._usr_inp}'}).split('='))[-1]))
                        _initial_search_result = (
                            BeautifulSoup(_initial_search.data, features='html.parser')).select(
                            '.lisbox22 .similarbox .centered div')

                        if _initial_search.status != 200:
                            print(
                                f'[!] AnimeKisa error code {_initial_search.status}! Please try again in several '
                                f'minutes!')
                            mainmenu()

                        elif len(_initial_search_result) == 0:
                            print('[!] Could not find anything. Please try again.   ')
                            self.aninfo()

                        else:
                            _title_name = (inquirer.prompt([inquirer.List('Selected', message="Which one?",
                                                                          choices=[_item.text.replace('\n', '') for
                                                                                   _index, _item in
                                                                                   enumerate(_initial_search_result)
                                                                                   if _index % 2 == 0])]))[
                                'Selected']

                            if list(_title_name)[-1] == ' ':
                                _title_name = _title_name[:-1]
                            if list(_title_name)[0] == ' ':
                                _title_name = _title_name[0:]

                            rep = {" ": "-", ":": "", "???": "-", "?": "", "!": "", ".": "", "/": "-", '???': '', '%': '',
                                   '+': '', '=': '',
                                   '??': '-'}
                            rep = dict((escape(k), v) for k, v in rep.items())
                            pattern = compile("|".join(rep.keys()))

                            self.query_title = pattern.sub(lambda m: rep[escape(m.group(0))],
                                                           _title_name.casefold())

                        _anime_info = BeautifulSoup(
                            (html.request('GET', f'https://animekisa.tv/{self.query_title}')).data,
                            features='html.parser')

                        _anime_details = [("".join(c.find_all(text=True))) for c in
                                          _anime_info.find_all('div', {'class': 'textc'}, text=True)]
                        _anime_details.append(
                            str(_anime_info.find('div', {'class': 'infodes2'}).getText()).replace('\'', '???'))

                        self.genres = [("".join(g.find_all(text=True))) for g in
                                       _anime_info.find_all('a', {'class': 'infoan'}) if
                                       not g.has_attr('target')]

                        if len(_anime_details) == 3:
                            _anime_details.insert(0, _title_name)

                        self.alt_title = _anime_details[0]
                        self.status = _anime_details[1]
                        self.episodes = int(_anime_details[2])
                        self.synopsis = _anime_details[3]
                        self.title = _title_name

                        if self.episodes == '?':
                            self.episodes = int(_anime_info.find('div', {'class': 'infoept2'}).getText())

                    elif _search_engine == 'GogoAnime':
                        print('[+] Changed search engine to GogoAnime\n')
                        self.gogoanime = True

                        _initial_requests = html.request('GET', 'https://gogoanime.pe//search.html?keyword=' + str(
                            (urlencode({'q': f'{self._usr_inp}'}).split('='))[-1]))

                        if _initial_requests.status != 200:
                            print(
                                f'[!] Gogoanime error code {_initial_requests.status}! Please try again in '
                                f'several minutes!')
                            quit()

                        _search_result = BeautifulSoup(_initial_requests.data, features='html.parser')
                        _search_result = _search_result.select('.last_episodes .items .name a')

                        _title_list = []
                        _href_list = []
                        _title_link = ''
                        _title_name = ''

                        if len(_search_result) == 0:
                            print('[!] Could not find anything. Please try again!')
                            self.aninfo()

                        else:
                            for _index, _item in enumerate(_search_result):
                                _title_list.append(_item.text)
                                _href_list.append(_item['href'])

                            _title_list.append('Cancel')

                            selection = [inquirer.List('Selected', message="Which one?", choices=_title_list)]
                            _title_name = (inquirer.prompt(selection))['Selected']

                            if _title_name == 'Cancel':
                                mainmenu()

                            _index_bridge = int(_title_list.index(f"{_title_name}"))
                            _title_link = _href_list[_index_bridge]

                        _details_result = html.request('GET', 'https://gogoanime.pe/' + _title_link)
                        _details_result = BeautifulSoup(_details_result.data, features='html.parser')

                        infodes = [_details.text.replace('\n', '') for _details in
                                   _details_result.find_all('p', {'class': 'type'})]
                        infodes = [_det if ':' not in _det else (_det.split(': ')[-1]) for _det in infodes]
                        infodes.append(_details_result.find('a', {'class': 'active'}).text.split('-')[-1])

                        self.title = _title_name
                        self.alt_title = infodes[5]
                        self.genres = infodes[2]
                        self.media = infodes[0]
                        self.status = infodes[4]
                        self.year_aired = infodes[3]
                        self.episodes = int(infodes[6])
                        self.synopsis = infodes[1]
                else:
                    _anime_details = self.client.get_anime_details(
                        self._anime_search_result[int(self._anime_search_result_string.index(_anime_selected))].id)

                    self.title = _anime_details.title
                    self.alt_title = _anime_details.alternative_titles.en

                    try:
                        self.year_aired = _anime_details.start_season.year
                    except AttributeError:
                        self.year_aired = '?'

                    self.year_aired = _anime_details.start_season.year
                    self.score = _anime_details.mean
                    self.media = _anime_details.media_type
                    self.status = _anime_details.status
                    self.genres = ", ".join(
                        [_anime_details.genres[gen_index].name for gen_index in range(0, len(_anime_details.genres))])
                    self.episodes = int(_anime_details.num_episodes)
                    self.synopsis = _anime_details.synopsis

                    try:
                        self.my_list = _anime_details.my_list_status
                    except AttributeError:
                        self.my_list = '-'

                try:
                    print(tabulate([['Title', self.title],
                                    ['Alternative Title', self.alt_title],
                                    ['Score', self.score],
                                    ['Genre', self.genres],
                                    ['Type', str(self.media).upper()],
                                    ['Status', (str(self.status).replace("_", ' ')).title()],
                                    ['Released', self.year_aired],
                                    ['Episodes', self.episodes]], tablefmt='orgtbl'), '\n\n' + fill(self.synopsis, 80),
                          '\n')
                except AttributeError:
                    print('[!] Error, incomplete data. ')

                if self.query_title is None:
                    rep = {" ": "-", ":": "", "???": "-", "?": "", "!": "", ".": "", "/": "-", '???': '', '%': '', '+': '',
                           '=': '', '??': '-'}
                    rep = dict((escape(k), v) for k, v in rep.items())
                    pattern = compile("|".join(rep.keys()))
                    self.query_title = pattern.sub(lambda m: rep[escape(m.group(0))], self.title.casefold())

                    self.file_title = sub('[^A-Za-z0-9-,! ]+', '', self.title)

            download_confirmation = (inquirer.prompt(
                [inquirer.List('Selected', message="Proceed to download??", choices=['Cancel', 'All', 'Single'])]))[
                'Selected']
            if download_confirmation == 'Single':
                ahf.downloader(mode='Single')
            elif download_confirmation == 'Cancel':
                ahf.aninfo()
            elif download_confirmation == 'All':
                ahf.downloader(mode='All')


if __name__ == '__main__':
    ahf = ahframework()


    def mainmenu():
        print(
            '=' * 55 + '\n _ _ _         _   \n| | | |___ ___| |_   AnimeHub Framework by Neek0tine\n| | | | -_| -_| . '
                       '|  Version 0.1\n|_____|___|___|___|  https://github.com/neek0tine\n' + '=' * 55)

        main_selection = \
            (inquirer.prompt([inquirer.List('Main Menu', message="What to do?",
                                            choices=['Search Anime', 'Update ongoing series', 'Update MAL data', 'Cancel'])]))[
                'Main Menu']
        if main_selection == 'Cancel':
            quit()

        elif main_selection == 'Update ongoing series':
            print('This feature is being worked on!')

        elif main_selection == 'Update MAL data':

            _mal_anime_list = [str(entry.name) for entry in scandir(str(winreg.QueryValueEx(
                winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                               'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'),
                '{374DE290-123F-4565-9164-39C4925E467B}')[0]) + '\Downloader')]
            _mal_anime_list.append('Cancel')

            _mal_my_status = dict()
            _mal_anime = list()

            _mal_menu = (inquirer.prompt([inquirer.List('init', message="Is the anime already downloaded? ",
                                                        choices=['Yes', 'Custom Series', 'Cancel'])]))['init']

            if _mal_menu == 'Custom Series':
                _mal_anime = ahf.client.search_anime(input('[+] Enter anime name: '), limit=1)

            elif _mal_menu == 'Cancel':
                quit()

            else:
                _mal_title_name = (inquirer.prompt([
                    inquirer.List('Selected', message="Pick a series you wish to rate: ", choices=_mal_anime_list)]))[
                    'Selected']
                if _mal_title_name == 'Cancel':
                    self.select()

                _mal_anime = ahf.client.search_anime(_mal_title_name, limit=1)
            try:
                print(_mal_anime[0].title)
                print()
            except IndexError:
                print('[!] Sorry, currently this API has no access to this anime!')
                mainmenu()

            _mal_todo = (inquirer.prompt([
                inquirer.List('Todo', message='What to do',
                              choices=['Rate', 'Drop', 'Watch later', 'Hold', 'Cancel'])]))['Todo']

            print(f'[+] {_mal_todo}: ')

            if _mal_todo == 'Hold':
                _mal_my_status = {'status': 'on_hold'}
                print(_mal_anime[0].title, '\nStatus:', _mal_my_status['status'], '\n')

            elif _mal_todo == 'Watch later':
                _mal_my_status = {'status': 'plan_to_watch'}
                print(_mal_anime[0].title, '\nStatus:', _mal_my_status['status'], '\n')

            elif _mal_todo == 'Drop':
                _mal_my_status = {'status': 'dropped'}
                print(_mal_anime[0].title, '\nStatus:', _mal_my_status['status'], '\n')

            elif _mal_todo == 'Cancel':
                self.select()

            else:

                while True:
                    try:
                        _mal_score = int(input('How good? (1-10): '))
                        if _mal_score < 0 or _mal_score > 10:
                            print('[+] Please enter a valid number in range of 1 to 10!!\n')
                        else:
                            _mal_my_status = {'status': 'completed', 'score': _mal_score}
                            print(_mal_anime[0].title, '\nStatus:', _mal_my_status['status'], 'Score:',
                                  _mal_my_status['score'], '\n')
                            break
                    except TypeError:
                        print('[+] Please enter a valid number!\n')

            ahf.client.update_anime_my_list_status(_mal_anime[0].id, _mal_my_status)
            print('Status update success! Returning to main menu.. \n')
            mainmenu()

        else:
            ahf.aninfo()


    if selenium_installer.get_msedge_driver():
        while True:
            mainmenu()
