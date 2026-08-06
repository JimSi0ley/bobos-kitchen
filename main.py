from functions import add_recipe, display_recipes, delete_recipe, update_recipe, search_recipe
from database import create_database
def main():

    create_database()

    while True:
        print("Welcome to BoBo's Kitchen")
        print("1. Add Recipe")
        print("2. Display Recipes")
        print("3. Delete Recipe")
        print("4. Update Recipe")
        print("5. Search Recipes")
        print("6. Exit \n")


        user_choice = (input("Enter your choice: "))

        if user_choice == "1":
            add_recipe()


        elif user_choice == "2":
            display_recipes()


        elif user_choice == "3":
            delete_recipe()

        elif user_choice == "4":
            update_recipe()

        elif user_choice == "5":
            search_recipe()


        elif user_choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid choice!")

main()
