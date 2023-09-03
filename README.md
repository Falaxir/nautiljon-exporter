# Nautiljon Exporter

Nauliljon animes list exporter to MAL XML format. \

Use this tool to export your Nauliljon gallery, it can be usefull to make backups and import your gallery into a new platform.

## How to configure
Make sure you have Python 3.x installed (tested with python 3.10)
Enable virtual env to install packets in a seperate environement.
```shell
$ python3 -m virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```
If you want exit the virtual environment
```shell
$ desactivate
```

## How to run
Make sure your Nautiljon list is public, you can do that on your preferences ("Nauti'liste" and "bloc-notes"). \
Go to the file `exporter.py` and edit at the begining:
- username
    - The username of the list to export, you can find that when going to your Nautiljon list at the address bar.
- status_list
    - You can keep as it is, it is a list of category to save on the xml format.
- update_all_entries
    - When set to `True` (recommanded), it will replace all your existing matching data on your existing MAL list.

Now you can run the command in your virtual env:
```shell
$ python3 exporter.py
```
Process might take a while depending on the size of your list. It took ~17m on a list of ~500 entries.

## How to import to myanimelist.net (MAL)
Go to the [myanimelist.net import page](https://myanimelist.net/import.php) \
Select myanimelist import, and pick the `nautilist.xml` file. \
Now your list should be imported.\
> **NOTE**: Make sure to compare the entries, it might be possible due to name duplicates (ex: upcoming seasons that dont have a distinctive name yet) that it marked the wrong season. So check and compare your entries after importing, especially the plan to watch.

## Export to other websites
You might want to use [animeManga-autoBackup](https://github.com/Animanga-Initiative/animeManga-autoBackup) after you exported your Nautiljon list. \
You can export your MAL list [here](https://myanimelist.net/panel.php?go=export)

## Limitations and Supported sections
- Nauti'liste Anime
    - ✅ Status ("En cours", "Terminé", "En pause", "Abandonné")
    - ✅ Score given
    - ✅ Episodes watched
    - ❌ Number of rewatch
- Bloc-notes
    - ✅ Planned to watch
- Others
    - ❌ Favourites
    - ❌ Custom lists

## Note on Nautiljon request accessibility 
Nautiljon uses cloudflare security to avoid scraping. This script only get two time the nautiljon list of the profile when running. For now, [cloudscraper](https://github.com/VeNoMouS/cloudscraper) is used but keep in mind it will need to be updated or even changed in the future.

## Credits

Thanks to Dranixx for the original code that i improved to make it up to date.
