from recipe_parser import parse_recipe


ocr_text = """
Cheesesteaks

served in

well-marbled steak, sauteed onions, and

provolone cheese

a soft but

hoagie roll define this classic Philly sandwich:

Leah Colins

Updated on September 26,2025

Time: 25 mins

Cook Time: 15 mins

Freezing: 1 hr

Total Time: 1 hr 40 mins

Servings: 2

Ingredients

1

pound (454 g) boneless rib eye steak or skirt steak or store-bought

pre-sliced rib eye (see notes)

1

tablespoon (15 ml) vegetable

or other neutral oil

1/2 medium yellow onion (4 ounces; 114 g), cut into 1/4-inch dice

8 thin slices provolone cheese (about 6 ounces; 160 g), 4 slices torn into

1-inch pieces and 4 slices left whole

2 tablespoons grated Parmigiano-Reggiano cheese (optional)

1

teaspoon Diamond Crystal kosher salt; for table salt use half as much

by volume

1/8 teaspoon freshly ground black pepper

Two 7- to 8-inch-long Italian hoagie/sub rolls, split lengthwise, but left

attached on 1 side to create a hinge

Directions

Step 1

If using a whole steak; trim and cut steak crosswise with

into roughly

3-inch wide sections, then set on large plate

and freeze until firm but not

solid, about 1 hour. If using

pre-sliced steak, skip to chopping

instructions in Step 2.

Step 2

Using a sharp knife, shave steak as thin as

possible on a biased angle.

Mound shaved meat

on cutting board and chop coarse

with knife, about 5 times for store-bought

sliced meat or 10 times for

hand-sliced.

Step 3

Heat an empty

12-inch cast-iron skillet over

medium-high heat for 5

minutes. Add oil to skillet and

heat until just smoking. Add meat and onion

in an even layer

and cook, without stirring, until well

browned on one side,

4 to 6 minutes. Continue to

cook, stirring frequently to move and pull apart

the slices until meat and

onions are browned and meat is no longer

pink,

2 to 4 minutes.

Step 4

Stir in

torn provolone cheese, Parmesan cheese if using, salt, and pepper.

Cook, stirring constantly, until cheese is melted and well combined,

1 to 2 minutes. Turn

off heat.

Divide mixture into 2 individual portions the length

of the rolls. Shingle 2 slices of provolone cheese over each portion. Cover

and let cheese melt, about 1 minute.

Step 5

Center rolls, cut sides down, over each portion of

meat.

Working with one

at a time, use a

large spatula to

scoop under each portion of meat and flip

meat into roll to create

a filled sandwich. Serve

immediately.
"""


try:
    recipe = parse_recipe(ocr_text)

    print("\n==============================")
    print("PARSED RECIPE")
    print("==============================")

    print(f"\nTitle:\n{recipe.title}")

    print(f"\nCategory:\n{recipe.category}")

    print(
        f"\nCook Time:\n"
        f"{recipe.cook_hours} hours, "
        f"{recipe.cook_minutes} minutes"
    )

    print(f"\nIngredients:\n{recipe.ingredients}")

    print(f"\nInstructions:\n{recipe.instructions}")

except Exception as error:
    print("\nThe recipe could not be parsed.")
    print(f"Error: {error}")
