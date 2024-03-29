import React from "react";

function Ensure({ goToPage }) {
  return (
    <div className="maindiv background">
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          flexDirection: "column",
          height: "100%",
        }}
      >
        <p style={{ fontSize: "30px", fontWeight: "500" }}>
          You’re POSITIVE it’s super <br />
          clean and in ambient air??
        </p>
        <p style={{ fontSize: "20px" }}>This is kinda important</p>
        <div
          style={{
            width: "50%",
            display: "flex",
            justifyContent: "space-around",
            marginTop: "20px",
          }}
        >
          <button className="btn" onClick={() => goToPage(7)}>
            Yes, I mean it!
          </button>
          <button className="btn" onClick={() => goToPage(3)}>
            Maybe not...
          </button>
        </div>
      </div>
      <button className="footer" onClick={()=>goToPage(14)}> Go To Home</button>
    </div>
  );
}

export default Ensure;
