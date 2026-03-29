# 🍽️ OptiMeal

**Your Smart, Dynamic, & Beautiful Chef**

OptiMeal is a dynamic, Streamlit-based web application that helps you decide what to cook based on the ingredients you already have. By searching through localized recipe datasets (including Pakistani and Indian cuisines), it provides personalized, ranked recipe recommendations to reduce food waste and make cooking easier.

## ✨ Features
- **Smart Ingredient Matching:** Input what's in your fridge, and OptiMeal finds the best matching recipes.
- **Meal Type Filtering:** Filter recommendations by Breakfast, Lunch, Dinner, or Any.
- **Localized Datasets:** Integrates authentic Pakistani and Indian recipe datasets for diverse and realistic meal options.
- **Beautiful UI:** A vibrant, responsive, and interactive Streamlit interface with custom styling.
- **Detailed Instructions:** View required ingredients, prep time, and step-by-step cooking instructions directly in the app.

## 🛠️ Tech Stack
- **Python:** Core programming language.
- **Streamlit:** Frontend framework for the interactive web dashboard.
- **Pandas:** Used for efficient dataset loading, parsing, and filtering.

## 🚀 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/optimeal.git
   cd optimeal
   ```

2. **Install dependencies:**
   Make sure you have Python installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run dashboard.py
   ```

4. **Open your browser:**
   Navigate to `http://localhost:8501` to start using OptiMeal!

## 📁 Project Structure
- `dashboard.py`: The main Streamlit frontend application containing UI components and styling.
- `app.py`: The backend logic for loading datasets and implementing the recipe search/ranking algorithm.
- `requirements.txt`: Python package dependencies.
- `pakistani_food_recipes_dataset_full.csv` & `indian_food.csv`: Local recipe datasets (ensure these are in your root directory).
