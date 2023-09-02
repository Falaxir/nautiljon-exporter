# Nautiljon Exporter

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
For now only "Terminé" (Completed) anime works.

Make sure your Nautiljon list is public, you can do that on your preferences.
Go to the file `exporter.py` and edit at the begining:
- username
 - The username of the list to export, you can find that when going to your Nautiljon list at the address bar.
- status_list
 - You can keep as it is, it is a list of category to save on the xml format.
- update_all_entries
 - When set to `True`, it will replace all your existing data on your  
Now you can run the command in your virtual env:
```shell
$ python3 exporter.py
```
Process might take a while depending on the size of your list.

## How to import to myanimelist.net
Go to the [myanimelist.net import page](https://myanimelist.net/import.php)
Select myanimelist import, and pick the `nautilist.xml` file.
Now your list should be imported

## Note on Nautiljon request accessibility 
Nautiljon uses cloudflare security to avoid scraping. This script only get two time the nautiljon list of the profile when running. For now, [cloudscraper](https://github.com/VeNoMouS/cloudscraper) is used but keep in mind it will need to be updated in the future.

## Credits

Thanks to @Dranixx for the original code that i improved to make it up to date.
