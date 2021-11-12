import re
import json,  requests
import random
from random import choice
import time


regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def check_email(email):
    if(re.fullmatch(regex, email)):
        return True
 
    else:
        return False

def check_ingr(flav):
    data = requests.get(f"https://www.thecocktaildb.com/api/json/v1/1/search.php?i={flav.sp}").json()
    if data['ingredients'] == None:
        print("Return False")
        return False
    else:
        print("Return True")
        return True

def non_alco_cocktail(flav1): 
    data = requests.get(f'https://thecocktaildb.com/api/json/v1/1/filter.php?i={flav1}').json() # getting data from the first database
    dataNonAlco = requests.get('https://thecocktaildb.com/api/json/v1/1/filter.php?a=Non_Alcoholic').json() # getting data from the second database
    drinkByFlav = []
    drinkByAlco = []
    number_of_flav= 1
    lengh = len(data["drinks"])
    if lengh == 0:
        return False
    i=0
    for i in range (lengh): # storing all drinks id data to the list
        drinkByFlav.append(json.dumps((data["drinks"][i])["idDrink"], indent=4))
    lengh = len(dataNonAlco["drinks"])
    i=0
    for i in range (lengh): # storing all drinks id data to the list
        drinkByAlco.append(json.dumps((dataNonAlco["drinks"][i])["idDrink"], indent=4))
    finalDrinkOptions = [x for x in drinkByFlav if x in drinkByAlco]   # finalDrinkOptions = set(drinkByFlav).intersection(drinkByAlco) - I know about this method, but I can't use it due to fron data format on input
    drinkID = choice(finalDrinkOptions)
    return result_data(drinkID, number_of_flav)
    

def random_cocktail():
    data = requests.get('https://thecocktaildb.com/api/json/v1/1/random.php').json() 
    # drink = (data["drinks"])[0]
    drink = data['drinks'][0]
    picture = drink["strDrinkThumb"] 
    picture= picture.replace('"', '')          
    name = '"' + drink["strDrink"] + '"'    
    result = name, ingredients_in_list(drink), picture
    number_of_flav = 0
    return (result, number_of_flav)


def flavor_cocktail(flav1, flav2 = None, flav3 = None):

    # inputs = [input(f"{i}: ").strip() for i in range(1, n + 1)] # maybe we want to add option of typing more that 3 ingredients
    # n = 3 # any number of flavors

    #  .strip() - just removing whitespaces
    if flav1!=None and flav2!=None and flav3!=None:
        flavours = flav1.strip(),flav2.strip(),flav3.strip()
    elif flav1!=None and flav2!=None:
        flavours = flav1.strip(),flav2.strip()
    else: # flav1!=None:
        flavours = flav1.strip(),flav2.strip()

    data = []
    error_text = []
    search_ingredients = []
    matching_drinks = {}
    list_of_ing = ''
    flavours_used = 0

    seconds_elapsed = time.time_ns() # just for me to see to speed of function :)

    for i in flavours:  #taking all data about dirnks withe ach ingredient separaetely
        response = requests.get(f'https://thecocktaildb.com/api/json/v1/1/filter.php?i={i}')
        if response.content:  # if there are cocktails with this ingredient in database
            drinks = response.json()["drinks"]
            error_text.append(f'Found {len(drinks)} drinks with {i}')  # how much drink we have we this flavour
            data.append(drinks)
            search_ingredients.append(i) # storing ingredient's names in order to use later
        else:
            error_text.append(f'No drinks with {i}')  # we can use "result" to if there is no cocktail with some flavour 

    if not data:  # if there are not cocktails with any of typed ingredients 
        # print('No drinks matching any of ingredients')
        return False
    else:
        for r in error_text: 
            print(r)

    ids = []  # list to search all matching drink options by ID

    for drinks_list in data:  # storing all the three lists with drink's options to new list, in order to find all matches
        ids.append([drink['idDrink'] for drink in drinks_list])

    # len(ids) how much (1,2,3) flavors we used taking data
    a=0
    for i in range(len(ids)):  # matches finder, starting from i=0
        ingredient = str(search_ingredients[i])  # we using search_ingredients list to take ingredients one after one
        for j in range(i, len(ids)):   # maybe just i+1??
            if i == j:  # in order not to compare the list with himself 
                continue # we just skip it  if ==
            res = set(ids[i]) & set(ids[j])
        
            if res:
                a = 1 # to check if we have at least one match
                ids[i] = list(res) # storing id from dictionary to the list
                ingredient += ', ' + str(search_ingredients[j])
        matching_drinks[ingredient] = ids[i]
    key = ''
    if a == 0:    # check if there was a least one match
        matching_drinks[key] = ids[0] # if no, we will do random choice throught cocktails only with first flavour
    else:
        for k in matching_drinks.keys():  # looking for the longest "matching list" (with the biggest number of matched ingredients)
            if len(k.split(',')) > len(key.split(',')):  # changing places if we found
                key = k

    # checking to much flavours used
    if str(key) == '':
        flavours_used = 1
    elif str(key) == (str(flav1) + ", " + str(flav2)) or str(key) == (str(flav2) + ", " + str(flav3)) or str(key) == (str(flav1) + ", " + str(flav3)):
        flavours_used = 2
    else: # str(key) == (flav1,flav2,flav3)
        flavours_used = 3

    data = requests.get(f'https://thecocktaildb.com/api/json/v1/1/lookup.php?i={random.choice(matching_drinks[key])}')
    # making random choice from all choosen drink's options and taking all info about it from the link
    
    if not data: # in case that we can't find drink with this ID, probably that's not possible, but better to check :)
        print('Something went wrong err: 078')
        return
    drink = data.json()['drinks'][0]  # Putting the choosen drink's data (in json) to the variable

    print('Finished in {:.3f} seconds'.format((time.time_ns() - seconds_elapsed) / 1000000000))
    
    picture = drink["strDrinkThumb"] 
    picture= picture.replace('"', '')    # deleting the " because we need only the link to add it to html page
    name = '"' + drink["strDrink"] + '"'  
    result_data = name,ingredients_in_list(drink),picture
    return (result_data, flavours_used)


