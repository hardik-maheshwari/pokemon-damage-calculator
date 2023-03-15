from typing import List,Dict,NamedTuple,Tuple
import csv
# from functools import cmp_to_key

input_filename= "./data/Emerald.csv"

route_dictionary: Dict[str,List[str]] = {}

"""
RouteDictionary: dict

A dictionary containing routes as keys and trainers as values.

The keys of the dictionary are strings representing the route name, while the
values are strings representing the trainer name. The dictionary is used to keep
track of which trainer is associated with each route.

Example:

    RouteDictionary = {
        "Route 1": "Ash Ketchum",
        "Route 2": "Brock",
        "Route 3": "Misty"
    }

"""

PokemonDictionary : Dict[str, List[str]] = {}

"""
pokemon_dictionary: dict

A dictionary containing pokemons as keys and trainers as values.

The keys of the dictionary are strings representing the pokemon name, while the
values are strings representing the trainer name. The dictionary is used to keep
track of which trainer is associated with each route.

Example:

    pokemon_dictionary = {
        "Pikachu": "Ash",
        "Nidkoing": "Brock,Paul"
    }

"""

PokemonInfo = NamedTuple("PokemonInfo", [
    ("pokemon", str),
    ("level", int),
    ("attack", Tuple[str, str, str, str]),
    ("stats", Tuple[int, int, int, int, int, int])
])

trainer_dictionary: Dict[str, List[PokemonInfo]] = {}

"""
A dictionary that stores information about Pokemon trainers and their Pokemon.

The keys of the dictionary are strings representing the names of trainers. The values are lists of
named tuples, where each named tuple contains information about a single Pokemon belonging to the
trainer. The named tuple has the following fields:

- `pokemon`: A string representing the name of the Pokemon.
- `level`: An integer representing the level of the Pokemon.
- `attack`: A tuple of four strings representing the Pokemon's four attacks.
- `stats`: A tuple of six integers representing the Pokemon's six stats (HP, Attack, Defense,
  Special Attack, Special Defense, Speed).

"""

# Open the input file in read mode

with open(input_filename,encoding="utf-8") as input_file:

    # Read the CSV file using the DictReader object
    reader = csv.DictReader(input_file)

    # Initialize variables

    last_encountered = ""    # Store the name of the last trainer encountered
    magma_count = 0          # Counter for Team Magma Grunts encountered
    aqua_count = 0           # Counter for Team Aqua Grunts encountered

    # Loop through each row in the CSV file

    for row in reader:
        
        # Extract information from the row
        name : str =  row["Name"]
        route : str =  row["Route"]
        pokemon : str =  row["Pokemon"]
        level : int =  int(row["Level"])

        # Extract the four attack names from the row
        attacks = (row["Attack 1"] , row["Attack 2"] , row["Attack 3"] , row["Attack 4"])

        # Extract the six stats from the row and convert them to integers
        stats = (int(row["HP"]), 
                 int(row["Attack"]), 
                 int(row["Defense"]),
                 int(row["Sp. Attack"]), 
                 int(row["Sp. Defense"]), 
                 int(row["Speed"])
                )
        
        # Create a named tuple to store the extracted information
        value: PokemonInfo = PokemonInfo(pokemon, level, attacks, stats)

        # Check if the name is empty or starts with '['

        if name=="" or name[0]=="[":
            
            # If it does, the trainer encountered is the same as the previous one

            pokemon_info : List[PokemonInfo]=[]
            pokemon_info = trainer_dictionary[last_encountered]

            pokemon_info.append(value)

            trainer_dictionary[last_encountered] = pokemon_info

        else:

            # If the name contains "Magma Grunt", increase the counter and add the count to the name
            if "Magma Grunt" in name:
                magma_count+=1
                new_name = name + " " + str(magma_count)
                name = new_name

            # Similarly if the name contains "Aqua Grunt", 
            # increase the counter and add the count to the name
            elif "Aqua Grunt" in name:

                aqua_count+=1
                new_name = name + " " + str(aqua_count)
                name = new_name

            # Store the name of the current trainer as the last encountered trainer
            last_encountered = name

            # Check if the trainer has already been encountered
            if name not in trainer_dictionary:

                # If not, create a new list of PokemonInfo objects
                pokemon_used  : List[PokemonInfo] = []
                pokemon_used.append(value)
                trainer_dictionary[name] = pokemon_used
            
            else:

                # If yes, append the new PokemonInfo object to the existing list
                pokemon_used = trainer_dictionary[name]
                pokemon_used.append(value)
                trainer_dictionary[name] = pokemon_used
            
            # Try to add the trainer's name to the list of trainers encountered on the current route
            
            try:
                trainer_list : List[str] = []
                trainer_list = route_dictionary[route]
                trainer_list.append(name)
                route_dictionary[route] = trainer_list

            # If the route has not been encountered before, create a new list with trainer's name
            except (KeyError,AttributeError):
                trainer_list =  []
                trainer_list.append(name)
                route_dictionary[route] = trainer_list


        if pokemon in PokemonDictionary:

            # If the pokemon is already in the dictionary, 
            # retrieve list of trainers who have used it
            trainer_list = PokemonDictionary[pokemon]

            # Check if the last trainer who used the pokemon is different from the current trainer
            if trainer_list[-1]!=last_encountered:

                # If the last trainer who used the pokemon is different from the current trainer, 
                # append the current trainer to the list
                trainer_list.append(last_encountered)

                # Update the dictionary with the updated list of trainers who have used the pokemon
                PokemonDictionary[pokemon] = trainer_list

        else:
             # If the pokemon is not already in the dictionary, 
             # create a new list with the current trainer as the only entry
            trainer_list =[]
            trainer_list.append(last_encountered)

            # Add the new entry to the dictionary with the pokemon as the key 
            # and the list of trainers as the value
            PokemonDictionary[pokemon] = trainer_list

# **************************************************************************** # 

# Testing Trainer_Dictionary
print()

for key,value_list in trainer_dictionary.items():

    if "Elite" in key :

        print("*" * 100)
        for value in value_list:
            
            pokemon,level,attacks,stats = value
            print(f"{pokemon} : {level} : {attacks} : {stats}")
        
        print("*" * 100)
        print()

print("*" * 100)

temp_list = trainer_dictionary["Champion Wallace"]
for temp in temp_list:
    pokemon,level,attacks,stats = temp
    print(f"{pokemon} : {level} : {attacks} : {stats}")

print("*" * 100)
print()


temp_list= trainer_dictionary["PKMN Trainer Steven"]

for temp in temp_list:
    pokemon,level,attacks,stats = temp
    print(f"{pokemon} : {level} : {attacks} : {stats}")

print("*" * 100)
print()

# ***************************************************************************** # 

# Testing  Route Dictionary and Pokemon Dictionary 


# def compare(key1,key2):
#   return len(pokemon_dictionary[key2])-len(pokemon_dictionary[key1])

# letter_cmp_key = cmp_to_key(compare)
# pokemon_list = sorted(pokemon_dictionary,key=letter_cmp_key)

pokemon_list = sorted(PokemonDictionary.items(), key=lambda x: len(x[1]), reverse=True)
route_list = sorted(route_dictionary.items() , key = lambda x : len(x[1]) , reverse=True )


for route, trainers in route_list:
    print(f"{route}: {len(trainers)}")

print()
print("*" * 100)
print()

for pokemon,trainers in pokemon_list :
    print(f"{pokemon} : {len(trainers)}")