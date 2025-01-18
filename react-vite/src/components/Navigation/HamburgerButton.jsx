import { useState, useEffect, useRef } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { thunkLogout } from "../../redux/session";

import OpenModalMenuItem from "./OpenModalMenuItem";
import { LoginFormModal, SignupFormModal } from "../AuthenticationForms";

function HamburgerButton() {
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const user = useSelector((store) => store.session.user);
  const [showMenu, setShowMenu] = useState(false);
  const ulRef = useRef();

  // Toggle the dropdown menu
  const toggleMenu = (e) => {
    e.stopPropagation(); // Keep from bubbling up to document and triggering closeMenu
    setShowMenu(!showMenu);
  };

  useEffect(() => {
    if (!showMenu) return;

    const closeMenu = (e) => {
      if (ulRef.current && !ulRef.current.contains(e.target)) {
        setShowMenu(false);
      }
    };

    document.addEventListener("click", closeMenu);

    return () => document.removeEventListener("click", closeMenu);
  }, [showMenu]);

  const closeMenu = () => setShowMenu(false);

  const logout = (e) => {
    e.preventDefault();
    dispatch(thunkLogout());
    navigate("/");
    closeMenu();
  };

  return (
    <div className="hamburger-button-container">
      <button onClick={toggleMenu} id="hamburger-button">
        ☰
      </button>
      <div className="drop-down-container">
        {showMenu && (
          <ul className={"profile-menu-dropdown"} ref={ulRef}>
            {user ? (
              <>
                <li className="profile-details no-click">
                  <img
                    src={user.profile_image_url || "/default-profile.png"}
                    alt={`${user.first_name}'s profile`}
                    className="profile-image"
                  />
                  <div id="profile-details-text">
                    <p style={{ fontWeight: "bold" }}>{user.first_name}</p>
                    <p>{user.username}</p>
                    <p>{user.email}</p>
                  </div>
                </li>
                <hr className="menu-separator" /> {/* Horizontal line */}
                <li onClick={() => navigate("/recipes")}>All Recipes</li>
                <li onClick={() => navigate("recipes/owner/:owner_id")}>
                  Manage Recipes
                </li>
                <li onClick={logout}>Logout</li>
              </>
            ) : (
              <>
                <OpenModalMenuItem
                  itemText="Log In"
                  onItemClick={closeMenu}
                  modalComponent={<LoginFormModal />}
                />
                <OpenModalMenuItem
                  itemText="Sign Up"
                  onItemClick={closeMenu}
                  modalComponent={<SignupFormModal />}
                />
                <hr className="menu-separator" /> {/* Horizontal line */}
                <li onClick={() => navigate("/recipes")}>All Recipes</li>
              </>
            )}
          </ul>
        )}
      </div>
    </div>
  );
}

export default HamburgerButton;
