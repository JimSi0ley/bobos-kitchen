from functions import connect_to_db


def add_recipe(title, category, cook_time, ingredients, instructions, rating, favorite):
    connection, cursor = connect_to_db()

    cursor.execute("""
        INSERT INTO recipes
        (title, category, cook_time, ingredients, instructions, rating, favorite)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (title, category, cook_time, ingredients, instructions, rating, favorite))

    new_recipe_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return new_recipe_id

def get_recipe(recipe_id):
    connection, cursor = connect_to_db()

    cursor.execute("""
        SELECT *
        FROM recipes
        WHERE id = ?
    """, (recipe_id,))

    recipe = cursor.fetchone()

    connection.close()

    return recipe

def delete_recipe(recipe_id):
    connection, cursor = connect_to_db()

    cursor.execute("""
        DELETE FROM recipes
        WHERE id = ?
    """, (recipe_id,))

    deleted = cursor.rowcount > 0

    connection.commit()
    connection.close()

    return deleted

def update_recipe(recipe_id, new_title, new_category, new_cook_time, new_ingredients, new_instructions, new_rating):
    connection, cursor = connect_to_db()

    cursor.execute("""UPDATE recipes
                    SET title = ?, category = ?, cook_time = ?, ingredients = ?, instructions = ?, rating=?
                    WHERE id = ?""",
                   (new_title, new_category, new_cook_time, new_ingredients, new_instructions, new_rating, recipe_id)
                   )

    connection.commit()

    updated = cursor.rowcount > 0

    connection.close()

    return updated


def search_recipe(keyword):
    sql_keyword = f"%{keyword}%"

    connection, cursor = connect_to_db()

    cursor.execute("SELECT * FROM recipes WHERE title LIKE ?  OR ingredients LIKE ? OR Category LIKE ? OR instructions LIKE ?", (sql_keyword, sql_keyword, sql_keyword,sql_keyword))

    recipes = cursor.fetchall()

    connection.close()

    return recipes


def get_all_recipes(sort_by="title_asc"):
    connection, cursor = connect_to_db()

    sort_options = {
        "title_asc": "title ASC",
        "title_desc": "title DESC",
        "category": "category ASC, title ASC",
        "cook_time_asc": "cook_time ASC",
        "cook_time_desc": "cook_time DESC",
        "rating_desc": "rating DESC, title ASC",
        "rating_asc": "rating ASC, title ASC",
        "newest": "id DESC",
        "oldest": "id ASC"
    }

    order_by = sort_options.get(sort_by, "title ASC")

    cursor.execute(f"""
        SELECT *
        FROM recipes
        ORDER BY {order_by}
    """)

    recipes = cursor.fetchall()

    connection.close()

    return recipes

def get_recipes_by_category(category):
    connection, cursor = connect_to_db()

    cursor.execute("""
        SELECT *
        FROM recipes
        WHERE category = ?
        ORDER BY title
    """, (category,))

    recipes = cursor.fetchall()

    connection.close()

    return recipes

def toggle_favorite(recipe_id):
    connection, cursor = connect_to_db()

    cursor.execute("""
        UPDATE recipes
        SET favorite = CASE
            WHEN favorite = 0 THEN 1
            ELSE 0
        END
        WHERE id = ?
    """, (recipe_id,))

    connection.commit()
    connection.close()


def get_favorite_recipes():
    connection, cursor = connect_to_db()

    cursor.execute("""
        SELECT *
        FROM recipes
        WHERE favorite = 1
        ORDER BY title ASC
    """)

    recipes = cursor.fetchall()

    connection.close()

    return recipes

def get_random_recipe():
    connection, cursor = connect_to_db()

    cursor.execute("""
        SELECT *
        FROM recipes
        ORDER BY RANDOM()
        LIMIT 1
    """)

    recipe = cursor.fetchone()

    connection.close()

    return recipe

def update_recipe_photo(recipe_id, photo_filename):
    connection, cursor = connect_to_db()

    cursor.execute("""
        UPDATE recipes
        SET photo_filename = ?
        WHERE id = ?
    """, (photo_filename, recipe_id))

    connection.commit()
    connection.close()
