import React, { useEffect } from "react";
import newton from "../assets/images/cover-image.png";
import "./components.css";

function Intro({ goToPage }) {
  useEffect(() => {
    setTimeout(() => {
      goToPage(1);
    }, [1000]);
  });

  return (
    <div className="maindiv background">
      <img src={newton} alt=""  />
    </div>
  );
}

export default Intro;
