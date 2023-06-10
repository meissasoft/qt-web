import React from "react";
import "./components.css";
import axios from "axios";
import { REACT_APP_API_URL } from './utils'
// import Live from "../assets/icons/live.png";
// import Data from "../assets/icons/data.png";
function Reference({ goToPage ,token, scanId, setCheckData}) {
  const Spinner = () => <div className="loader"></div>;
  const [loader, setLoader] = React.useState(true)

  const getStatus = async () => {
    try {
      const resp = await axios.post(
        REACT_APP_API_URL + "/user/check-predict-status/",
        { scan_id: scanId },
        {
          headers: {
            "Content-Type": "multipart/form-data",
            Authorization: "Bearer " + token,
          },
        }
      );
      if(resp && resp.data && resp.data.predict_value
        ){
          setLoader(false)
          setCheckData(true)
          goToPage(4)
        }
        else{
          setTimeout(() =>{
            getStatus()
          },5000)

        }
    } catch (err) {
      console.log("error while getMachineData", err);
    }
  };
  React.useEffect(() =>{
    getStatus()
  },[])
  return (
    <div className="maindiv background">
     {loader ? <Spinner/> : 
     <>
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
          <button className="btn" onClick={() => goToPage(3)}>
            Nope, use old reference
          </button>
        </div>
      </div>
      <button className="footer" onClick={()=>goToPage(14)}> Go To Home</button>
     </>
     }
    </div>
  );
}

export default Reference;
