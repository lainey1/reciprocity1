// react-vite/src/utils/form_validations.js

export const validateRecipeField = (name, value) => {
  let error = "";
  switch (name) {
    case "name":
      if (!value) {
        error = "Name is required.";
      } else if (value.length > 100) {
        error = "Name must be under 100 characters.";
      }
      break;
    case "yield_servings":
    case "total_time":
    case "cuisine":
    case "ingredients":
    case "instructions":
      if (!value) {
        error = `${name.charAt(0).toUpperCase() + name.slice(1)} is required.`;
      }
      break;

    case "description":
      if (value > 500) {
        error = "Please limit the description to fewer than 500 characters.";
      }
      break;
    default:
      break;
  }

  return error;
};

export const validateAllRecipeFields = (formData) => {
  const finalErrors = {};
  [
    "name",
    "yield_servings",
    "total_time",
    "cuisine",
    "ingredients",
    "instructions",
    "description",
  ].forEach((field) => {
    const error = validateRecipeField(field, formData[field]);
    if (error) finalErrors[field] = error;
  });
  return finalErrors;
};
