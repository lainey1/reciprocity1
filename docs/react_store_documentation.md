## React Store Documentation

### Store Structure

```javascript
{
  user: {
    isAuthenticated: false,
    details: { id: 1, name: 'Jane Doe' },
  },
  recipes: {
    all: [],
    current: { id: 1, title: 'Spaghetti', ingredients: ['Pasta', 'Tomato Sauce'] },
  },
  collections: {
    all: [],
    current: { id: 5, title: 'Italian Favorites', recipes: [1, 2, 3] },
  },
}
```

### Actions and Reducers

1. Recipes Slice
   - `fetchRecipes`: Fetches all recipes from the API.
   - `addRecipe`: Adds a new recipe to the state.
   - `updateRecipe`: Updates an existing recipe in the state.

### Example Flows

- User clicks "Save Recipe" -> addRecipe action dispatched.
- Reducer updates the recipes.all array with the new recipe.
- React component re-renders with the updated list.
