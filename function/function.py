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
    finalDrinkOptions = [x for x in drinkByFlav if x in drinkByAlco]   #finalDrinkOptions = set(drinkByFlav).intersection(drinkByAlco) - I know about this method, but I can't use it due to fron data format on input
    drinkID = choice(finalDrinkOptions) 
    drinkID = drinkID.replace('"', '')
    # random choice of final drink from all options that was found
    moreData = requests.get(f'https://thecocktaildb.com/api/json/v1/1/lookup.php?i={drinkID}').json()
    drink = (moreData["drinks"])[0]
    # maybe we can show ingredients to user because it was a random choice, like only name isn't enough
    ingredients = drink["strIngredient1"] + ", " + drink["strIngredient2"] 
    if type(drink["strIngredient3"]) != type(None):
      ingredients = ingredients + ", " + (drink["strIngredient3"])
      if  type(drink["strIngredient4"]) != type(None):
           ingredients = ingredients + ", " + (drink["strIngredient4"])
           if  type(drink["strIngredient5"]) != type(None):
              ingredients = ingredients + ", " + (drink["strIngredient5"])
    result = drink["strDrink"], ingredients
    return result

def random_cocktail():
    data = requests.get('https://thecocktaildb.com/api/json/v1/1/random.php').json() 
    drink = (data["drinks"])[0]
    # maybe we can show ingredients to user because it was a random choice, like only name isn't enough
    ingredients = drink["strIngredient1"] + ", " + drink["strIngredient2"] 
    if type(drink["strIngredient3"]) != type(None):
      ingredients = ingredients + ", " + (drink["strIngredient3"])
      if  type(drink["strIngredient4"]) != type(None):
           ingredients = ingredients + ", " + (drink["strIngredient4"])
           if  type(drink["strIngredient5"]) != type(None):
               ingredients = ingredients + ", " + (drink["strIngredient5"])
    #drink = drink["strDrink"] + drink["idDrink"] + ingredients
    result = drink["strDrink"], ingredients
    return result
    

def flavor_cocktail(flav1, flav2):
    data = requests.get(f'https://thecocktaildb.com/api/json/v1/1/filter.php?i={flav1}').json()
    lengh = len(data["drinks"])
    i=0
    finalDrinkOptions = []
    for i in range (lengh):
        # drink ID = (data["drinks"][i])["idDrink"]
        moreData = requests.get (f'https://thecocktaildb.com/api/json/v1/1/lookup.php?i={(data["drinks"][i])["idDrink"]}').json()
        if flav2 == (moreData["drinks"][0])["strIngredient1"] or flav2 == (moreData["drinks"][0])["strIngredient2"] or flav2 == (moreData["drinks"][0])["strIngredient3"] or flav2 == (moreData["drinks"][0])["strIngredient4"] or flav2 == (moreData["drinks"][0])["strIngredient5"] or flav2 == (moreData["drinks"][0])["strIngredient6"]:
            finalDrinkOptions.append(json.dumps((data["drinks"][i])["idDrink"], indent=4))
            drinkID = choice(finalDrinkOptions)  # random choice of final drink from all options that was found
    drinkID = drinkID.replace('"', '')
    moreData = requests.get(f'https://thecocktaildb.com/api/json/v1/1/lookup.php?i={drinkID}').json()
    drink = (moreData["drinks"])[0]
    # maybe we can show ingredients to user because it was a random choice, like only name isn't enough
    ingredients = drink["strIngredient1"] + ", " + drink["strIngredient2"] 
    if type(drink["strIngredient3"]) != type(None):
      ingredients = ingredients + ", " + (drink["strIngredient3"])
      if  type(drink["strIngredient4"]) != type(None):
           ingredients = ingredients + ", " + (drink["strIngredient4"])
           if  type(drink["strIngredient5"]) != type(None):
              ingredients = ingredients + ", " + (drink["strIngredient5"])
    result = drink["strDrink"], ingredients
    return (result)

    # line 75: ina = '"' + (f"strIngredient{a}") + '"' and all this put to a loop, don't know is it possible
    # a=1 ... and then 2, 3, 4,...
    
    # picture link = ["strDrinkThumb"]
    # drinkGlass = ["strGlass"]
    # drink ID = ["idDrink"]