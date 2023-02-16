import React from "react";
import {
  AreaChart,
  Area,
  Tooltip,
  CartesianGrid,
  XAxis,
  YAxis,
  Label,
} from "recharts";
import Live from "../assets/icons/live.png";
import Data from "../assets/icons/data.png";

function WhatToDo({ goToPage }) {
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
    <div className="maindiv background">
      <div
        style={{
          marginTop:"80px",
          display: "flex",
          // justifyContent: "center",
          alignItems: "center",
          flexDirection: "column",
          height: "100%",
        }}
      >
        <h1 className="text" style={{}}>
          What would you like to do?
        </h1>
        <div
          style={{
            width: "60%",
            display: "flex",
            justifyContent: "space-around",
            marginTop: "40px",
          }}
        >
          <button className="btn" onClick={() => goToPage(4)} style={{}}>
            <img src={Live} alt="" />
            <br />
            Start Live Data
          </button>
          <button className="btn" onClick={() => goToPage(4)} style={{}}>
            <img src={Data} alt="" width={30} />
            <br />
            Show Old Data
          </button>
        </div>

        <div
          style={{
            marginTop: "50px",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            flexDirection: "column",
          }}
        >
          <div
            style={{
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
            }}
          ></div>
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
      </div>
    </div>
  );
}

export default WhatToDo;
