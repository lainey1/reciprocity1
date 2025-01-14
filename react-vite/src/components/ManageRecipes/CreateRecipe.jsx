// react-vite/src/components/ManageRecipes/CreateRecipe.jsx

import { useState } from "react";
import { useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import { validateAllRecipeFields } from "../../helpers/form_helpers";
import { thunkCreateRecipe, thunkFetchRecipeById } from "../../redux/recipes";

const CreateRecipe = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    name: "",
    yield_servings: 1,
    prep_time: 1,
    cook_time: 1,
    total_time: 1,
    cuisine: "American",
    short_description: "",
    description: "",
    ingredients: [""],
    instructions: [""],
    tags: "",
    visibility: "Everyone",
  });

  const [errors, setErrors] = useState({});
  const [flashMessage, setFlashMessage] = useState("");
  const [showFlash, setShowFlash] = useState(false);

  // Handle input changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  // Handle number input changes
  const handleNumberChange = (e) => {
    const { name, value } = e.target;
    if (value >= 0 || value === "") {
      setFormData((prevData) => ({
        ...prevData,
        [name]: value,
      }));
    }
  };

  // Add ingredient/instruction dynamically
  const addField = (fieldName) => {
    setFormData((prevData) => ({
      ...prevData,
      [fieldName]: [...prevData[fieldName], ""],
    }));
  };

  // Function to remove an item from a dynamic field
  const removeField = (index, fieldName) => {
    setFormData((prevData) => {
      const updatedField = [...prevData[fieldName]];
      updatedField.splice(index, 1); // Remove the item at the specified index
      return {
        ...prevData,
        [fieldName]: updatedField,
      };
    });
  };

  // Update dynamic fields
  const handleDynamicChange = (index, fieldName, value) => {
    setFormData((prevData) => {
      const updatedField = [...prevData[fieldName]];
      updatedField[index] = value;
      return {
        ...prevData,
        [fieldName]: updatedField,
      };
    });
  };

  // Validate form and display errors
  const validateForm = () => {
    const fieldErrors = validateAllRecipeFields(formData);
    setErrors(fieldErrors);
    return Object.keys(fieldErrors).length === 0; // Return true if no errors
  };

  // Handlers for Save Draft, Post Recipe, Cancel
  // Add flash message logic to saveDraft
  const saveDraft = () => {
    setFlashMessage("Feature Coming Soon");
    setShowFlash(true);

    // Hide the flash message after 3 seconds
    setTimeout(() => {
      setShowFlash(false);
    }, 3000);
  };

  const postRecipe = async (e) => {
    e.preventDefault();

    if (validateForm()) {
      const filteredFormData = {
        ...formData,
        ingredients: formData.ingredients.filter(
          (ingredient) => ingredient.trim() !== ""
        ),
        instructions: formData.instructions.filter(
          (instruction) => instruction.trim() !== ""
        ),
      };

      try {
        const data = await dispatch(thunkCreateRecipe(filteredFormData));
        console.log(data);
        dispatch(thunkFetchRecipeById(data.id));
        navigate(`/recipes/${data.recipe.id}`);
      } catch (error) {
        console.error("Failed to update recipe:", error);
      }
    }
  };

  const cancel = () => {
    console.log("Recipe Creation Cancelled");
    setFormData({
      name: "",
      yield_servings: "",
      prep_time: "",
      cook_time: "",
      total_time: "",
      cuisine: "",
      short_description: "",
      description: "",
      ingredients: [""],
      instructions: [""],
      tags: "",
      visibility: "",
    });
  };

  return (
    <div>
      <h1>Create a New Recipe</h1>

      {showFlash && <div className="flash-message">{flashMessage}</div>}

      <form>
        <label>
          Recipe Name:
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
          />
          {errors.name && <span className="error-message">{errors.name}</span>}
        </label>
        <br />
        <label>
          Servings:
          <input
            type="number"
            name="yield_servings"
            value={formData.yield_servings}
            onChange={handleNumberChange}
          />
          {errors.yield_servings && (
            <span className="error-message">{errors.yield_servings}</span>
          )}
        </label>
        <br />
        <label>
          Prep Time (minutes):
          <input
            type="number"
            name="prep_time"
            value={formData.prep_time}
            onChange={handleNumberChange}
          />
          {errors.prep_time && (
            <span className="error-message">{errors.prep_time}</span>
          )}
        </label>
        <br />
        <label>
          Cook Time (minutes):
          <input
            type="number"
            name="cook_time"
            value={formData.cook_time}
            onChange={handleNumberChange}
          />
          {errors.cook_time && (
            <span className="error-message">{errors.cook_time}</span>
          )}
        </label>
        <br />
        <label>
          Total Time (minutes):
          <input
            type="number"
            name="total_time"
            value={formData.total_time}
            onChange={handleNumberChange}
          />
          {errors.total_time && (
            <span className="error-message">{errors.total_time}</span>
          )}
        </label>
        <br />
        <label>
          Cuisine:
          <select
            name="cuisine"
            value={formData.cuisine}
            onChange={handleChange}
          >
            <option value="">Select Cuisine</option>
            <option value="American">American</option>
            <option value="Argentinian">Argentinian</option>
            <option value="Brazilian">Brazilian</option>
            <option value="British">British</option>
            <option value="Caribbean">Caribbean</option>
            <option value="Chinese">Chinese</option>
            <option value="Colombian">Colombian</option>
            <option value="Ethiopian">Ethiopian</option>
            <option value="Filipino">Filipino</option>
            <option value="French">French</option>
            <option value="Fusion">Fusion</option>
            <option value="German">German</option>
            <option value="Greek">Greek</option>
            <option value="Indian">Indian</option>
            <option value="Italian">Italian</option>
            <option value="Japanese">Japanese</option>
            <option value="Korean">Korean</option>
            <option value="Mediterranean">Mediterranean</option>
            <option value="Mexican">Mexican</option>
            <option value="Middle Eastern">Middle Eastern</option>
            <option value="Moroccan">Moroccan</option>
            <option value="Nigerian">Nigerian</option>
            <option value="Peruvian">Peruvian</option>
            <option value="South African">South African</option>
            <option value="Spanish">Spanish</option>
            <option value="Thai">Thai</option>
            <option value="Vietnamese">Vietnamese</option>
            <option value="Other">Other</option>
          </select>
          {errors.cuisine && (
            <span className="error-message">{errors.cuisine}</span>
          )}
        </label>
        <br />
        <label>
          Short Description:
          <input
            type="text"
            name="short_description"
            value={formData.short_description}
            onChange={handleChange}
          />
          {errors.short_description && (
            <span className="error-message">{errors.short_description}</span>
          )}
        </label>
        <br />
        <label>
          Description:
          <textarea
            name="description"
            value={formData.description}
            onChange={handleChange}
          />
          {errors.description && (
            <span className="error-message">{errors.description}</span>
          )}
        </label>
        <br />
        <h3>Ingredients</h3>
        {formData.ingredients.map((ingredient, index) => (
          <div key={index}>
            <input
              type="text"
              value={ingredient}
              onChange={(e) =>
                handleDynamicChange(index, "ingredients", e.target.value)
              }
            />
            <button
              type="button"
              onClick={() => removeField(index, "ingredients")}
              style={{ marginLeft: "10px" }}
            >
              Delete
            </button>
          </div>
        ))}
        <button type="button" onClick={() => addField("ingredients")}>
          Add Ingredient
        </button>
        <br />
        <h3>Instructions</h3>
        {formData.instructions.map((instruction, index) => (
          <div key={index}>
            <input
              type="text"
              value={instruction}
              onChange={(e) =>
                handleDynamicChange(index, "instructions", e.target.value)
              }
            />
            <button
              type="button"
              onClick={() => removeField(index, "ingredients")}
              style={{ marginLeft: "10px" }}
            >
              Delete
            </button>
          </div>
        ))}
        <button type="button" onClick={() => addField("instructions")}>
          Add Instruction
        </button>
        <br />
        <label>
          Tags:
          <input
            type="text"
            name="tags"
            value={formData.tags}
            onChange={handleChange}
          />
        </label>
        <br />
        <label>
          Who can view this recipe?
          <select
            type="text"
            name="visibility"
            value={formData.visibility}
            onChange={handleChange}
          >
            <option value="Everyone">Everyone</option>
            <option value="Only You">Only You</option>
            <option value="Connections Only">Connections Only</option>
          </select>
        </label>
        <br />
        <button type="button" onClick={saveDraft}>
          Save Draft
        </button>
        <button type="button" onClick={postRecipe}>
          Post Recipe
        </button>
        <button type="button" onClick={cancel}>
          Cancel
        </button>
      </form>
    </div>
  );
};

export default CreateRecipe;
