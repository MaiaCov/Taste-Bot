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
    number_of_flav= 1
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
    if finalDrinkOptions!=[]:
        return result_data(drinkID, number_of_flav)
    else:
        return False # mistake, we don't have cocktail with pyped flaour

def random_cocktail():
    data = requests.get('https://thecocktaildb.com/api/json/v1/1/random.php').json() 
    drink = (data["drinks"])[0]
    picture = drink["strDrinkThumb"] 
    picture= picture.replace('"', '')          
    name = '"' + drink["strDrink"] + '"'    
    result = name, ingredients_in_list(drink), picture
    number_of_flav = 0
    return (result, number_of_flav)

def flavor_cocktail(flav1, flav2, flav3):
    data = requests.get(f'https://thecocktaildb.com/api/json/v1/1/filter.php?i={flav1}').json()
    finalDrinkOptions = []  # list to store suitable drink options
    number_of_flav = 0  # varible to count number of flavors used to generate the drink (sometimes we don't have drink with one of typed flavours)
    if (flav2 != ''):  # in case that we have only one typed flavor
        i=0
        lengh = len(data["drinks"])
        if (flav2 != '') and (flav3 != ''):  # First case, then we have all three flavours typed
            for i in range (lengh):
                # drink ID = (data["drinks"][i])["idDrink"]
                moreData = requests.get (f'https://thecocktaildb.com/api/json/v1/1/lookup.php?i={(data["drinks"][i])["idDrink"]}').json()
                if flav2 == (moreData["drinks"][0])["strIngredient1"] or flav2 == (moreData["drinks"][0])["strIngredient2"] or flav2 == (moreData["drinks"][0])["strIngredient3"] or flav2 == (moreData["drinks"][0])["strIngredient4"] or flav2 == (moreData["drinks"][0])["strIngredient5"] or flav2 == (moreData["drinks"][0])["strIngredient6"]:
                    if flav3 == (moreData["drinks"][0])["strIngredient1"] or flav3 == (moreData["drinks"][0])["strIngredient2"] or flav3 == (moreData["drinks"][0])["strIngredient3"] or flav3 == (moreData["drinks"][0])["strIngredient4"] or flav3 == (moreData["drinks"][0])["strIngredient5"] or flav3 == (moreData["drinks"][0])["strIngredient6"]:
                        finalDrinkOptions.append(json.dumps((data["drinks"][i])["idDrink"], indent=4))
            if  finalDrinkOptions != []:
                number_of_flav = 3
                drinkID = choice(finalDrinkOptions)  # random choice of final drink from all options that was found
            else:
                number_of_flav = 2
                flav3 = ''
                moreData = None
        if (flav2 != '') and (flav3 == ''): # Second case, we have only two flavours typed
            for i in range (lengh):
                # drink ID = (data["drinks"][i])["idDrink"]
                moreData = requests.get (f'https://thecocktaildb.com/api/json/v1/1/lookup.php?i={(data["drinks"][i])["idDrink"]}').json()
                if flav2 == (moreData["drinks"][0])["strIngredient1"] or flav2 == (moreData["drinks"][0])["strIngredient2"] or flav2 == (moreData["drinks"][0])["strIngredient3"] or flav2 == (moreData["drinks"][0])["strIngredient4"] or flav2 == (moreData["drinks"][0])["strIngredient5"] or flav2 == (moreData["drinks"][0])["strIngredient6"]:
                    finalDrinkOptions.append(json.dumps((data["drinks"][i])["idDrink"], indent=4))
            if  finalDrinkOptions != []:
                number_of_flav = 2
                drinkID = choice(finalDrinkOptions)  # random choice of final drink from all options that was found
            else:
                number_of_flav = 1
                flav2 = ''
    if finalDrinkOptions == []:
        number_of_flav = 1
        drinkID = choice(data["drinks"]) ["idDrink"]
    return result_data(drinkID, number_of_flav) # function 'ingredients_in_list' is storing ingredients to the list

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

def result_data(drinkID, number_of_flav):
    drinkID = drinkID.replace('"', '')  # deleting the " because we need only numbers to them in the link below
    finalData = requests.get(f'https://thecocktaildb.com/api/json/v1/1/lookup.php?i={drinkID}').json()
    drink = (finalData["drinks"])[0]
    picture = drink["strDrinkThumb"] 
    picture= picture.replace('"', '')    # deleting the " because we need only the link to add it to html page
    name = '"' + drink["strDrink"] + '"'      
    result = name,ingredients_in_list(drink), picture 
    return (result, number_of_flav) # function 'ingredients_in_list' is storing ingredients to the list
