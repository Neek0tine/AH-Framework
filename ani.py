import winreg
import inquirer
import malclient
from os import scandir
from textwrap import fill
from tabulate import tabulate


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

                self._anime_search_result_string = [_anime.title for _anime in self._anime_search_result]
                _anime_selected = inquirer.prompt([inquirer.List('selected anime', message="Which one?", choices=list(self._anime_search_result_string))])['selected anime']
                _anime_details = self.client.get_anime_details(self._anime_search_result[int(self._anime_search_result_string.index(_anime_selected))].id)

                self.title = _anime_details.title
                self.alt_title = _anime_details.alternative_titles.en
                self.year_aired = _anime_details.start_season.year
                self.score = _anime_details.mean
                self.media = _anime_details.media_type
                self.status = _anime_details.status
                self.genres = ", ".join([_anime_details.genres[gen_index].name for gen_index in range(0, len(_anime_details.genres))])
                self.episodes = _anime_details.num_episodes
                self.synopsis = _anime_details.synopsis
                self.my_list = _anime_details.my_list_status

                print(tabulate([['Title', self.title],
                                ['Alternative Title', self.alt_title],
                                ['Scpre', self.score],
                                ['Genre', self.genres],
                                ['Type', self.media],
                                ['Status', self.status],
                                ['Released', self.year_aired],
                                ['Episodes', self.episodes]], tablefmt='orgtbl'), '\n\n' + fill(self.synopsis, 80), '\n')


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
