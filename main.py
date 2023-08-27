from dataclasses import dataclass

import numpy as np
import matplotlib.pyplot as plt
import requests

CALORIE_LIMIT = float(input("Enter your calorie limit")) #cals
SUGAR_LIMIT = float(input("Enter your sugar limit (g)")) #grams
PROTEIN_GOAL = float(input("Enter your protein goal (g)")) #grams

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

        one_goal = False

        if calories_sum <= CALORIE_LIMIT and protein_sum >= PROTEIN_GOAL and  sugar_sum <= SUGAR_LIMIT:
            print("Good Job! All food goal met today.")
        else:
            if calories_sum < CALORIE_LIMIT:
                one_goal = True
                print("Calorie goal achieved")
            if protein_sum >= PROTEIN_GOAL:
                one_goal = True
                print("Protein goal achieved")
            if sugar_sum <= SUGAR_LIMIT:
                one_goal = True
                print("Sugar goal achieved")
            if not one_goal:
                print("No food goals achieved today")

        #Graphs section
        fig, axs = plt.subplots(2,2)

        axs[0,0].pie([protein_sum, fat_sum, carb_sum, sugar_sum], labels=["Protein", "Fat", "Carbs", "Sugar"])
        axs[0,0].set_title("Food Distribution")
        axs[0,1].plot(list(range(len(today))), np.cumsum([food.calories for food in today]), label="Calories Eaten")
        axs[0,1].plot(list(range(len(today))), [CALORIE_LIMIT] * len(today), label="Calorie Limit")
        axs[0, 1].legend()
        axs[0, 1].set_title("Calorie Limit Progress")
        axs[1,1].plot(list(range(len(today))), np.cumsum([food.sugar for food in today]), label = "Sugar Eaten")
        axs[1,1].plot(list(range(len(today))), [SUGAR_LIMIT] * len(today), label = "Sugar Limit")
        axs[1,1].legend()
        axs[1,1].set_title("Sugar Limit Progress")
        axs[1, 0].plot(list(range(len(today))), np.cumsum([food.protein for food in today]),label = "Protein Eaten")
        axs[1, 0].plot(list(range(len(today))), [PROTEIN_GOAL] * len(today), label = "Protein Goal")
        axs[1, 0].legend()
        axs[1, 0].set_title("Protein Goal Progress")

        fig.tight_layout()
        plt.show()

    elif choice == "q":
        break
    else:
        print("Invalid")