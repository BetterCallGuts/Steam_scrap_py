import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest



f = input("what you want to search:  ")
web = requests.get(f"https://store.steampowered.com/search/?term={f}")
src = web.content
soup = BeautifulSoup(src, "lxml")

games_name_list = []
number_of_game_list = []
game_details_list = []
game_release_date = []
game_price = []##
game_price_finished = []
game_on_sale = []

names_of_games = soup.find_all('span', {'class': 'title'})
prices = soup.find_all('div', {'class' : 'responsive_secondrow'})




def screab():
    g = 1
    for i in range(len(names_of_games)):
        games_name_list.append( names_of_games[i].text.strip())
        number_of_game_list.append(g)
        g += 1
    for i in range(len(prices)):
        game_details_list.append(prices[i].text.strip())


    a = 0 #date game
    b = 1
    c = 2 #price
    d = 3 #on sale
    e = 4 #maybe price agin

    for i in range(len(names_of_games)):
        game_release_date.append(game_details_list[a])
        game_on_sale.append(game_details_list[d])
        game_price.append(game_details_list[c])
        a += 5
        d += 5
        c += 5


    for i in game_price:
        game_price_finished.append(i.replace("\n\n\n", "<-it was this but after the discount now: "))


screab()

# print(game_release_date )
# print("#" *100)
# print(game_on_sale)
# print("#"*100)
# print(game_price_finished)







games_info = [ number_of_game_list,games_name_list, game_release_date,game_on_sale, game_price_finished]
exported = zip_longest(*games_info)
with  open("games.csv", "w", encoding="utf-8") as output_file:
    dicwriter = csv.writer(output_file)
    dicwriter.writerow(['NO', 'name of the game', "game realese date", "on sale", "game prices"])
    dicwriter.writerows(exported)
    print("file created")














