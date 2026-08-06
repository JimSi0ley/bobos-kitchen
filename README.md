# 🍳 BoBo's Kitchen

A web-based digital cookbook designed to preserve and organize family recipes.

BoBo's Kitchen allows recipes to be entered manually or imported directly from photographs. Using OCR (Optical Character Recognition) and the OpenAI API, the application extracts recipe information from one or more images, intelligently organizes the content, and stores it in a searchable SQL database.

This project was created for my father to preserve his growing recipe collection while also serving as a real-world software engineering project that combines Python, SQL, AI, OCR, authentication, and web development.

---

# Features

### Recipe Management

- Add recipes manually
- Edit existing recipes
- Delete recipes
- Organize recipes by category
- Recipe ratings
- Favorite recipes
- Store cook times

### AI Recipe Import

- Import one or more recipe photos
- OCR extracts text from each page
- OpenAI organizes the extracted text into:
  - Recipe title
  - Category
  - Cook time
  - Ingredients
  - Instructions
- Automatically populates the Add Recipe form for review before saving

### Photo Management

- Upload recipe photos
- Replace existing photos
- Remove photos
- Display recipe images throughout the application

### Search & Discovery

- Search recipes
- Browse favorite recipes
- Random "Surprise Me" recipe selection

### Authentication

- Secure administrator login
- Password hashing
- Protected administrative routes
- Public read-only recipe browsing

---

# Technologies Used

### Backend

- Python
- Flask
- SQLite

### AI & OCR

- OpenAI API
- EasyOCR
- OpenCV

### Frontend

- HTML
- CSS
- Jinja2 Templates

### Security

- Flask-Login
- Werkzeug Password Hashing
- Environment Variables (.env)

---

# Screenshots

(Add screenshots here after deployment.)

---

# Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/bobos-kitchen.git
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file using `.env.example`

Run the application

```bash
python app.py
```

---

# Environment Variables

Create a `.env` file containing:

```
FLASK_SECRET_KEY=
OPENAI_API_KEY=
ADMIN_USERNAME=
ADMIN_PASSWORD_HASH=
```

---

# Future Enhancements

- AI recipe generation
- Ingredient scaling
- Nutrition information
- Shopping list generation
- Meal planning
- User accounts
- Cloud photo storage
- Mobile-friendly improvements

---

# Author

**James Sibley**

Bachelor of Science — Cybersecurity and Information Assurance

Western Governors University

---

# License

This project is licensed under the MIT License.
