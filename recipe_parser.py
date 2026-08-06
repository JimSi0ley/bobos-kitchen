import os

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field


# Load variables from the project's .env file.
load_dotenv()


class ParsedRecipe(BaseModel):
    """
    Describes the exact recipe fields that the AI must return.
    """

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


def parse_recipe(ocr_text):
    """
    Convert disorganized OCR text into structured recipe information.

    Args:
        ocr_text: Raw OCR text from one or more recipe pages.

    Returns:
        A ParsedRecipe object containing the organized recipe fields.
    """

    if not ocr_text or not ocr_text.strip():
        raise ValueError("No OCR text was provided.")

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY was not found. Check the project's .env file."
        )

    client = OpenAI(api_key=api_key)

    response = client.responses.parse(
        model="gpt-5",
        instructions=(
            "You organize OCR text extracted from printed recipes. "
            "The OCR may contain words in the wrong order, broken lines, "
            "duplicate fragments, website addresses, author information, "
            "advertisements, headers, footers, or recognition errors. "
            "\n\n"
            "Extract only the actual recipe. Reconstruct its intended "
            "reading order using headings, quantities, step numbers, and "
            "context. Remove obvious website navigation, author biographies, "
            "URLs, advertisements, and unrelated page content. "
            "\n\n"
            "Do not invent missing ingredients, quantities, temperatures, "
            "or instructions. Correct obvious OCR spelling errors only when "
            "the intended word is clear from context. "
            "\n\n"
            "For cook time, use the active Cook Time when explicitly given. "
            "Do not use total time, freezing time, chilling time, or prep time "
            "as the cook time. If no active cook time can be determined, "
            "return 0 hours and 0 minutes."
        ),
        input=(
            "Organize the following raw OCR text into a recipe:\n\n"
            f"{ocr_text}"
        ),
        text_format=ParsedRecipe
    )

    parsed_recipe = response.output_parsed

    if parsed_recipe is None:
        raise ValueError(
            "The AI did not return a structured recipe."
        )

    return parsed_recipe
