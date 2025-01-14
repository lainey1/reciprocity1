import { useState, useEffect, useRef } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { FaUserCircle } from "react-icons/fa";

import { thunkLogout } from "../../redux/session";
import OpenModalMenuItem from "./OpenModalMenuItem";
import LoginFormModal from "../AuthenticationForms/LoginFormModal";
import SignupFormModal from "../AuthenticationForms/SignupFormModal";

function ProfileButton() {
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const [showMenu, setShowMenu] = useState(false);
  const user = useSelector((store) => store.session.user);
  const ulRef = useRef();

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
    <>
      <button onClick={toggleMenu} id="profile-dropdown-button">
        <FaUserCircle id="icon-user" />
      </button>
      <div className="drop-down-container">
        {showMenu && (
          <ul className={"profile-menu-dropdown"} ref={ulRef}>
            {user ? (
              <>
                <li className="profile-details no-click">
                  <p>{user.first_name}</p>
                  <p>{user.username}</p>
                  <p>{user.email}</p>
                </li>
                <hr className="menu-separator" /> {/* Horizontal line */}
                <li onClick={() => navigate("/recipes")}>Recipes</li>
                <li onClick={() => logout.then(navigate("/recipes"))}>
                  Logout
                </li>
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
              </>
            )}
          </ul>
        )}
      </div>
    </>
  );
}

export default ProfileButton;
