import sqlite3


def connect_to_db():
    connection = sqlite3.connect("recipes.db")
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    return connection, cursor







def display_recipes():
    connection, cursor = connect_to_db()

    cursor.execute("SELECT * FROM recipes")

    recipes = cursor.fetchall()

    print_recipes(recipes)

    connection.close()
    print("\n\n")

def delete_recipe():
    connection, cursor = connect_to_db()

    recipe_id= input("Enter recipe ID to delete: ")

    cursor.execute("DELETE FROM recipes WHERE ID = ?", (recipe_id,))

    connection.commit()
    connection.close()

    print("\n\n")

def update_recipe():
    connection, cursor = connect_to_db()


    recipe_id= input("Enter recipe ID to update: ")
    new_title = input("Enter new recipe title: ")
    new_category = input("Enter new recipe category: ")
    new_cook_time = input("Enter new recipe cook time: ")
    new_ingredients = input("Enter new ingredients: ")
    new_instructions = input("Enter new instructions: ")

    cursor.execute("""UPDATE recipes
                    SET title = ?, category = ?, cook_time = ?, ingredients = ?, instructions = ?
                    WHERE id = ?""",
                   (new_title, new_category, new_cook_time, new_ingredients, new_instructions, recipe_id)
                   )

    if cursor.rowcount == 0:
        print("No recipe found with that ID.")
    else:
        print("Recipe updated successfully!")

    print("\n\n")
    connection.commit()
    connection.close()

    print("\n\n")

    display_recipes()



def search_recipe():
    keyword = input("Enter keyword to search: ")
    sql_keyword = f"%{keyword}%"

    connection, cursor = connect_to_db()

    cursor.execute("SELECT * FROM recipes WHERE title LIKE ?  OR ingredients LIKE ? OR Category LIKE ? OR instructions LIKE ?", (sql_keyword, sql_keyword, sql_keyword,sql_keyword))

    recipes = cursor.fetchall()

    connection.close()

    print_recipes(recipes)


def print_recipes(recipes):
    if len(recipes) == 0:
        print("No recipe found with that keyword.")
    else:
        for recipe in recipes:
            print()
            print("================================")
            print()
            print(f"Recipe ID: {recipe[0]}")
            print()
            print(f"Title: \n {recipe[1]}")
            print()
            print(f"Category: \n {recipe[2]}")
            print()
            print(f"Cook Time: \n {recipe[3]}")
            print()
            print(f"Ingredients: \n {recipe[4]}")
            print()
            print(f"Instructions: \n {recipe[5]}")
            print()
            print("================================")
            print()
