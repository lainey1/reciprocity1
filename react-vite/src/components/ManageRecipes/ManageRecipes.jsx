import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate, Link } from "react-router-dom";
import { IoIosAdd } from "react-icons/io";
import { FaSave, FaEdit, FaShareAlt } from "react-icons/fa";

import no_image_available from "../../../public/no_image_available.png";
import OpenModalButton from "../OpenModalButton/OpenModalButton";
import { thunkFetchRecipes } from "../../redux/recipes";
import DeleteRecipeModal from "./DeleteRecipeModal";

import "./ManageRecipes.css";

function ManageRecipes() {
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const recipes = useSelector((state) => state.recipes.recipes);
  const currentUser = useSelector((state) => state.session.user);
  const recipesArr = Object.values(recipes);

  const userRecipes = recipesArr?.filter(
    (recipe) => recipe.owner_id == currentUser.id
  );

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [recipeToDelete, setRecipeToDelete] = useState(null);

  useEffect(() => {
    dispatch(thunkFetchRecipes());
  }, [dispatch]);

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setRecipeToDelete(null);
  };

  if (!currentUser) return <div>You must be logged in to manage recipes.</div>;

  return (
    <div className="page-container">
      <div>Created Recipes</div>
      <div id="manage-recipe-buttons">
        <button
          onClick={() => {
            navigate("/recipes/new");
          }}
          className="add-button"
        >
          <IoIosAdd />
        </button>
      </div>

      <div className="recipes-grid">
        {userRecipes?.map((recipe) => {
          return (
            <div key={recipe.id} className="recipe-tile">
              <Link to={`/recipes/${recipe.id}`} className="recipe-link">
                <div className="recipe-image-container">
                  {recipe?.preview_image ? (
                    <img src={recipe.preview_image} className="recipe-image" />
                  ) : (
                    <img
                      src={no_image_available}
                      alt="no image available"
                      className="recipe-image"
                    />
                  )}
                  <div className="hover-buttons">
                    <button className="save-button">
                      <FaSave />
                    </button>
                    <div className="action-buttons">
                      <button className="open-button">Open</button>
                      <button className="edit-button">
                        <FaEdit />
                      </button>
                      <button className="share-button">
                        <FaShareAlt />
                      </button>
                    </div>
                  </div>
                </div>
                <div className="recipe-highlight">
                  <p className="recipe-description">
                    <span style={{ fontWeight: "bold" }}>{recipe.name}</span>
                  </p>
                </div>
              </Link>
              {/* Open Delete Modal Button */}

              <OpenModalButton
                buttonText="Delete"
                id="delete-button"
                modalComponent={<DeleteRecipeModal recipe_id={recipe.id} />}
              />
            </div>
          );
        })}
      </div>

      {/* Conditional Modal Rendering */}
      {isModalOpen && (
        <DeleteRecipeModal
          recipeId={recipeToDelete}
          onClose={handleCloseModal}
        />
      )}
    </div>
  );
}

export default ManageRecipes;
