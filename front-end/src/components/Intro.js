import React, { useEffect } from "react";
import "./components.css";

function Intro({goToPage}) {

  useEffect(() => {
    setTimeout(() => {
        goToPage(1)
    }, [1000]);
  });

  return (
    <div className="maindiv">
      <div className="h1">
        <h1 className="Welcometag">
          Welcome to Product -to-be-Named <br /> by
          <br /> Company-to-be-named{" "}
        </h1>
      </div>
    </div>
  );
}

export default Intro;
