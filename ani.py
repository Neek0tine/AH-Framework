import winreg
import malclient
import inquirer
from os import scandir


class ahframework:
    def __init__(self):
        self.client = malclient.Client()
        self.client.init(
            refresh_token="def502007b613dc7114efb6b2e0dc50593a060fbfedda409cea33a2eb409824edc6c95a1e1d5c6c7c0eeb40e7f5ec3f8b9fe1a249248b7a73b352efa1526ad20405b2611b1608ac1f1cd60d7e8445e0879fa35928a90b5b82129f8a6360e212e84cf7b9ef4aed3f4387e708b1e5c5f83dc43c9e43aa8e0dfd24d4e6c9a2559b929b73af4bed8499c2255f22b130ee491ccd0212b3f14505b5c25624dded5b72c71427540b0b08b8b2d696470ac83f4b48db6053b2a74cc757e53c37fa6b16d73049572c69c09012d9687208a9c1ff9f91d2f34e46d1e376ba97d34834db68a6e6aa1c4adf28f37d2e7f305c3b4b54010309119a32f6a55d56afb8b751210ecce2a667f45cd8750caf6d506167c220bf97eb35ffd3c2f9d9a4011819968892be95905e678ecffc34e42ccce8727198179c84e19a054b92b33cd1553d1c281e020e69c298a25912f1b9b697fe43bd81e9008c88d53d17206f73001a7b5b0212194f2ee00e8f46ca49d8752e9749cdfcdfb17c1315fea22edf0f04e117ccabbe3322851e34510d35dfa1e")
        self.auth = self.client.refresh_bearer_token(
            client_secret='',
            client_id="421a09b495c9559a458eb06c8c5f41c1",
            refresh_token="def502007b613dc7114efb6b2e0dc50593a060fbfedda409cea33a2eb409824edc6c95a1e1d5c6c7c0eeb40e7f5ec3f8b9fe1a249248b7a73b352efa1526ad20405b2611b1608ac1f1cd60d7e8445e0879fa35928a90b5b82129f8a6360e212e84cf7b9ef4aed3f4387e708b1e5c5f83dc43c9e43aa8e0dfd24d4e6c9a2559b929b73af4bed8499c2255f22b130ee491ccd0212b3f14505b5c25624dded5b72c71427540b0b08b8b2d696470ac83f4b48db6053b2a74cc757e53c37fa6b16d73049572c69c09012d9687208a9c1ff9f91d2f34e46d1e376ba97d34834db68a6e6aa1c4adf28f37d2e7f305c3b4b54010309119a32f6a55d56afb8b751210ecce2a667f45cd8750caf6d506167c220bf97eb35ffd3c2f9d9a4011819968892be95905e678ecffc34e42ccce8727198179c84e19a054b92b33cd1553d1c281e020e69c298a25912f1b9b697fe43bd81e9008c88d53d17206f73001a7b5b0212194f2ee00e8f46ca49d8752e9749cdfcdfb17c1315fea22edf0f04e117ccabbe3322851e34510d35dfa1e")
        self._usr_inp = str()

    def aninfo(self):
        while True:
            self._usr_inp = input('[+] Search Anime: ')
            if len(self._usr_inp) == 0:
                print('[!] Please enter a valid input!')
                continue
            else:
                _anime = self.client.search_anime(self._usr_inp, limit=1)
                _anime_details = self.client.get_anime_details(_anime[0].id)
                print(_anime_details)

                print('[!] Could not find any anime matching the query. Please try again!')
                continue



        #
        #
        # _anime_selection = inquirer.prompt([inquirer.List('anime selection', message="Which one?",
        #                                                   choices=list(_anime_list_string))])['anime selection']
        #
        # _anime_list_index = _anime_list_string.index(_anime_selection)
        # print(_anime_list_index)
        #
        # _anime_selected = self.client.search_anime(_anime_selection.title)
        # _anime_details = self.client.get_anime_details(_anime_selected)
        # print(_anime_details)
        # return self._usr_inp



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
