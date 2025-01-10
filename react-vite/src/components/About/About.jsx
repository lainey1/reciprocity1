import logo from "../../../public/reciprocity_logo.png";
import "./About.css";

const About = () => {
  return (
    <div className="page-container">
      <div className="about-image">
        <img src={logo} alt="EaterVerse" />
      </div>

      <div className="about-content">
        <h1>About Reciprocity</h1>
        <p>
          At Reciprocity, we believe that food is more than just nourishment —
          it&apos;s a way to connect, share, and celebrate life’s most
          meaningful moments. Whether it’s a treasured family recipe passed down
          through generations or a spontaneous meal shared with friends, food
          has the power to create lasting bonds and unforgettable memories.
        </p>
        <p>
          Reciprocity is your digital home for preserving and sharing the
          recipes that tell your story. Our app lets you:
        </p>

        <ul className="features">
          <li className="features-item">
            Save and organize your favorite recipes.
          </li>
          <li className="features-item">
            Create family collections that honor your heritage and traditions.
          </li>
          <li className="features-item">
            Tag recipes to specific family members or branches of your family
            tree through Familial Feast, our unique feature for blending food
            with family history.
          </li>
          <li className="features-item">
            Host and plan food meetups to cook, eat, and connect with friends
            and loved ones.
          </li>
        </ul>

        <p>
          We’re dedicated to strengthening relationships, celebrating cultures,
          and fostering joy through the universal language of food. Whether
          you’re passing down a recipe to the next generation or inviting
          friends to a shared table, Reciprocity is here to help you turn simple
          meals into cherished memories.
        </p>

        {/* Horizontal line */}
        <hr style={{ margin: "20px 0", border: "1px solid #465775" }} />

        <p className="tag-line">Let’s gather, savor, and share —</p>
        <p className="tag-line">
          because the best stories always start with reciprocity
        </p>
      </div>
    </div>
  );
};

export default About;
