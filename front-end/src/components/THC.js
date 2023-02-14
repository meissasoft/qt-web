import React from "react";
import { LineChart, Line, Tooltip } from "recharts";

function THC({ goToPage }) {
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
    },
  ];
  var b = document.getElementsByTagName("svg");
  b[0]?.setAttribute("viewBox", "60 0 880 450");
  return (
    <div>
      <button
        className="btn"
        style={{ float: "right", marginRight: "8px", marginTop: "8px" }}
        onClick={() => goToPage(5)}
      >
        Close
      </button>
      <div
        className="maindiv"
        style={{
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
        >
          <h1>
            {/* <u>Filename</u> */}
          </h1>
        </div>
        <div style={{ display: "flex" }}>
          <h2 style={{ transform: "rotate(270deg)", marginRight: "-260px" }}>
            THC Prediction (%)
          </h2>
          <div id="svg1">
            <LineChart
              width={550}
              height={390}
              data={data}
              margin={{ top: 5, right: 20, bottom: 5, left: 0 }}
            >
              <Line type="monotone" dataKey="uv" stroke="#000000" />
              {/* <CartesianGrid stroke="#ccc" strokeDasharray="0 0" /> */}
              {/* <XAxis dataKey="hello" Hello/>
    <YAxis /> */}
              <Tooltip />
            </LineChart>
          </div>
        </div>
        <h2>Time (minutes) </h2>
      </div>
    </div>
  );
}

export default THC;
