import { Link } from "react-router-dom";
import reciprocity_banner from "../../../public/reciprocity_banner.png";
import ProfileButton from "./ProfileButton";
import "./Navigation.css";

function Navigation() {
  return (
    <nav id="nav-bar">
      {/* Logo Section */}
      <div id="logo-banner">
        <Link to="/" className="logo-link">
          <img src={reciprocity_banner} alt="Reciprocity Logo" />
        </Link>
      </div>

      {/* Search Bar */}
      {/* <div id="search-bar-container">
        <SearchBar />
      </div> */}

      {/* Navigation Actions */}
      <div id="actions-container">
        <Link to="/about" className="nav-link">
          About
        </Link>
        {/* <Link to="/restaurants" className="nav-link">
          Restaurants
        </Link> */}
        <ProfileButton />
      </div>
    </nav>
  );
}

export default Navigation;
