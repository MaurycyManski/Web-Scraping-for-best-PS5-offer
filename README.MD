# Find the best offer for your dream piece of tech!
Script written in python3 shows in terminal all PS5 offers from 3 most popular electromarkets from Poland:
* RTVeuroAGD, 
* MediaMarkt, 
* MediaExpert.

1. To run script simply type: "python3 webScraping.py" in terminal inside folder with webScraping.py and shops_links.json files. Every execution of this command updates offers.json file where dictionary of offers is stored. Script compare result from internet with what is saved in a file and every change of existing offer or new one is highlighted with red.

 2. To filter result f.e. you are into another controller or specific game in set, you can type one or multiple keyword in single/double quotes after -f parameter, like: -f 'key1 key2 ... '
example: python3 webScraping.py -f 'pad kontroler'

    Order of keywords and lower/uppercase doesn't matter. Execution of script with filter parameter do not save results to file and keep white color for all offers.

3. You can modify object of searching by changing links inside shops_links.json file (but keep the same shop site). So you can search f.e. for Xbox Series X or Nintendo Switch.

4. Photos of executed script are inside link below:
https://drive.google.com/drive/folders/1u0xbs0rPD786j9Od63Llo6pxwuo-vW3f?usp=sharing


