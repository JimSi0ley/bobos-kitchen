from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from database import create_database, add_favorite_column, add_photo_column, add_rating_column
from functions_web import add_recipe, get_recipe, get_all_recipes, delete_recipe, update_recipe, search_recipe, get_recipes_by_category, toggle_favorite, get_favorite_recipes, get_random_recipe, update_recipe_photo
from utils import format_cook_time
import os
from dotenv import load_dotenv
from recipe_parser import parse_recipe_images
from urllib.parse import urljoin, urlparse
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash

load_dotenv()

app = Flask(__name__)


app.config["SECRET_KEY"] = os.getenv(
    "FLASK_SECRET_KEY",
    "temporary-development-key"
)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"
login_manager.login_message = "Please log in to access that page."

class AdminUser(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

@login_manager.user_loader
def load_user(user_id):

    admin_username = os.getenv("ADMIN_USERNAME")

    if (
        admin_username
        and user_id.lower() == admin_username.lower()
    ):
        return AdminUser(admin_username)

    return None

def is_safe_redirect_url(target):
    if not target:
        return False

    host_url = urlparse(request.host_url)
    redirect_url = urlparse(
        urljoin(request.host_url, target)
    )

    return (
        redirect_url.scheme in ("http", "https")
        and redirect_url.netloc == host_url.netloc
    )

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        stored_password_hash = os.getenv("ADMIN_PASSWORD_HASH")

        if (
                username.lower() == os.getenv("ADMIN_USERNAME").lower()
                and
                stored_password_hash
                and
                check_password_hash(
                    stored_password_hash,
                    password
                )
        ):

            login_user(
                AdminUser(os.getenv("ADMIN_USERNAME"))
            )

            next_page = request.args.get("next")

            if is_safe_redirect_url(next_page):
                return redirect(next_page)

            return redirect(
                url_for("home")
            )
        return render_template(
            "login.html",
            error="Invalid username or password."
        )

    return render_template(
        "login.html",
        error=None
    )

@app.route("/logout")
@login_required
def logout():
    logout_user()

    return redirect(
        url_for("home")
    )

if os.getenv("RENDER"):
    UPLOAD_FOLDER = os.path.join(
        "/opt/render/project/src/storage",
        "uploads"
    )
else:
    UPLOAD_FOLDER = os.path.join(
        "static",
        "uploads"
    )

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "webp"
}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )

def save_recipe_photo(recipe_id, photo):
    existing_recipe = get_recipe(recipe_id)

    if not photo or not photo.filename:
        return None

    if not allowed_file(photo.filename):
        return None

    extension = photo.filename.rsplit(".", 1)[1].lower()

    filename = secure_filename(
        f"recipe_{recipe_id}.{extension}"
    )

    photo_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    if (
        existing_recipe
        and existing_recipe["photo_filename"]
        and existing_recipe["photo_filename"] != filename
    ):
        old_photo_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            existing_recipe["photo_filename"]
        )

        if os.path.exists(old_photo_path):
            os.remove(old_photo_path)

    photo.save(photo_path)

    update_recipe_photo(
        recipe_id,
        filename
    )

    return filename

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )

app.jinja_env.filters["format_cook_time"] = format_cook_time

create_database()
add_favorite_column()
add_photo_column()
add_rating_column()

@app.route("/")
def home():
    return render_template(
        "home.html",
        hide_nav=True
    )
@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        title = request.form["title"].strip().title()
        category = request.form["category"].strip().title()

        cook_hours = int(request.form.get("cook_hours", 0))
        cook_minutes = int(request.form.get("cook_minutes", 0))
        cook_time = cook_hours * 60 + cook_minutes

        ingredients = request.form["ingredients"]
        instructions = request.form["instructions"]
        rating = int(request.form.get("rating", 0))
        favorite = 1 if request.form.get("favorite") else 0

        new_recipe_id = add_recipe(
            title,
            category,
            cook_time,
            ingredients,
            instructions,
            rating,
            favorite
        )

        photo = request.files.get("photo")

        save_recipe_photo(
            new_recipe_id,
            photo
        )

        return redirect(
            url_for(
                "recipe_details",
                recipe_id=new_recipe_id
            )
        )

    return render_template(
            "add.html",
            imported_recipe=None,
            import_success=False
        )

@app.route("/recipe/<int:recipe_id>")
def recipe_details(recipe_id):
    recipe = get_recipe(recipe_id)

    if recipe is None:
        return "Recipe not found", 404

    return render_template(
        "recipe_details.html",
        recipe=recipe
    )

@app.route("/recipes")
def recipes():
    sort_by = request.args.get("sort", "title_asc")

    all_recipes = get_all_recipes(sort_by)

    return render_template(
        "recipes.html",
        recipes=all_recipes,
        page_heading="All Recipes",
        current_sort=sort_by,
        show_sort=True
    )

@app.route("/recipe/<int:recipe_id>/delete", methods=["POST"])
@login_required
def delete(recipe_id):

    recipe = get_recipe(recipe_id)

    deleted = delete_recipe(recipe_id)

    if recipe and recipe["photo_filename"]:

        photo_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            recipe["photo_filename"]
        )

        if os.path.exists(photo_path):
            os.remove(photo_path)

    if not deleted:
        return "Recipe not found", 404

    return redirect("/recipes")

