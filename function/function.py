import re
import json,  requests
from random import choice

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def check_email(email):
    if(re.fullmatch(regex, email)):
        return True
 
    else:
        return False

def nonAlcoCocktail(flav1): # maybe add search by at least one word like 'coffee'?
    data = requests.get(f'https://thecocktaildb.com/api/json/v1/1/filter.php?i={flav1}').json() # getting data from the first database
    dataNonAlco = requests.get('https://thecocktaildb.com/api/json/v1/1/filter.php?a=Non_Alcoholic').json() # getting data from the second database
    drinkByFlav = []
    drinkByAlco = []
    lengh = len(data["drinks"])
    i=0
    for i in range (lengh): # storing all drinks id data to the list
        drinkByFlav.append(json.dumps((data["drinks"][i])["idDrink"], indent=4))
    lengh = len(dataNonAlco["drinks"])
    i=0
    for i in range (lengh): # storing all drinks id data to the list
        drinkByAlco.append(json.dumps((dataNonAlco["drinks"][i])["idDrink"], indent=4))
    finalDrinkOptions = [x for x in drinkByFlav if x in drinkByAlco]   # finalDrinkOptions = set(drinkByFlav).intersection(drinkByAlco) - I know about this method, but I can't use it due to fron data format on input
    drink = choice(finalDrinkOptions) # random choice of final drink from all options that was found
    # print(drink) - you will receive drink id
    return True

def random_cocktail():
    data = requests.get('https://thecocktaildb.com/api/json/v1/1/random.php').json() 
    drink = (data["drinks"][0])
    drinkID = (data["drinks"][0])["idDrink"]
    # maybe we can show ingredients to user because it was a random choice, like only name isn't enough
    ingredients = drink["strIngredient1"] + ", " + drink["strIngredient2"] 
    if type(drink["strIngredient3"]) != type(None):
      ingredients = ingredients + ", " + (drink["strIngredient3"])
      if  type(drink["strIngredient4"]) != type(None):
           ingredients = ingredients + ", " + (drink["strIngredient4"])
           if  type(drink["strIngredient5"]) != type(None):
               ingredients = ingredients + ", " + (drink["strIngredient5"])
    #print(drinkID)
    #print (ingredients)
    data = requests.get('https://thecocktaildb.com/api/json/v1/1/random.php').json() 
    drink = choice(data["drinks"]) 
    return drink

def flavor_cocktail(flav1, flav2):
    data = requests.get(f'https://thecocktaildb.com/api/json/v1/1/filter.php?i={flav1}').json()
    lengh = len(data["drinks"])
    i=0
    finalDrinkOptions = []
    for i in range (lengh):
        # drinkID = (data["drinks"][i])["idDrink"]
        moreData = requests.get (f'https://thecocktaildb.com/api/json/v1/1/lookup.php?i={(data["drinks"][i])["idDrink"]}').json()
        if flav2 == (moreData["drinks"][0])["strIngredient1"] or flav2 == (moreData["drinks"][0])["strIngredient2"] or flav2 == (moreData["drinks"][0])["strIngredient3"] or flav2 == (moreData["drinks"][0])["strIngredient4"] or flav2 == (moreData["drinks"][0])["strIngredient5"] or flav2 == (moreData["drinks"][0])["strIngredient6"]:
            finalDrinkOptions.append(json.dumps((data["drinks"][i])["idDrink"], indent=4))
            drink = choice(finalDrinkOptions)  # random choice of final drink from all options that was found
            # print (drink)
    return True 

    # ina = '"' + (f"strIngredient{a}") + '"'
    # a=1 ... and then 2, 3, 4,...
    # picture link = ["strDrinkThumb"]
    # drinkGlass = ["strGlass"]
    # drink ID = ["idDrink"]

    return True
