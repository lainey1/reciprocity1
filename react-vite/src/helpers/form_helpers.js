// react-vite/src/helpers/form_helpers.js

const allowedCuisines = [
  "American",
  "Argentinian",
  "Brazilian",
  "British",
  "Caribbean",
  "Chinese",
  "Colombian",
  "Ethiopian",
  "Filipino",
  "French",
  "Fusion",
  "German",
  "Greek",
  "Indian",
  "Italian",
  "Japanese",
  "Korean",
  "Mediterranean",
  "Mexican",
  "Middle Eastern",
  "Moroccan",
  "Nigerian",
  "Peruvian",
  "South African",
  "Spanish",
  "Thai",
  "Vietnamese",
  "Other",
];

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
    case "ingredients":
    case "instructions":
      if (!value) {
        error = `${name.charAt(0).toUpperCase() + name.slice(1)} is required.`;
      }
      break;
    case "cuisine":
      if (!value || !allowedCuisines.includes(value)) {
        error = "Requires valid cuisine option.";
      }
      break;
    case "short_description":
      if (value > 150) {
        error = "Please limit the description to fewer than 150 characters.";
      }
      break;
    case "description":
      if (value > 500) {
        error = "Please limit the description to fewer than 500 characters.";
      }
      break;
    case "visibility":
      if (!["Everyone", "Only You", "Connections Only"].includes(value)) {
        error = "Invalid visibility option.";
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
