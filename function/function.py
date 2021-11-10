import re
import json,  requests
from random import choice

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def check_email(email):
    if(re.fullmatch(regex, email)):
        return True
 
    else:
        return False

def non_alco_cocktail(flav1): 
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
    drinkID = choice(finalDrinkOptions) 
    drinkID = drinkID.replace('"', '')  # deleting the " because we need only numbers to them in the link below
    
    # random choice of final drink from all options that was found
    moreData = requests.get(f'https://thecocktaildb.com/api/json/v1/1/lookup.php?i={drinkID}').json()
    drink = (moreData["drinks"])[0]
    picture = drink["strDrinkThumb"] 
    picture= picture.replace('"', '')    
    name = '"' + drink["strDrink"] + '"'
    result = name, ingredients_in_list(drink), picture
    return result

def random_cocktail():
    data = requests.get('https://thecocktaildb.com/api/json/v1/1/random.php').json() 
    drink = (data["drinks"])[0]
    picture = drink["strDrinkThumb"] 
    picture= picture.replace('"', '')          
    name = '"' + drink["strDrink"] + '"'    
    result = name, ingredients_in_list(drink), picture
    return result

def flavor_cocktail(flav1, flav2, flav3):
    data = requests.get(f'https://thecocktaildb.com/api/json/v1/1/filter.php?i={flav1}').json()
    lengh = len(data["drinks"])
    i=0
    number_of_flav = 3  # varible to count number of flavors used to generate the drink (sometimes we don't have drink with one of typed flavours)
    finalDrinkOptions = []  # list to store suitable drink options
    if (flav2 != None) and (flav3 != None):  # First case, then we have all three flavours typed
        for i in range (lengh):
            # drink ID = (data["drinks"][i])["idDrink"]
            moreData = requests.get (f'https://thecocktaildb.com/api/json/v1/1/lookup.php?i={(data["drinks"][i])["idDrink"]}').json()
            if flav2 == (moreData["drinks"][0])["strIngredient1"] or flav2 == (moreData["drinks"][0])["strIngredient2"] or flav2 == (moreData["drinks"][0])["strIngredient3"] or flav2 == (moreData["drinks"][0])["strIngredient4"] or flav2 == (moreData["drinks"][0])["strIngredient5"] or flav2 == (moreData["drinks"][0])["strIngredient6"]:
                if flav3 == (moreData["drinks"][0])["strIngredient1"] or flav3 == (moreData["drinks"][0])["strIngredient2"] or flav3 == (moreData["drinks"][0])["strIngredient3"] or flav3 == (moreData["drinks"][0])["strIngredient4"] or flav3 == (moreData["drinks"][0])["strIngredient5"] or flav3 == (moreData["drinks"][0])["strIngredient6"]:
                    finalDrinkOptions.append(json.dumps((data["drinks"][i])["idDrink"], indent=4))
        if  finalDrinkOptions != []:
            drinkID = choice(finalDrinkOptions)  # random choice of final drink from all options that was found
        else:
            number_of_flav = 2
            flav3 = None
            moreData = None
    if (flav2 != None) and (flav3 == None): # Second case, we have only two flavours typed
        for i in range (lengh):
            # drink ID = (data["drinks"][i])["idDrink"]
            moreData = requests.get (f'https://thecocktaildb.com/api/json/v1/1/lookup.php?i={(data["drinks"][i])["idDrink"]}').json()
            if flav2 == (moreData["drinks"][0])["strIngredient1"] or flav2 == (moreData["drinks"][0])["strIngredient2"] or flav2 == (moreData["drinks"][0])["strIngredient3"] or flav2 == (moreData["drinks"][0])["strIngredient4"] or flav2 == (moreData["drinks"][0])["strIngredient5"] or flav2 == (moreData["drinks"][0])["strIngredient6"]:
                finalDrinkOptions.append(json.dumps((data["drinks"][i])["idDrink"], indent=4))
        if  finalDrinkOptions != []:
            drinkID = choice(finalDrinkOptions)  # random choice of final drink from all options that was found
        else:
            number_of_flav = 1
            flav2 = None
    if (flav2 == None) and (flav3 == None):
        drink = (data["drinks"])[0]
        picture = drink["strDrinkThumb"] 
        picture= picture.replace('"', '')    # deleting the " because we need only the link to add it to html page
        name = '"' + drink["strDrink"] + '"'      
        result = name,ingredients_in_list(drink), picture
        return (result, number_of_flav)   # function 'ingredients_in_list' is storing ingredients to the list
    
    if finalDrinkOptions != []:
        drinkID = drinkID.replace('"', '')  # deleting the " because we need only numbers to them in the link below
        finalData = requests.get(f'https://thecocktaildb.com/api/json/v1/1/lookup.php?i={drinkID}').json()
        drink = (finalData["drinks"])[0]
        picture = drink["strDrinkThumb"] 
        picture= picture.replace('"', '')    # deleting the " because we need only the link to add it to html page
        name = '"' + drink["strDrink"] + '"'      
        result = name,ingredients_in_list(drink), picture 
        return (result, number_of_flav)

def ingredients_in_list(drink):
    ingredients = drink["strIngredient1"] + ", " + drink["strIngredient2"] 
    if type(drink["strIngredient3"]) != type(None):
      ingredients = ingredients + ", " + (drink["strIngredient3"])
      if  type(drink["strIngredient4"]) != type(None):
           ingredients = ingredients + ", " + (drink["strIngredient4"])
           if  type(drink["strIngredient5"]) != type(None):
              ingredients = ingredients + ", " + (drink["strIngredient5"])
    return ingredients

    # line 75: ina = '"' + (f"strIngredient{a}") + '"' and all this put to a loop, don't know is it possible
    # a=1 ... and then 2, 3, 4,...