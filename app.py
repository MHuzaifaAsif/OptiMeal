import streamlit as st
import pandas as pd
import os

@st.cache_data(show_spinner=False)
def load_and_combine_data():
    base_dir = r"c:\Users\Huzaifa's\Desktop\Projects\OptiMeal"
    
    # Load Nigerian/Pakistani/Indian datasets safely
    try:
        pak_df = pd.read_csv(os.path.join(base_dir, "pakistani_food_recipes_dataset_full.csv"))
    except FileNotFoundError:
        pak_df = pd.DataFrame()
        
    try:
        ind_df = pd.read_csv(os.path.join(base_dir, "indian_food.csv"))
    except FileNotFoundError:
        ind_df = pd.DataFrame()
    
    recipes = []
    
    # Parse Pakistani Dataset
    if not pak_df.empty:
        for _, row in pak_df.iterrows():
            recipes.append({
                "name": str(row.get("Recipe Name", "")),
                "ingredients": [x.strip() for x in str(row.get("Ingredients", "")).split(",")],
                "instructions": str(row.get("Steps", "Instructions not available.")),
                "prep_time": str(row.get("Prep Time", "Varies")),
                "meal_type": str(row.get("Meal Type", "")).strip(),
                "thumb": ""
            })
            
    # Parse Indian Dataset
    if not ind_df.empty:
        def map_indian_course(course):
            c = str(course).lower()
            if "dessert" in c: return "Dessert"
            if "main course" in c: return "Lunch, Dinner" # Indian main courses often work for both
            if "starter" in c or "snack" in c: return "Snack"
            return "Any"
            
        for _, row in ind_df.iterrows():
            p_time = str(row.get('prep_time', '-1'))
            prep_time_str = f"{p_time} mins" if p_time != "-1" else "Varies"
            
            recipes.append({
                "name": str(row.get("name", "")),
                "ingredients": [x.strip() for x in str(row.get("ingredients", "")).split(",")],
                "instructions": "Step-by-step instructions not provided in this dataset.",
                "prep_time": prep_time_str,
                "meal_type": map_indian_course(row.get("course", "")),
                "thumb": ""
            })
            
    return recipes

def search_recipes(user_ingredients, user_meal_type="Any"):
    """
    Searches combined local CSV datasets for matching recipes.
    """
    recipes_db = load_and_combine_data()
    
    if not user_ingredients:
        return []
    
    ingredients_list = [ing.strip().lower() for ing in user_ingredients.split(",") if ing.strip()]
    if not ingredients_list:
        return []
        
    user_ing_set = set(ingredients_list)
    ranked_recipes = []
    
    for recipe in recipes_db:
        # Filter by meal_type
        mt = recipe["meal_type"].lower()
        if user_meal_type != "Any":
            if user_meal_type == "Breakfast" and "breakfast" not in mt:
                continue
            if user_meal_type == "Lunch" and "lunch" not in mt:
                continue
            if user_meal_type == "Dinner" and "dinner" not in mt:
                continue
                
        # Check ingredient match count
        recipe_ing_names = set([ing.lower() for ing in recipe["ingredients"]])
        match_count = 0
        
        for u_ing in user_ing_set:
            if any(u_ing in r_ing for r_ing in recipe_ing_names):
                match_count += 1
                
        if match_count > 0:
            recipe_copy = dict(recipe)
            recipe_copy["match_count"] = match_count
            ranked_recipes.append(recipe_copy)
            
    # Sort descending by match_count
    ranked_recipes.sort(key=lambda x: x["match_count"], reverse=True)
    return ranked_recipes
