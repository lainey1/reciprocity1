import { useDispatch } from "react-redux";
import { useModal } from "../../context/Modal";
import { thunkDeleteRecipe } from "../../redux/recipes";

function DeleteRecipeModal({ recipe_id }) {
  const dispatch = useDispatch();
  const { closeModal } = useModal();

  const handleDelete = async () => {
    try {
      console.log(recipe_id);
      await dispatch(thunkDeleteRecipe(recipe_id));
      closeModal();
    } catch (err) {
      console.error("Error deleting recipe:", err);
    }
  };

  return (
    <div className="page-form-container">
      <form className="form-modal">
        <h3>Confirm Deletion</h3>
        <p>Are you sure you want to delete this recipe?</p>
        <button onClick={handleDelete}>Delete</button>
        <button onClick={closeModal}>Cancel</button>
      </form>
    </div>
  );
}

export default DeleteRecipeModal;
