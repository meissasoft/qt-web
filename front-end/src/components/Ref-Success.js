import React from "react";

function RefSuccess({ goToPage }) {
  return (
    <div
      className="maindiv background"
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center ",
        justifyContent: "center",
      }}
    >
      <p style={{ fontSize: "30px", fontWeight: "500", marginBottom: "2rem" }}>
        Nice job! That was a good baseline!
      </p>
      <button
        className="btn"
        style={{
          width: "400px",
        }}
        onClick={() => goToPage(8)}
      >
        Let’s Get Going
      </button>
      <button className="footer" onClick={() => goToPage(14)}>
        {" "}
        Go To Home
      </button>
    </div>
  );
}

export default RefSuccess;
