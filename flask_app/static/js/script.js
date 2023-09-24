function search() {
    let searchInput = document.getElementById('searchInput');
    let allRecipes = document.getElementById('all_recipes');
    let recipes = Array.from(allRecipes.getElementsByClassName('one_recipe'));
    let searchTerm = searchInput.value.toLowerCase();
    recipes.forEach(function(recipe) {
        let text = recipe.querySelector('.recipe_name').textContent.toLowerCase();
        if(text.includes(searchTerm)) {
            recipe.style.removeProperty('display');
        }
        else {
            recipe.style.display = 'none';
        }
    });
}

function sendToPage() {
    window.open("https://www.vecteezy.com/free-png/kawaii-food");
}