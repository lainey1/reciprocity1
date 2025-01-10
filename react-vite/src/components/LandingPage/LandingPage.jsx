import reciprocity_page_banner from "../../../public/reciprocity_page_banner.png";
import "./LandingPage.css";

function LandingPage() {
  return (
    <div className="page-container">
      {/* <h1>Welcome to Reciprocity!</h1> */}
      <div id="page-banner-container">
        <img
          src={reciprocity_page_banner}
          alt="reciprocity page banner"
          id="reciprocity-page-banner"
        />
      </div>
    </div>
  );
}

export default LandingPage;
