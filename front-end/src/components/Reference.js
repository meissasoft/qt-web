import React from "react";
import "./components.css";
// import Live from "../assets/icons/live.png";
// import Data from "../assets/icons/data.png";
function Reference({ goToPage }) {
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
        <h1
          style={{ fontSize: "40px", fontWeight: "bold", lineHeight: "60px" }}
        >
          Is the pipetrain solvent-cleaned
          <br />
          and full of air?
        </h1>
        <p style={{ fontSize: "20px", lineHeight: "40px" }}>
          A reference signal needs to be obtained and these <br />
          conditions must be met
        </p>
        <div
          style={{
            width: "60%",
            display: "flex",
            justifyContent: "space-around",
            marginTop: "40px",
          }}
        >
          {/* <button className="btn" onClick={() => goToPage(4)}>
            <img src={Live} alt="" />
            <br />
            Start Live Data
          </button>
          <button className="btn" onClick={() => goToPage(4)}>
            <img src={Data} alt="" width={30} />
            <br />
            Show Old Data
          </button> */}
        </div>
        <div
          style={{
            width: "60%",
            display: "flex",
            justifyContent: "space-around",
            marginTop: "20px",
          }}
        >
          <button className="btn" onClick={() => goToPage(6)}>
            Yep, get a reference!
          </button>
          <button className="btn" onClick={() => goToPage(6)}>
            Nope, use old reference
          </button>
        </div>
      </div>
      <button className="footer" onClick={()=>goToPage(0)}> Go To Home</button>
    </div>
  );
}

export default Reference;
