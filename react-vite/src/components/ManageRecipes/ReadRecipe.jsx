import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import logo from "../../../public/reciprocity_logo.png";
import "./ReadRecipe.css";

const RecipeDetails = () => {
  const { id } = useParams(); // Retrieve the recipe ID from the route parameters
  const [recipe, setRecipe] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const [currentImageIndex, setCurrentImageIndex] = useState(0);
  // const [isModalOpen, setIsModalOpen] = useState(false);

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

  const handleNextImage = () => {
    setCurrentImageIndex((prevIndex) =>
      prevIndex === recipe.images.length - 1 ? 0 : prevIndex + 1
    );
  };

  const handlePreviousImage = () => {
    setCurrentImageIndex((prevIndex) =>
      prevIndex === 0 ? recipe.images.length - 1 : prevIndex - 1
    );
  };

  // const openModal = () => {
  //   setIsModalOpen(true);
  // };

  // const closeModal = () => {
  //   setIsModalOpen(false);
  // };

  if (loading) {
    return <img src={logo} alt="Loading..." className="logo-spinner" />;
  }

  if (error) return <div className="error">{error}</div>;

  return (
    <div className="recipe-details-container">
      <div>
        {recipe ? (
          <div className="recipe-info">
            <h2 className="recipe-name">{recipe.name}</h2>
            <span className="detail-main">
              <div className="left-side">
                <div className="image-slider">
                  <button className="prev-button" onClick={handlePreviousImage}>
                    &#60;
                  </button>
                  <div className="image-container">
                    <img
                      src={recipe.images[currentImageIndex].image_url}
                      alt={`Recipe image ${currentImageIndex + 1}`}
                    />
                  </div>
                  <button className="next-button" onClick={handleNextImage}>
                    &#62;
                  </button>
                </div>

                <div className="recipe-highlights">
                  <p>
                    <em>Created by: {recipe.owner}</em>
                  </p>
                  <hr />
                  <p>
                    <strong>Cuisine:</strong> {recipe.cuisine}
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
                </div>
              </div>

              <div className="right-side">
                <h3>Description</h3>
                <p>{recipe.description}</p>
                <h3>Ingredients</h3>
                <ul className="ingredients-list">
                  {recipe.ingredients.map((item, index) => (
                    <li key={index}>{item.ingredient}</li>
                  ))}
                </ul>

                <h3>Instructions</h3>
                <ol className="instructions-list">
                  {recipe.instructions.map((step, index) => (
                    <li key={index}>{step.instruction}</li>
                  ))}
                </ol>
              </div>
            </span>
          </div>
        ) : (
          <p>Recipe not found.</p>
        )}
      </div>

      {/* Modal for image viewer
      {isModalOpen && (
        <div className="modal" onClick={closeModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <img
              src={recipe.images[currentImageIndex].image_url}
              alt={`Expanded Recipe image ${currentImageIndex + 1}`}
              className="expanded-image"
            />
            <button className="close-modal" onClick={closeModal}>
              &times; Close
            </button>
          </div>
        </div>
      )} */}
    </div>
  );
};

export default RecipeDetails;
