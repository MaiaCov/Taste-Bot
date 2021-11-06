import re
import json,  requests
from random import choice

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def check_email(email):
    if(re.fullmatch(regex, email)):
        return True
 
    else:
        return False

def nonAlcoCocktail():
    data3 = requests.get('https://www.thecocktaildb.com/api/json/v1/1/filter.php?a=Non_Alcoholic').json()
    drink = (f'Your drink is: {choice(data3["drinks"])}')
    drink_name = drink["strDrink"]
    pic= drink["strDrinkThumb"]
    return data3


# def random_cocktail():
#    data = requests.get('https://thecocktaildb.com/api/json/v1/1/random.php').json() 
#   drink = choice(data["drinks"]) 
#    drinkName = drink["strDrink"]
#   drinkPicture = drink["strDrinkThumb"]
#    ingredients = drink["strIngredient1"] + ", " + drink["strIngredient2"] 
#    if type(drink["strIngredient3"]) != type(None):
#      ingredients = ingredients + ", " + (drink["strIngredient3"])
#     if  type(drink["strIngredient4"]) != type(None):
#           ingredients = ingredients + ", " + (drink["strIngredient4"])
#           if  type(drink["strIngredient5"]) != type(None):
#               ingredients = ingredients + ", " + (drink["strIngredient5"])
    

#def flavor_cocktail(flav0, flav1):
#    ?? working with this? data1 = requests.get(f'https://thecocktaildb.com/api/json/v1/1/search.php?f={flav0}').json()
#    return data1