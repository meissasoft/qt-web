import React from "react";
import { LineChart, Line } from 'recharts';
function DisplayThc({goToPage}) {
    const data = [
        {
        //   name: "Page A",
          uv: 300,
        //   pv: 0,
        //   amt: 0
        },
        {
        //   name: "Page B",
          uv: 500,
        //   pv: 1398,
        //   amt: 0
        },
        {
        //   name: "Page C",
          uv: 1400,
        //   pv: 9800,
        //   amt: 2290
        },
        {
          name: "Time (minutes)",
          uv: 1280,
        //   pv: 3908,
        //   amt: 2000
        },
        {
        //   name: "Page E",
          uv: 1890,
        //   pv: 4800,
        //   amt: 2181
        },
        {
        //   name: "Page F",
          uv: 2390,
        //   pv: 3800,
        //   amt: 2500
        },
        {
        //   name: "Page G",
          uv: 3490,
        //   pv: 4300,
        //   amt: 2100
        }
      ];
  return (
    <div className="maindiv1">
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
         
        }}
      >
        <h1 style={{ marginTop:"2rem" , marginLeft:"3rem"}}>
          <u>Filename</u>
        </h1>
        <div>
          <p style={{ fontSize: "30px", fontWeight: "400", marginRight:"3rem",marginTop:"2rem" }}>
            Elapsed time: <span style={{ color: "#45818e" }}>93:81</span>
          </p>
        </div>
      </div>
      <div style={{display: "flex", margin: "0rem 2rem", marginTop: "3rem" , justifyContent:"space-between"}}>
        <div style={{ width: "60%", height: "60vh", backgroundColor: "#45818e" }}>
          <p style={{ color: "white", fontSize: "30px" }}>Total THC</p>
            <p
              style={{
                color: "white",
                fontSize: "24vw",
                position: "relative",
                bottom: "6rem"
               }}
            >
              31.6
            <span style={{ color: "white", fontSize: '9vw' }}>%</span>
            </p>
    
        </div>

    <h2 style={{transform:"rotate(270deg)" , marginRight:"-660px"}}>THC Prediction (%)</h2>
        <div style={{ width: "30%"  }}>
        <LineChart width={550} height={390}  data={data} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
   <Line type="monotone" dataKey="uv" stroke="#000000" />
    {/* <CartesianGrid stroke="#ccc" strokeDasharray="0 0" /> */}
    {/* <XAxis dataKey="hello" Hello/>
    <YAxis /> */}
    {/* <Tooltip /> */}
  </LineChart>
  <h2>Time (minutes) </h2>

        </div>
      </div>
      <button className="btn" style={{float:"right" ,position:"relative" , top:"10rem",right:"1rem"}} onClick={()=>goToPage(12)}>Cancel</button>
    </div>
  );
}

export default DisplayThc;