@app.route("/recipe/<int:recipe_id>/edit", methods=["GET", "POST"])
@login_required
def edit_recipe(recipe_id):
    recipe = get_recipe(recipe_id)

    if recipe is None:
        return "Recipe not found", 404

    if request.method == "POST":
        new_title = request.form["title"].strip().title()
        new_category = request.form["category"].strip().title()

        cook_hours = int(request.form.get("cook_hours", 0))
        cook_minutes = int(request.form.get("cook_minutes", 0))

        new_cook_time = cook_hours * 60 + cook_minutes

        new_ingredients = request.form["ingredients"]
        new_instructions = request.form["instructions"]

        new_rating = int(request.form.get("rating", 0))

        update_recipe(
            recipe_id,
            new_title,
            new_category,
            new_cook_time,
            new_ingredients,
            new_instructions,
            new_rating
        )

        remove_photo = request.form.get("remove_photo")
        photo = request.files.get("photo")

        if remove_photo and recipe["photo_filename"]:
            old_photo_path = os.path.join(
                app.config["UPLOAD_FOLDER"],
                recipe["photo_filename"]
            )

            if os.path.exists(old_photo_path):
                os.remove(old_photo_path)

            update_recipe_photo(
                recipe_id,
                None
            )

        save_recipe_photo(
            recipe_id,
            photo
        )

        return redirect(f"/recipe/{recipe_id}")

    cook_hours, cook_minutes = divmod(int(recipe["cook_time"]), 60)

    return render_template(
        "edit_recipe.html",
        recipe=recipe,
        cook_hours=cook_hours,
        cook_minutes=cook_minutes
    )

@app.route("/search")
def search():
    keyword = request.args.get("keyword", "")

    if keyword:
        results = search_recipe(keyword)
    else:
        results = []

    return render_template(
        "search.html",
        recipes=results,
        keyword=keyword
    )

@app.route("/category/<category>")
def category_recipes(category):
    recipes = get_recipes_by_category(category)

    return render_template(
        "recipes.html",
        recipes=recipes,
        page_heading=category,
        show_sort=False
    )

@app.route("/recipe/<int:recipe_id>/favorite", methods=["POST"])
@login_required
def favorite(recipe_id):
    toggle_favorite(recipe_id)

    return redirect(request.referrer or url_for("recipes"))


@app.route("/favorites")
def favorites():
    favorite_recipes = get_favorite_recipes()

    return render_template(
        "recipes.html",
        recipes=favorite_recipes,
        page_heading="Favorite Recipes",
        show_sort=False
    )

@app.route("/random")
def random_recipe():
    recipe = get_random_recipe()

    if recipe is None:
        return redirect(url_for("recipes"))

    return redirect(
        url_for("recipe_details", recipe_id=recipe["id"])
    )

@app.route("/import", methods=["GET", "POST"])
@login_required
def import_recipe():

    if request.method == "POST":

        recipe_files = request.files.getlist("recipe_files")

        recipe_files = [
            recipe_file
            for recipe_file in recipe_files
            if recipe_file and recipe_file.filename
        ]

        if not recipe_files:
            return render_template(
                "import_recipe.html",
                extracted_text=None,
                extracted_pages=None,
                error="Please select at least one recipe image."
            )

        for page_number, recipe_file in enumerate(
            recipe_files,
            start=1
        ):
            filename = recipe_file.filename
            lowercase_filename = filename.lower()

            if not lowercase_filename.endswith(
                (".jpg", ".jpeg", ".png", ".webp")
            ):
                return render_template(
                    "import_recipe.html",
                    extracted_text=None,
                    extracted_pages=None,
                    error=(
                        f'"{filename}" is not a supported image format. '
                        "Please upload JPG, JPEG, PNG, or WEBP files."
                    )
                )

        try:
            parsed_recipe = parse_recipe_images(
                recipe_files
            )

        except ValueError as error:
            app.logger.exception(
                "Recipe image import failed: %s",
                error
            )

            return render_template(
                "import_recipe.html",
                extracted_text=None,
                extracted_pages=None,
                error=(
                    "BoBo's Kitchen could not read and organize those "
                    "recipe images. Make sure the pages are clear, upright, "
                    "and selected in the correct order."
                )
            )

        except Exception:
            app.logger.exception(
                "Unexpected recipe image import error."
            )

            return render_template(
                "import_recipe.html",
                extracted_text=None,
                extracted_pages=None,
                error=(
                    "The recipe import service is unavailable right now. "
                    "Please try again in a moment."
                )
            )

        return render_template(
            "add.html",
            imported_recipe=parsed_recipe,
            import_success=True
        )

    return render_template(
        "import_recipe.html",
        extracted_text=None,
        extracted_pages=None,
        error=None
    )

@app.errorhandler(404)
def page_not_found(error):
    return render_template(
        "404.html"
    ), 404

@app.errorhandler(403)
def forbidden(error):
    return render_template(
        "403.html"
    ), 403


@app.errorhandler(500)
def internal_server_error(error):
    app.logger.exception(
        "Unhandled server error: %s",
        error
    )

    return render_template(
        "500.html"
    ), 500


if __name__ == "__main__":
    app.run(debug=True)
