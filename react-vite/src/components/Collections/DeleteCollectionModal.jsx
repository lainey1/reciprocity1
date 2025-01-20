import { useDispatch } from "react-redux";
import { useModal } from "../../context/Modal";
import { deleteCollectionById } from "../../redux/collections";

function DeleteCollectionModal({ collection_id, collection_name }) {
  const dispatch = useDispatch();
  const { closeModal } = useModal();

  const handleDelete = async () => {
    try {
      await dispatch(deleteCollectionById(collection_id)); // Ensure this returns a promise
      window.location.reload(); // Force reload after deletion
      closeModal();
    } catch (err) {
      console.error("Error deleting recipe:", err);
    }
  };

  return (
    <div className="page-form-container">
      <h3>Confirm Deletion</h3>
      <p>
        Are you sure you want to delete this collection:{" "}
        <span style={{ fontWeight: "bold" }}>{collection_name}</span>?
      </p>
      <button onClick={handleDelete}>Delete</button>
      <button onClick={closeModal}>Cancel</button>
    </div>
  );
}

export default DeleteCollectionModal;
