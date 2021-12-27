# Mahjong

Author: Valeria Izvoreanu, B4

### Description
This project implements the game of Mahjong, following Microsoft rules. You get three different classic tables: *turtle*, *fortress* and *dragon*. The aim of the game is to remove all Mahjong tiles from the game board. In order to move tiles, gamers should pick Mahjong tiles in pairs. Each tile pair must exactly be a match of each tile in the pair. Of course there are exceptions of this rule. You can match any flower with another flower tile. You can also match a seasons tile with another seasons tile. 

Each tile you attempt to select must be free to move.If you can move a tile without affecting other tiles then this means the selected tile is free. For example, you can not move a tile which is under another Mahjong tile in the tile pile.The Mahjong tiles which are under other tiles or stuck between other piles can not be played so can not be a pair with a free tile. In order to play with a stuck tile, gamer has to free tile by removing tiles around the stuck tile by making them pair with others. To win you have to remove all tiles from the board, if you fail to do so and no more matches are left you loose.

### Technology
This project is written in **Python 3.9** and uses the *pygame* library.
