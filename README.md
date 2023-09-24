# RecipeShare 🥘

RecipeShare is a recipe sharing platform where people can search for recipes and post their own recipes. 

Users can:
- 🔍 search for a recipe
- ➕ create a recipe
- 👀 view others' recipes
- ✏️ edit & delete recipes they created

In this project I:
- Employed Python and MySQL to handle back-end functionalities, including recipe and user CRUD operations
- Utilized Flask and JavaScript to elevate user experience by implementing validation error notifications and enabling recipe search functionality
- Harnessed HTML, CSS, and Bootstrap to craft an adaptive front-end design
  
<img width="1440" alt="all_recipes" src="https://github.com/yuzuha48/RecipeShare/assets/106595505/7e153f16-278e-4146-9340-abbe852466f2">
<img width="1440" alt="create_recipe" src="https://github.com/yuzuha48/RecipeShare/assets/106595505/07d7b07e-f908-46a4-bc22-4aed36e583b1">
<img width="1440" alt="recipe" src="https://github.com/yuzuha48/RecipeShare/assets/106595505/6cdee36c-b455-4d12-9d51-45deb87c1896">
<img width="1440" alt="recipe_2" src="https://github.com/yuzuha48/RecipeShare/assets/106595505/2e1c9f2e-a591-4a70-a0bb-d25e674559a5">

## Prerequisites

Ensure you have the following software installed on your machine:
- Python (version 3.6 or higher)
- pip (Python package installer)
- pipenv (Python package manager)

## Getting Started 

To get started with WanderGuide, follow these steps: 
1. Clone this repository to your local machine:
   - git clone https://github.com/yuzuha48/RecipeShare
2. Navigate to the project directory:
   ```
   cd RecipeShare
   ```
3. Install the required dependencies using pipenv:
   ```
   pipenv install
   ```
4. Activate the virtual environment:
   ```
   pipenv shell
   ```
5. Modify the database connection configurations in:
   `flask_app/config/mysqlconnection.py`
6. Start RecipeShare by running the following command:
     ```
     python3 server.py
     ```
7. Open a web browser and visit `http://localhost:5001` to view the running app. 
