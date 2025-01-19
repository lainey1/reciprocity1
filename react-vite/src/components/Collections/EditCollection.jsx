import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { createNewCollection } from "../../redux/collections";
import { useNavigate } from "react-router-dom";

const EditCollection = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const currentUser = useSelector((state) => state.session.user);

  const [newCollectionName, setNewCollectionName] = useState("");
  const [newCollectionDescription, setNewCollectionDescription] = useState("");

  const handleCreate = () => {
    const payload = {
      name: newCollectionName,
      description: newCollectionDescription,
    };
    dispatch(createNewCollection(payload));
    setNewCollectionName("");
    setNewCollectionDescription("");
    navigate(`/user/${currentUser.id}?section=collections`);
  };

  return (
    <div className="manage-collections">
      {/* Edit Collection */}
      <div className="create-collection">
        <h2>Edit Collection</h2>
        <input
          type="text"
          placeholder="Collection Name"
          value={newCollectionName}
          onChange={(e) => setNewCollectionName(e.target.value)}
        />
        <textarea
          placeholder="Collection Description"
          value={newCollectionDescription}
          onChange={(e) => setNewCollectionDescription(e.target.value)}
        ></textarea>
        <button onClick={handleCreate}>Create Collection</button>
      </div>
    </div>
  );
};

export default EditCollection;
