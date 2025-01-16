// action types
const SET_RECIPES = "recipes/setRecipes";
const SET_RECIPE = "recipes/setRecipe";
const ADD_RECIPE = "recipes/addRecipe";
const SET_LOADING = "recipes/setLoading";
const SET_ERRORS = "recipes/setError";

// action creators
const setRecipes = (recipes) => ({
  type: SET_RECIPES,
  payload: recipes,
});

const setRecipe = (recipe) => ({
  type: SET_RECIPE,
  payload: recipe,
});

const addRecipe = (recipe) => ({
  type: ADD_RECIPE,
  payload: recipe,
});

const setLoading = (loading) => ({
  type: SET_LOADING,
  payload: loading,
});

const setErrors = (error) => ({
  type: SET_ERRORS,
  payload: error,
});

// Thunks (for async actions like fetching recipes)
export const thunkFetchRecipes = () => async (dispatch) => {
  dispatch(setLoading(true));

  try {
    const response = await fetch("/api/recipes");

    if (!response.ok) {
      throw new Error("Failed to fetch recipes");
    }

    const data = await response.json();
    dispatch(setRecipes(data));
    dispatch(setLoading(false));
  } catch (error) {
    dispatch(setErrors(error.message));
    dispatch(setLoading(false));
  }
};

export const thunkFetchRecipeById = (id) => async (dispatch) => {
  dispatch(setLoading(true));

  try {
    const response = await fetch(`/api/recipes/${id}`);

    if (!response.ok) {
      throw new Error("Failed to fetch recipe");
    }

    const data = await response.json();
    console.log(data);
    dispatch(setRecipe(data.recipe));
    dispatch(setLoading(false));
  } catch (error) {
    dispatch(setErrors(error.message));
    dispatch(setLoading(false));
  }
};

export const thunkCreateRecipe = (recipeData) => async (dispatch) => {
  dispatch(setLoading(true));

  try {
    const response = await fetch("/api/recipes/new", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(recipeData),
    });
    // console.log("RESPONSE=======>", response);

    if (response.ok) {
      const data = await response.json();
      console.log("DATA=======>", data);
      dispatch(addRecipe(data)); // Dispatch action to update store with new recipe
      // console.log("DATA RESPONSE=======>", response);
      return data.recipe;
    } else {
      const errors = await response.json();
      dispatch(setErrors(errors)); // Dispatch errors if creation failed
    }
  } catch (err) {
    console.error("Error creating recipe:", err);
    dispatch(setErrors({ message: "Error submitting form" }));
  }
  dispatch(setLoading(false));
};

// initial state
const initialState = {
  loading: false,
  error: null,
};

// reducer
function recipesReducer(state = initialState, { type, payload }) {
  switch (type) {
    case SET_RECIPES:
      return { ...state, recipes: payload };
    case SET_RECIPE:
      return { ...state, recipe: payload, error: null };
    case ADD_RECIPE:
      return {
        ...state,
        recipes: [...(state.recipes || []), payload],
        error: null,
      };
    case SET_LOADING:
      return { ...state, loading: payload };
    case SET_ERRORS:
      return { ...state, error: payload };
    default:
      return state;
  }
}

export default recipesReducer;
