import React from "react";
// import { LineChart, Line, Tooltip } from "recharts";
import {
  AreaChart,
  Area,
  Tooltip,
  CartesianGrid,
  XAxis,
  YAxis,
  Label,
} from "recharts";

function THC({ goToPage }) {
  const data = [
    {
      time: 1676463556446,
      thc: 10.1,
    },
    {
      time: 1676463683942,
      thc: 15.2,
    },
    {
      time: 1676463556450,
      thc: 20.6,
    },
    {
      time: 1676463556446,
      thc: 32.3,
    },
    {
      time: 1676463556446,
      thc: 40.3,
    },
    {
      time: 1676463683942,
      thc: 50.2,
    },
    {
      time: 1676463556448,
      thc: 55.3,
    },
  ];

  var b = document.getElementsByTagName("svg");
  b[0]?.setAttribute("viewBox", "60 0 880 450");
  return (
    <div className="maindiv background" style={{display:"flex",flexDirection:"column"}}>
      <div>
        {/* <div
          style={{
            // display: "flex",
            // justifyContent: "center",
            // alignItems: "center",
          }}
        ></div> */}
        <AreaChart
          width={800}
          height={390}
          data={data}
          margin={{ top: 5, right: 20, bottom: 5, left: 0 }}
        >
          <defs>
            <linearGradient id="colorUv" x1="0" y1="0" x2="0" y2="1">
              <stop offset="20%" stopColor="#4AA6ED" stopOpacity={0.9} />
              <stop offset="80%" stopColor="#FFFFFF" stopOpacity={0.3} />
            </linearGradient>
          </defs>
          <Area
            type="monotone"
            dataKey="thc"
            stroke="#2b61af"
            fill="url(#colorUv)"
          ></Area>
          <XAxis dataKey="time" tick={false}>
            <Label style={{ fontSize: "130%", fill: "black" }}>
              Time (minutes)
            </Label>
          </XAxis>
          <YAxis dataKey="thc" tick={false}>
            <Label
              style={{
                textAnchor: "middle",
                fontSize: "130%",
                fill: "black",
              }}
              angle={270}
              value={"THC PREDICTION (%)"}
            />
          </YAxis>
          <Tooltip />
        </AreaChart>
      </div>
      <div>
        <button
          className="btn"
          style={{fontSize:"30px",fontWeight:"bold", marginBottom: "150px", }}
          onClick={() => goToPage(5)}
        >
          Close
        </button>
      </div>
    </div>
  );
}

export default THC;
