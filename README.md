# Text Based Browser

This a text-based web browser where you have the following options:
```
    * Enter a URL (e.g. "example.com")
    * Enter "back" to go to previous page
    * Enter just domain name to see saved search (e.g."example" for "example.com")
    * Enter "exit" to exit the browser
```

The program expects a parameter for the directory to save the searched site results and is run as follows:

``` browser.py [direcory_name]```

All searches are saved to the file system and then the user can see the saved results by entering only the domain name.

You can see a demo of the project below (links are shown in blue in the pages):

![gif2](https://user-images.githubusercontent.com/37106831/91997825-2b1af480-ed43-11ea-873e-41c63909a0d1.gif)

[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) is used for web scraping and [Colorama](https://pypi.org/project/colorama/) is used to color the text.

The following packages are installed to the project in the beginning:

```pip install bs4 colorama requests tldextract validators```

