import streamlit as st
import re
from app import search_recipes

# Set page configuration
st.set_page_config(
    page_title="OptiMeal Dashboard",
    page_icon="🍽️",
    layout="wide"
)

def load_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Outfit', sans-serif;
        }
        
        .header-container {
            background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%);
            padding: 2.5rem;
            border-radius: 20px;
            text-align: center;
            color: white;
            box-shadow: 0 10px 25px rgba(255, 107, 107, 0.3);
            margin-bottom: 2rem;
        }
        
        .header-title {
            font-size: 3.5rem !important;
            font-weight: 800 !important;
            margin: 0 !important;
            letter-spacing: 1px;
            color: white !important;
        }
        
        .header-subtitle {
            font-size: 1.2rem;
            font-weight: 300;
            margin-top: 5px;
            opacity: 0.9;
        }
        
        h2 {
            color: #FF6B6B !important;
            border-bottom: 2px solid #FF8E53;
            padding-bottom: 0.5rem;
            margin-top: 1rem;
        }
        
        h3, h4 {
            color: #FF8E53 !important;
            font-weight: 600 !important;
        }
        
        .stTextInput > div > div > input {
            border-radius: 12px;
            border: 2px solid #ffe885;
            padding: 10px 15px;
            font-size: 1.1rem;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #FF6B6B;
            box-shadow: 0 0 10px rgba(255, 107, 107, 0.2);
        }
        
        strong {
            color: #FF6B6B;
            background-color: #fff0ec;
            padding: 2px 6px;
            border-radius: 4px;
        }
        </style>
    """, unsafe_allow_html=True)

def main():
    load_css()
    
    st.markdown('''
        <div class="header-container">
            <h1 class="header-title">🍽️ OptiMeal</h1>
            <p class="header-subtitle">Your Smart, Dynamic, & Beautiful Chef</p>
        </div>
    ''', unsafe_allow_html=True)
    
    st.write("Enter the ingredients you have on hand, and we'll dynamically search our robust recipe datasets!")
    
    st.markdown("---")
    
    # User Input Section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        user_input = st.text_input(
            "What's in your fridge or pantry?", 
            placeholder='e.g., "chicken, garlic, spinach"',
            help="Type your ingredients separated by commas."
        )
        
    with col2:
        meal_type = st.radio(
            "Select Meal Type:",
            ("Any", "Breakfast", "Lunch", "Dinner")
        )
    
    if user_input:
        with st.spinner(f"Searching datasets for {meal_type.lower() if meal_type != 'Any' else 'the best'} recipes..."):
            suggested_recipes = search_recipes(user_input, meal_type)
        
        if not suggested_recipes:
            st.warning("No recipes found matching those ingredients. Try keeping it simple, e.g. 'chicken, pasta'.")
        else:
            st.success(f"Found {len(suggested_recipes)} recipe(s) based on your ingredients!")
            
            # Interactive Selection
            st.markdown("### Suggested Dishes")
            
            # Limit suggestions to top 10
            dish_names = [recipe["name"] for recipe in suggested_recipes[:10]]
            
            selected_dish_name = st.selectbox(
                "Select a dish to view its recipe:",
                options=dish_names
            )
            
            # Find the selected recipe dictionary
            selected_recipe = next((r for r in suggested_recipes if r["name"] == selected_dish_name), None)
            
            if selected_recipe:
                st.markdown("---")
                
                # Recipe Details Display
                st.markdown(f"## {selected_recipe['name']}")
                
                # Use columns for layout
                det_col1, det_col2 = st.columns([1, 2])
                
                with det_col1:
                    # Render Thumbnail if it exists
                    if selected_recipe.get("thumb"):
                        st.image(selected_recipe["thumb"], use_container_width=True)
                    
                    st.markdown("#### 🛒 Ingredients")
                    for ing in selected_recipe["ingredients"]:
                        # Highlight matching ingredients by bolding
                        user_ing_set = {u_ing.strip().lower() for u_ing in user_input.split(",") if u_ing.strip()}
                        matched = any(u_ing in ing.lower() for u_ing in user_ing_set)
                        
                        if matched:
                            st.markdown(f"- **{ing.title()} (matched)**")
                        else:
                            st.markdown(f"- {ing.title()}")
                        
                    st.markdown("#### ⏱️ Prep Time")
                    st.markdown(f"**{selected_recipe['prep_time']}**")
                    
                with det_col2:
                    st.markdown("#### 👩‍🍳 Instructions")
                    instructions = selected_recipe["instructions"]
                    
                    # Handle varying line breaks or numbered lists
                    if "\n" in instructions:
                        instructions_list = instructions.split("\n")
                    else:
                        instructions_list = re.split(r'(?=\b\d+\.\s)', instructions)
                    
                    for step in instructions_list:
                        if step.strip():
                            st.markdown(f"{step.strip()}")

if __name__ == "__main__":
    main()
