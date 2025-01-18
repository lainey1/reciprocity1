import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useLocation, useNavigate } from "react-router-dom";

import ManageRecipes from "../ManageRecipes/ManageRecipes";

import { thunkAuthenticate } from "../../redux/session";

import reciprocity_logo from "../../../public/reciprocity_logo.png";

import "./UserProfile.css";

function UserProfile() {
  const location = useLocation();
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const currentUser = useSelector((state) => state.session.user);

  // Extract the 'section" query parameter to have active sections in the profile
  const queryParams = new URLSearchParams(location.search);
  const activeSection = queryParams.get("section") || "profile";

  useEffect(() => {
    if (!currentUser) {
      dispatch(thunkAuthenticate()); // Load current user data
    }
  }, [dispatch, currentUser]);

  if (!currentUser) {
    return (
      <img src={reciprocity_logo} alt="Loading..." className="logo-spinner" />
    );
  }

  return (
    <div id="profile-page">
      {/* Main Profile Details*/}
      <div id="main-profile">
        <div id="user-info">
          <h2 className="name">{currentUser.first_name}</h2>
          <span className="icon-username">
            <img src={reciprocity_logo} id="reciprocity-icon" />
            <h3>{currentUser.username}</h3>
          </span>
          <p>{currentUser.bio}</p>

          {/* user/:userId/edit */}
          <button onClick={() => navigate(`/user/${currentUser.id}/edit`)}>
            Edit Profile
          </button>
        </div>
      </div>

      <nav className="menu">
        <button
          onClick={() =>
            navigate(`/user/${currentUser.id}?section=created_recipes`)
          }
        >
          Created Recipes
        </button>
        <button
          onClick={() => navigate(`/user/${currentUser.id}?section=created`)}
        >
          Collections
        </button>
        <button
          onClick={() => navigate(`/user/${currentUser.id}?section=created`)}
        >
          Saved Recipes
        </button>
      </nav>

      {/* Main Content */}
      <div className="main-content">
        {activeSection === "created_recipes" && <ManageRecipes />}
      </div>
    </div>
  );
}

export default UserProfile;
