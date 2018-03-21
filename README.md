# HQ_Bot 🤖
![License: MIT][ico-license]

A bot to help answer questions on trivia apps like HQ and CashShow. This bot takes screenshot of the game on the phone and uses googles tesseract OCR to read the questions and options. It automates the process of googling of the answers and gives the most likely answer! It is 70%+ accurate! 

Since it is against the policy of HQ-trivia i do not encourage anyone to use this during a live game and this is purely for educational purposes.  

## Packages Used

Use python 3.6. In particular the packages/libraries used are...

* JSON - Data Storage 
* Pillow - Image manipulation
* Google-Search-API - Google searching
* wikipediaapi - Wikipedia searches
* pytesseract - Google's free/open source OCR (requires seperate installtion)
* beautifulsoup4 - Parse google searches/html
* lxml - Beautifulsoup parser
* opencv2 - Image maniplulation
* pyscreenshot - Take screenshot of the game
* wxPython - GUI interface

*To easily install these*
1. Install python 3.6
2. Install above packages
    * `$ pip3 install -r requirements.txt`
3. For tesseract 
    * `$ brew install tesseract`
4. For opencv
    * `$ brew install opencv`


## Usage

Make sure all packages above are installed. For android phones use [Vysor][link-vysor] and for iOS use quicktime player. **The code expects the phone to be on the left side of the screen.** If you want to change the screenshot co-ordinates change the values inside the ImageGrab in the `screen_grab()` function. To use the script : 

```bash
$ git clone https://github.com/sushant10/HQ_Bot
$ cd HQ_Bot
$ pip3 install -r requirements.txt
$ python3 answer_bot.py
Press s to screenshot live game, sampq to run against sample questions or q to quit:
s
...Question...
```
## Screenshots

<img src="https://github.com/sushant10/HQ_Bot/blob/master/Screens/screenshot3.png" width="900" height="540" />
<img src="https://github.com/sushant10/HQ_Bot/blob/master/Screens/screenshot2.png" width="500" height="320" />


## Contributing

All contributions welcome.

## Credits

- [Sushant Rao][link-author]
- [All Contributors][link-contributors]

## Special shout out
[Jake Mor][jake-mor] was the person behind HQuack, the most viral popular bot to help solve HQ questions. His implementation inspired me to try my own. I recommend reading this [article][jake-more] to learn more about the whole story.

## Useful links

- [Wikipedia-API][link-wikiapi]
- [Google-Search-API][link-gapi]
- [Tesseract][link-tesseract]

## License

The MIT License (MIT)

[ico-license]: https://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat-square
[link-vysor]: https://www.vysor.io/
[link-author]: https://github.com/sushant10
[link-contributors]: ../../contributors
[link-wikiapi]: https://pypi.python.org/pypi/wikipedia
[link-gapi]: https://github.com/abenassi/Google-Search-API
[link-mike]: https://github.com/mikealmond/hq-trivia-assistant
[link-tesseract]: https://github.com/tesseract-ocr/tesseract/wiki
[jake-mor]: http://jakemor.com/
[jake-more]: https://medium.com/@jakemor/hquack-my-public-hq-trivia-bot-is-shutting-down-5d9fcdbc9f6e
[sampq]: ()
