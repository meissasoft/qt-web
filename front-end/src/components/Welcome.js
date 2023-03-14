import React, { useEffect } from "react";
import "./components.css";

function Welcome({goToPage}) {

  useEffect(() => {
    setTimeout(() => {
        goToPage(13)
    }, [1000]);
  });

  return (
    <div className="maindiv background" >
      <div >
        <h1 >
          Welcome to Newton Insights<br /> <br /> by
          <br /> <br /> Company-to-be-named{" "}
        </h1>
      </div>
    </div>
  );
}

export default Welcome;
