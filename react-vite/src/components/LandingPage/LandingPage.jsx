import reciprocity_page_banner from "../../../public/reciprocity_page_banner.png";
import "./LandingPage.css";

function LandingPage() {
  return (
    <div className="landing-page-container">
      <h2>Family recipes from...</h2>
      {/* <h1>Welcome to Reciprocity!</h1> */}
      <div id="page-banner-container">
        <img
          src={reciprocity_page_banner}
          alt="reciprocity page banner"
          id="reciprocity-banner-image"
        />
      </div>
    </div>
  );
}

export default LandingPage;
