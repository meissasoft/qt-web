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
      
      <div style={{display: "flex", flexDirection:"column", margin: "0rem 2rem", marginTop: "3rem" , justifyContent:"space-between"}}>
      <div style={{ width: "30%"  }}>
      <h2 style={{transform:"rotate(270deg)" , marginRight:"-660px"}}>THC Prediction (%)</h2>
        <LineChart width={550} height={390}  data={data} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
   <Line type="monotone" dataKey="uv" stroke="#000000" />
    {/* <CartesianGrid stroke="#ccc" strokeDasharray="0 0" /> */}
    {/* <XAxis dataKey="hello" Hello/>
    <YAxis /> */}
    {/* <Tooltip /> */}
  </LineChart>
  <h2>Time (minutes) </h2>

        </div>
        <divc style={{color:"black",alignItems:"center", marginLeft:"150px", fontSize:"50px"}} >
          TOTAL THC
        </divc>
        <div style={{ width: "30%", height: "20vh", backgroundColor:"#87C1FF",position:"relative",borderRadius:"40px",boxShadow:"2px 2px #D3D3D3" }}>
          {/* <p style={{ color: "white", fontSize: "30px" }}>Total THC</p> */}
            <p
              style={{
                color: "white",
                fontSize: "100px",
                position: "absolute",
               marginTop:"20px",
               fontWeight:"bold",
               marginLeft:"150px",
                alignItems:"center",
                
               }}
            >
              31.6
            <span style={{ color: "white", fontSize: '100px', fontWeight:"bold" }}>%</span>
            </p>
            
            <button className="btn" style={{float:"right" ,position:"relative" , top:"15rem",left:"5px"}} onClick={()=>goToPage(12)}>Cancel</button>
    
        </div>

   
        
      </div>
      
    </div>
  );
}

export default DisplayThc;
