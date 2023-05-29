import requests
import csv
import sqlite3
from os        import path, remove
from bs4       import BeautifulSoup
from itertools import zip_longest





def with_csv(number_of_game_list,games_name_list, game_release_date,game_on_sale, game_price_finished):
  print("Starting to creat CSV file.")
  project_name = input("What you want to name the CSV: ")

  games_info = [ number_of_game_list,games_name_list, game_release_date,game_on_sale, game_price_finished]
  exported = zip_longest(*games_info)
  with  open(f"{project_name}.csv", "w", encoding="utf-8") as output_file:
    dicwriter = csv.writer(output_file)
    dicwriter.writerow(['NO', 'name of the game', "game realese date", "on sale", "game prices"])
    dicwriter.writerows(exported)
    print("CSV file Done!")


def with_database(games_name_list, game_release_date,game_on_sale, game_price_finished):
  #We don't need number_of_game_list here because the sqlite3 have
  #rowid witch is the same as game N.O
  print("Starting to creat database.")
  project_name = input("What you want to name the database: ")
  file = path.join(f'{project_name}.db')
  try:
    remove(file)
    print("We deleted the old data_base if u want to save it move it to another directory or\nChoose another name")
  except:
    pass
  
  conn = sqlite3.connect(f'{project_name}.db')
  cursor = conn.cursor()

  cursor.execute('''
                CREATE TABLE games(
                  Name text,
                  realese_date text,
                  on_sale text,
                  price text
                )
                
                ''')

  cursor.executemany("INSERT INTO games VALUES (?, ?, ?, ?)", zip(games_name_list,game_release_date, game_on_sale,game_price_finished))

  conn.commit()
  conn.close()
  print("Done!")

def screab(csv_or_database):
  print(f"Ok so you choose {csv_or_database}")
  print("*"*50)
  f = input("what you want to search:  ")
  print("Witing request from server...")
  try:
    web = requests.get(f"https://store.steampowered.com/search/?term={f}")
  except:
    pass
  print('Succes!')
  src = web.content
  soup = BeautifulSoup(src, "lxml")
  games_name_list = []
  number_of_game_list = []
  game_details_list = []##
  game_release_date = []
  game_price = []##
  game_price_finished = []
  game_on_sale = []
  names_of_games = soup.find_all('span', {'class': 'title'})
  prices = soup.find_all('div', {'class' : 'responsive_secondrow'})
  g = 1
  print("Looping...")
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
  print("Done filtring the games.")
  if csv_or_database == "csv":
    with_csv(number_of_game_list,games_name_list, game_release_date,game_on_sale, game_price_finished)
  elif csv_or_database == "database":
    with_database(games_name_list, game_release_date,game_on_sale, game_price_finished)
  elif csv_or_database == 'both':
    with_csv(number_of_game_list,games_name_list, game_release_date,game_on_sale, game_price_finished)
    with_database(games_name_list, game_release_date,game_on_sale, game_price_finished)
  else:
    print("Unexpected Error happend!!")

  print("Thanks for using This scraping project by bettercallguts@")