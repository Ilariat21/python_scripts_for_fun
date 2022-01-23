# How to Download a Manga from a Web Page using Python

To install the dependencies, run

```pip3 install -r requirements.txt```


*(For example)* To download the ***162nd chapter of Jujutsu Kaisen*** manga from https://jujmanga.com/manga/jujutsu-kaisen-chapter-162/ and name it ***jjk_ch162***, run

`python get_manga.py -n jjk_ch162 https://jujmanga.com/manga/jujutsu-kaisen-chapter-162/`

If you do not include name, it will be ***jujmanga.com***

For any help, run

```python get_manga.py --help```

Output should be
```
usage: get_manga.py [-h] [-n NAME] url

This script downloads all images from a web page and creates a pdf file from them

positional arguments:
  url                   The URL of the web page you want to download images

optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  The name of the pdf file, default is the domain of URL passed
```