def ingredients_in_list(drink):
    list_of_ing = ''
    for i in range(1, 15):  # 15 - max amount of ingredients
        try: 
            ingred = drink.get(f'strIngredient{i}') # storing all ingredients to a list
            if not ingred:
                break
            list_of_ing = list_of_ing + (str(ingred)) + ", "
        except KeyError:
            pass
    return (list_of_ing)
    

def result_data(drinkID, number_of_flav):
    drinkID = drinkID.replace('"', '')  # deleting the " because we need only numbers to them in the link below
    finalData = requests.get(f'https://thecocktaildb.com/api/json/v1/1/lookup.php?i={drinkID}').json()
    drink = (finalData["drinks"])[0]
    picture = drink["strDrinkThumb"] 
    picture= picture.replace('"', '')    # deleting the " because we need only the link to add it to html page
    name = '"' + drink["strDrink"] + '"'      
    result = name,ingredients_in_list(drink), picture 
    return (result, number_of_flav) # function 'ingredients_in_list' is storing ingredients to the list

# First version of code (was updated because of the slow speed)
# def flavor_cocktail(flav1, flav2, flav3):
#     data = requests.get(f'https://thecocktaildb.com/api/json/v1/1/filter.php?i={flav1}').json()
#     finalDrinkOptions = []  # list to store suitable drink options
#     number_of_flav = 0  # varible to count number of flavors used to generate the drink (sometimes we don't have drink with one of typed flavours)
#     if (flav2 != ''):  # in case that we have only one typed flavor
#         i=0
#         lengh = len(data["drinks"])
#         if (flav2 != '') and (flav3 != ''):  # First case, then we have all three flavours typed
#             for i in range (lengh):
#                 # drink ID = (data["drinks"][i])["idDrink"]
#                 moreData = requests.get (f'https://thecocktaildb.com/api/json/v1/1/lookup.php?i={(data["drinks"][i])["idDrink"]}').json()
#                 if flav2 == (moreData["drinks"][0])["strIngredient1"] or flav2 == (moreData["drinks"][0])["strIngredient2"] or flav2 == (moreData["drinks"][0])["strIngredient3"] or flav2 == (moreData["drinks"][0])["strIngredient4"] or flav2 == (moreData["drinks"][0])["strIngredient5"] or flav2 == (moreData["drinks"][0])["strIngredient6"]:
#                     if flav3 == (moreData["drinks"][0])["strIngredient1"] or flav3 == (moreData["drinks"][0])["strIngredient2"] or flav3 == (moreData["drinks"][0])["strIngredient3"] or flav3 == (moreData["drinks"][0])["strIngredient4"] or flav3 == (moreData["drinks"][0])["strIngredient5"] or flav3 == (moreData["drinks"][0])["strIngredient6"]:
#                         finalDrinkOptions.append(json.dumps((data["drinks"][i])["idDrink"], indent=4))
#             if  finalDrinkOptions != []:
#                 number_of_flav = 3
#                 drinkID = choice(finalDrinkOptions)  # random choice of final drink from all options that was found
#             else:
#                 number_of_flav = 2
#                 flav3 = ''
#                 moreData = None
#         if (flav2 != '') and (flav3 == ''): # Second case, we have only two flavours typed
#             for i in range (lengh):
#                 # drink ID = (data["drinks"][i])["idDrink"]
#                 moreData = requests.get (f'https://thecocktaildb.com/api/json/v1/1/lookup.php?i={(data["drinks"][i])["idDrink"]}').json()
#                 if flav2 == (moreData["drinks"][0])["strIngredient1"] or flav2 == (moreData["drinks"][0])["strIngredient2"] or flav2 == (moreData["drinks"][0])["strIngredient3"] or flav2 == (moreData["drinks"][0])["strIngredient4"] or flav2 == (moreData["drinks"][0])["strIngredient5"] or flav2 == (moreData["drinks"][0])["strIngredient6"]:
#                     finalDrinkOptions.append(json.dumps((data["drinks"][i])["idDrink"], indent=4))
#             if  finalDrinkOptions != []:
#                 number_of_flav = 2
#                 drinkID = choice(finalDrinkOptions)  # random choice of final drink from all options that was found
#             else:
#                 number_of_flav = 1
#                 flav2 = ''
#     if finalDrinkOptions == []:
#         number_of_flav = 1
#         drinkID = choice(data["drinks"]) ["idDrink"]
#     return result_data(drinkID, number_of_flav) 

