# Nautiljon Exporter

Want to backup your anime list from Nautiljon but you can't because there is no option ? But now you can!

Nauliljon animes list exporter to MAL XML format. \
Nautiljon ==> Anilist.

## How to configure
Enable virtual env
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
> **NOTE**: Sometimes, you might need to import it at least two times in order to sucessfully import all the list. Especially if you have lot of data to import.

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
Nautiljon uses cloudflare security to avoid scraping. This script only get two time the nautiljon list of the profile when running. For now, [cloudscraper](https://github.com/VeNoMouS/cloudscraper) is used but keep in mind it will need to be updated in the future.

## Credits

Thanks to Dranixx for the original code that i improved to make it up to date.
