# Game of Thrones episodes-chapters chart

**View the chart at [joeltronics.github.io/got-book-show](http://joeltronics.github.io/got-book-show/)**

[<img src="http://joeltronics.github.io/got-book-show/chart-preview.png">](http://joeltronics.github.io/got-book-show/)

I like Game of Thrones - both the show and the books (yes, that's *A Song of Ice and Fire* for all you book-readers). I also like stats and graphs. So naturally, I made a chart that shows how the episodes line up to the book chapters. I don't know about you, but I think it's pretty cool.

This script generates 2 HTML files: the interactive web version and the static image "print" version. To turn the static version into images, I used Google Chrome with the extension [Full Page Screen Capture](https://chrome.google.com/webstore/detail/full-page-screen-capture/fdpohaocaechififmbbbbbknoalclacl). Since the print version does not have the settings checkboxes and menu on the page, it can have its spoiler scope, coloring, and whether or not to combine books 4+5 set via its query string - for example, by opening the page in a web browser and adding to the end of the URL so it follows this format:

```
bookshow_print.html?color=1&combine=0&spoilers=2
```

## Data sources

Chapter-episode data is partially taken from the [Game of Thrones Wiki](http://gameofthrones.wikia.com/wiki/Category:Episodes) and  westeros.org's ["Book to Screen" analysis](http://www.westeros.org/GoT/Episodes/), although much of this is based on my own analysis as well. Thanks also to the [Wiki of Ice and Fire](http://awoiaf.westeros.org/) for helping verify chapter details.

AFFC & ADWD chronological order is from [Boiled Leather](http://boiledleather.com/post/24543217702/a-proposed-a-feast-for-crows-a-dance-with-dragons) (spoiler warning!)

*Note: If you actually want to read them in combined order and it's your first time, [this spoiler-safe order](http://boiledleather.com/post/25902554148/a-new-reader-friendly-combined-reading-order-for-a) is much better.*

The Winds of Winter is based on preview chapters released so far, including chapters George R.R. Martin has read at conventions. Their actual order in the book is unknown.

## License

* All Python and Javascript code is licensed under the [GPL 3.0](http://www.gnu.org/licenses/)

* All HTML, CSS, and image files are licensed under the [Creative Commons BY-SA 4.0 license](http://creativecommons.org/licenses/by-sa/4.0/)
