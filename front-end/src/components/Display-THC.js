import React from "react";
function DisplayThc({ goToPage }) {
  return (
    <div className="maindiv2 background">
      <div
        className="percent"
        
      >
        <input
          placeholder="  type here"
          style={{
            width: "500px",
            height: "40px",
           
            borderRadius: "10px",
          }}
        />

        <div
          style={{
            color: "black",
            marginLeft: "80px",
            fontSize: "50px",
          }}
        >
          TOTAL THC
        </div>
        <p
          className="percentage"
         
        >
          31.6
          <span
            style={{ color: "white", fontSize: "100px", fontWeight: "bold" }}
          >
            %
          </span>
        </p>
        {/* <button className="btn" onClick={() => goToPage(13)} >
            
            
            Go to Machine List
          </button> */}
      </div>
      <button className="footer" onClick={()=>goToPage(0)}> Go To Home</button>
    </div>
  );
}

export default DisplayThc;