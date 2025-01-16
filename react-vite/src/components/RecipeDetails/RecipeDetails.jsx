import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import logo from "../../../public/reciprocity_logo.png";
import "./RecipeDetails.css";

const RecipeDetails = () => {
  const { id } = useParams(); // Retrieve the recipe ID from the route parameters
  const [recipe, setRecipe] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchRecipe = async () => {
      try {
        const response = await fetch(`/api/recipes/${id}`);
        if (!response.ok) {
          throw new Error("Failed to fetch the recipe.");
        }
        const data = await response.json();
        setRecipe(data.recipe);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchRecipe();
  }, [id]);

  //   if (loading) return <div className="spinner"></div>;
  if (loading) {
    return <img src={logo} alt="Loading..." className="logo-spinner" />;
  }

  if (error) return <div className="error">{error}</div>;

  return (
    <div className="page-container">
      <div className="recipe-details">
        {recipe ? (
          <>
            <h2>{recipe.name}</h2>
            <p>
              <strong>Created by:</strong> {recipe.owner}
            </p>
            <p>
              <strong>Cuisine:</strong> {recipe.cuisine}
            </p>
            <p>
              <strong>Description:</strong> {recipe.description}
            </p>
            <p>
              <strong>Yield:</strong> {recipe.yield_servings} servings
            </p>
            <p>
              <strong>Prep Time:</strong> {recipe.prep_time} minutes
            </p>
            <p>
              <strong>Cook Time:</strong> {recipe.cook_time} minutes
            </p>
            <p>
              <strong>Total Time:</strong> {recipe.total_time} minutes
            </p>
            {recipe.tags && (
              <p>
                <strong>Tags:</strong> {recipe.tags}
              </p>
            )}
            {recipe.preview_image && (
              <img
                src={recipe.preview_image}
                alt={`${recipe.name} preview`}
                className="recipe-preview"
              />
            )}
            <h2>Ingredients</h2>
            <ul>
              {recipe.ingredients.map((item, index) => (
                <li key={index}>{item.ingredient}</li>
              ))}
            </ul>
            <h2>Instructions</h2>
            <ol>
              {recipe.instructions.map((step, index) => (
                <li key={index}>{step.instruction}</li>
              ))}
            </ol>
          </>
        ) : (
          <p>Recipe not found.</p>
        )}
      </div>
    </div>
  );
};

export default RecipeDetails;
