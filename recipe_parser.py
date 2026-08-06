import os
import base64

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field


load_dotenv()


class ParsedRecipe(BaseModel):

    title: str = Field(
        description="The recipe's title."
    )

    category: str = Field(
        description=(
            "A short, sensible recipe category such as Beef, Chicken, "
            "Pork, Seafood, Pasta, Soup, Dessert, Breakfast, or Other."
        )
    )

    cook_hours: int = Field(
        ge=0,
        description="The recipe's active cook time in whole hours."
    )

    cook_minutes: int = Field(
        ge=0,
        le=59,
        description="The remaining active cook time in minutes."
    )

    ingredients: str = Field(
        description=(
            "The complete ingredient list. Put each ingredient on its "
            "own line. Preserve quantities and units whenever possible."
        )
    )

    instructions: str = Field(
        description=(
            "The complete cooking instructions, organized into numbered "
            "steps. Preserve important temperatures and cooking times."
        )
    )


def parse_recipe_images(recipe_files):

    if not recipe_files:
        raise ValueError("No recipe images were provided.")

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY was not found."
        )

    client = OpenAI(api_key=api_key)

    content = [
        {
            "type": "input_text",
            "text": (
                "Read the attached recipe image or images. "
                "The images are supplied in page order. "
                "Extract and organize the recipe."
            )
        }
    ]

    for recipe_file in recipe_files:

        image_bytes = recipe_file.read()

        if not image_bytes:
            raise ValueError(
                f'"{recipe_file.filename}" is empty.'
            )

        extension = recipe_file.filename.rsplit(".", 1)[-1].lower()

        if extension == "jpg":
            extension = "jpeg"

        encoded_image = base64.b64encode(
            image_bytes
        ).decode("utf-8")

        content.append(
            {
                "type": "input_image",
                "image_url": (
                    f"data:image/{extension};base64,"
                    f"{encoded_image}"
                )
            }
        )

    response = client.responses.parse(
        model="gpt-5",
        instructions=(
            "You extract recipes from photographs, screenshots, "
            "scanned cookbook pages, and printed recipe pages. "

            "The user may provide multiple images belonging to one "
            "recipe. Treat them as consecutive pages in the order "
            "provided. "

            "Extract only the actual recipe. Ignore advertisements, "
            "website navigation, author biographies, URLs, headers, "
            "footers, and unrelated page content. "

            "Preserve ingredient quantities and units. Organize the "
            "instructions into numbered steps. "

            "Do not invent missing ingredients, quantities, "
            "temperatures, or instructions. "

            "For cook time, use the active Cook Time when explicitly "
            "given. Do not use total time, freezing time, chilling "
            "time, or prep time as cook time. If active cook time "
            "cannot be determined, return 0 hours and 0 minutes."
        ),
        input=[
            {
                "role": "user",
                "content": content
            }
        ],
        text_format=ParsedRecipe
    )

    parsed_recipe = response.output_parsed

    if parsed_recipe is None:
        raise ValueError(
            "The AI did not return a structured recipe."
        )

    return parsed_recipe
