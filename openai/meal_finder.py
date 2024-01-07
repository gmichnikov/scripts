from openai import OpenAI
import sys
import os
import json


# Append the parent directory to sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from credentials import OPENAI_API_KEY

client = OpenAI(
  api_key=OPENAI_API_KEY,
)

# print("before call")

initial_info = input("Tell me who the meal will be for, which meal, etc.:\n")

completion = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    # model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a recipe suggestor. Your goal is to understand who is being fed, what materials and ingredients they have available, and deliver a suggestion they can actually make, and that meets their requirements."},
        {"role": "user", "content": "Here is some basic info about the meal I want: " + initial_info + "\nGive me a list of 12 ideas in json format like this: { \"suggestions\": [ {\"name\": <item_name>}, {\"name\": <item_name>} ... ] }\n"
        "It should be an array where each object just has a name property with the name of the suggested item or meal to cook."}
    ],
    max_tokens=500,
    temperature=0.8,
    response_format={ "type": "json_object" },
)

# print("after call")

# print(completion.choices[0].message)
print("Finish reason: " + completion.choices[0].finish_reason)
print("Usage: " + str(completion.usage) + "\n")
# print(completion.model)

content = completion.choices[0].message.content

# Parse the string to a JSON (dictionary) object
parsed_json = json.loads(content)

# Accessing the data
suggestions = parsed_json["suggestions"]
for index, suggestion in enumerate(suggestions, start=1):
    print(f"{index}. {suggestion['name']}")

while True:
    which_sound_good = input("\nWhich ones sound good? Enter numbers separated by commas or spaces:\n")

    try:
        # Convert the input string to a list of integers
        chosen_indices = [int(item.strip()) for item in which_sound_good.replace(',', ' ').split()]

        # Filter the suggestions
        filtered_suggestions = [suggestions[i - 1] for i in chosen_indices if 1 <= i <= len(suggestions)]

        # Break the loop if successful
        break

    except ValueError:
        # Handle invalid input
        print("Invalid input. Please enter valid numbers separated by commas or spaces.\n")

# Continue with filtered suggestions
print("\nYou have selected:")
for suggestion in filtered_suggestions:
    print("You chose: " + suggestion['name'])

meal_names = [suggestion['name'] for suggestion in filtered_suggestions]
meals_sentence = "Here are a list of meals that sound good to me: " + ", ".join(meal_names)


completion = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    messages=[
        {"role": "system", "content": "Your goal is to help a user figure out what to make for a meal. You'll be given a list of meal ideas that sound interesting to them. You need to help them think about the ingredients they need and compare them to which ones they have."},
        {"role": "user", "content": meals_sentence + ".\nPut together a list of unique ingredients I would need to make all of these. Don't include ingredients that I am very likely to have like butter, salt, eggs, flour, sugar, etc. Return a json object that looks like {\"ingredients\": [ <ingredients> ] } "}
    ],
    max_tokens=500,
    temperature=0.8,
    response_format={ "type": "json_object" },
)

# print(completion.choices[0].message)
print("\nFinish reason: " + completion.choices[0].finish_reason)
print("Usage: " + str(completion.usage))

content = completion.choices[0].message.content

# Parse the string to a JSON (dictionary) object
parsed_json = json.loads(content)

# Accessing the data
ingredients = parsed_json["ingredients"]
for index, ingredient in enumerate(ingredients, start=1):
    print(f"{index}. {ingredient}")


while True:
    have_ingredients = input("\nWhich of these do you have? Enter numbers separated by commas or spaces:\n")

    try:
        # Convert the input string to a list of integers
        chosen_indices = [int(item.strip()) for item in have_ingredients.replace(',', ' ').split()]

        # Filter the suggestions
        filtered_ingredients = [ingredients[i - 1] for i in chosen_indices if 1 <= i <= len(ingredients)]

        # Break the loop if successful
        break

    except ValueError:
        # Handle invalid input
        print("Invalid input. Please enter valid numbers separated by commas or spaces.\n")

# Continue with filtered suggestions
print("\nYou said ou have:")
for ingredient in filtered_ingredients:
    print("You chose: " + ingredient)

ingredient_sentence = "\nHere are a list of ingredients I have: " + ", ".join(filtered_ingredients)

what_can_i_make_prompt = meals_sentence + ". " + ingredient_sentence + ". I also have all the basics like flour, eggs, sugar, butter, bread, milk, and other common items.\n"
print(what_can_i_make_prompt)

completion = client.chat.completions.create(
    # model="gpt-3.5-turbo-1106",
    model="gpt-4-1106-preview",
    messages=[
        {"role": "system", "content": "Your goal is to help a user figure out what to make for a meal. You'll be given a list of meal ideas that sound interesting to them and a list of ingredients they have. You need to figure out which of the meal ideas they can make with the ingreidents they have. For each meal that they can make, you should provide a recipe for how to make it. Be brief in writing up the recipe. For each meal they cannot make, you need to explain why, meaning which ingredients they are missing. Be brief with the reason as well. You should never put a meal into both the possible and impossible lists."},
        {"role": "user", "content": what_can_i_make_prompt + "Which meals can I make, and what is the recipe for each?\n"
         "Return a json object that looks like {\"possible meals\": [ {\"name\": <meal name>, \"recipe\": <recipe>} ], \"impossible meals\": [ {\"name\": <meal name>, \"reason\": <reason>} ] } "}
    ],
    max_tokens=500,
    temperature=0.8,
    response_format={ "type": "json_object" },
)

content = completion.choices[0].message.content

print("\nFinish reason: " + completion.choices[0].finish_reason)
print("Usage: " + str(completion.usage) + "\n")

# Parse the string to a JSON (dictionary) object
parsed_json = json.loads(content)

possible_meals = parsed_json["possible meals"]
print("Here are the meals you can make:\n")
for index, meal in enumerate(possible_meals, start=1):
    print(f"{index}. {meal['name']}\n{meal['recipe']}\n ")

impossible_meals = parsed_json["impossible meals"]
print("Here are the meals you cannot make:\n")
for index, meal in enumerate(impossible_meals, start=1):
    print(f"{index}. {meal['name']}\n{meal['reason']}\n ")
