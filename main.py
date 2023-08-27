from dataclasses import dataclass

import numpy as np
import matplotlib.pyplot as plt
import requests

CALORIE_LIMIT = 2500 #cals
PROTEIN_GOAL = 150 #grams

today = []

@dataclass
class Food:
    name: str
    calories: float
    protein: float
    fat: float
    carbs: float
    sugar: float

done = False

while not done:
    print("""
    1. Add food
    2. See progress
    q. quit
    """)

    choice = input("Choose an option: ")

    if choice == "1":
        #communicate with the nutrition API
        query = input("Enter the amount and name of food (Ex. 300g grilled chicken")
        api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(query)
        response = requests.get(api_url,
                                headers = {'X-Api-Key': '3afaUHCxrorrBRQPqEz0nQ==qoRehIlN72mFMyUv'})
        if response.status_code == requests.codes.ok:
            data_list = response.json()
            if data_list and isinstance(data_list, list):
                data = data_list[0]
                print(data["calories"])
                food = Food(data["name"], data["calories"], data["protein_g"], data["fat_total_g"], data["carbohydrates_total_g"], data["sugar_g"])
                today.append(food)
                print("Success! Added " + query)
        else:
            print("Error:", response.status_code, response.text)

    elif choice == "2":
        calories_sum = sum(food.calories for food in today)
        protein_sum = sum(food.protein for food in today)
        fat_sum = sum(food.fat for food in today)
        carb_sum = sum(food.carbs for food in today)
        sugar_sum = sum(food.sugar for food in today)

        if calories_sum <= CALORIE_LIMIT and protein_sum >= PROTEIN_GOAL:
            print("Good Job! All food goal met today.")
        elif calories_sum < CALORIE_LIMIT:
            print("Calorie goal achieved")
        elif protein_sum >= PROTEIN_GOAL:
            print("Protein goal achieved")
        else:
            print("No food goals achieved today")

        #Graphs section
        fig, axs = plt.subplots(1,2)

        axs[0].pie([protein_sum, fat_sum, carb_sum, sugar_sum], labels=["Protein", "Fat", "Carbs", "Sugar"])
        axs[0].set_title("Food Distribution")
        axs[1].plot(list(range(len(today))), np.cumsum([food.calories for food in today]), label="Calories Eaten")
        axs[1].plot(list(range(len(today))), [CALORIE_LIMIT] * len(today), label="Calorie Limit")
        axs[1].legend()
        axs[1].set_title("Calories Limit Progress")

        fig.tight_layout()
        plt.show()

    elif choice == "q":
        break
    else:
        print("Invalid")