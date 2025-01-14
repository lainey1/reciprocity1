import { createBrowserRouter } from "react-router-dom";
import Layout from "./Layout";
import LandingPage from "../components/LandingPage";
import About from "../components/About/About";
import {
  LoginFormModal,
  SignupFormModal,
} from "../components/AuthenticationForms";
import AllRecipes from "../components/AllRecipes/AllRecipes";
import RecipeDetails from "../components/RecipeDetails/RecipeDetails";
import CreateRecipe from "../components/ManageRecipes/CreateRecipe";

export const router = createBrowserRouter([
  {
    element: <Layout />,
    children: [
      {
        path: "login",
        element: <LoginFormModal />,
      },
      {
        path: "signup",
        element: <SignupFormModal />,
      },
      {
        path: "/",
        element: <LandingPage />,
      },
      {
        path: "about",
        element: <About />,
      },
      {
        path: "recipes",
        element: <AllRecipes />,
      },
      {
        path: "/recipes/:id",
        element: <RecipeDetails />,
      },
      {
        path: "/recipes/new",
        element: <CreateRecipe />,
      },
    ],
  },
]);
