import { useNavigate, useSearchParams } from "react-router-dom";

const UserMenu = ({ currentUser }) => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  // Get the current section from the URL
  const currentSection = searchParams.get("section");

  return (
    <nav className="user-menu">
      <button
        onClick={() =>
          navigate(`/user/${currentUser.id}?section=created_recipes`)
        }
        className={currentSection === "created_recipes" ? "active" : ""}
      >
        Created Recipes
      </button>
      <button
        onClick={() => navigate(`/user/${currentUser.id}?section=collections`)}
        className={currentSection === "collections" ? "active" : ""}
      >
        Collections
      </button>
      <button
        onClick={() => navigate(`/user/${currentUser.id}?section=saved`)}
        className={currentSection === "saved" ? "active" : ""}
      >
        Saved Recipes
      </button>
    </nav>
  );
};

export default UserMenu;
