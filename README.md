
<a href='https://discord.gg/gWqbP9j3EV'> ![Discord](https://img.shields.io/discord/257479001365413889?label=Discord&style=flat-square) This is where I live. </a>


# AnimeHub Framework

AniHub is a video scraping framework whose task simply to look for animes info and downloads it (batch or single). The framework has built-in feature such as:
- Anime search 
- Anime batch download
- MyAnimeList status editor
- Multiprovider scrapping. (MyAnimeList, AnimeKisa, Gogoanime)

The framework utilize Microsoft Edge Selenium Webdriver as its webscrapping engine as it easily overcome the struggles that often occur when webscraping, such as Java script 
enabled buttons, iframes, token based GET requests, and complex request headers. Surely, all these are too good to be true if done without a problem. The webengine driver also
have its own problems, one of which are the severe hit on performance as webengine requires to be setup before action. Webengine driver also require a stable internet cnnection
as sometimes the program clicks faster than the page lods and leads to a standstill. Other than that, this program is pretty stable compared to other video scrappers.

## Usage

As the program is spesifically designed to be as intuitive as possible, there is not much explaining of how one uses this program.
Upon starting up, the user will be given 3 choice: Search, Update data and exit. The download option will be available when the target pops up in 
search result.

The option to change provider will also be available when the user already started a search. If the user did not find what they were looking for, provider 
change button will be available on the second from bottom selection menu.

Lastly, until the serie is found and episodes are available, the download prompt will be offered to the user. By clicking this prompt the anime will be downloaded 
in batch in respect of the current available episodes.


## End-User License Agreement

By running the software, the user acknowledged that:
 1. The user acknowledges that this app is made for EDUCATIONAL PURPOSES ONLY, and the Author emphasize to not use this program so oftenly, as to not disturb the streaming service (Anime Kisa) traffic .
 2. The user agrees and follows the Term of Service provided [LICENSE](https://github.com/Neek0tine/AKDownloader/blob/master/LICENSE)
 3. All changes that happened to end-user's computer, online account, or property made by running this appplication is NOT the responsibilty of the author


## Authors

* **Nick "Neek0tine" Calvin** - *Initial work* - [Neek0tine](https://github.com/Neek0tine)

## Contributing

Pull requests are welcome. For major changes, how-to, and in-depth explanation, please discuss it with the author first using the discord link. 

## License
![PyPI - License](https://img.shields.io/pypi/l/PyCl)
<br>
This project is licensed under MIT License - see the [LICENSE](https://github.com/Neek0tine/AH-Framework/blob/master/LICENSE) file for details
