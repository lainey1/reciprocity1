import landing_image from "../../../public/landing_image.png";

import "./LandingPage.css";

function LandingPage() {
  return (
    <div id="landing-page-container">
      <h2>Family recipes from...</h2>
      {/* <h1>Welcome to Reciprocity!</h1> */}
      <div id="landing-image-container">
        <img
          src={landing_image}
          alt="Reciprocity - Where Recipes Build Bonds and  Memories Last Forever"
          id="landing-page-image"
        />
      </div>
    </div>
  );
}

export default LandingPage;
