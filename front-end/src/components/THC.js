import { AreaChart, Area, Tooltip, XAxis, YAxis, Label } from "recharts";

function THC({ goToPage,  graphData }) {
  var b = document.getElementsByTagName("svg");
  b[0]?.setAttribute("viewBox", "60 0 880 450");

  return (
    <div className="maindiv background">
      <div
        style={{
          // marginTop: "80px",
          display: "flex",
          alignItems: "center",
          flexDirection: "column",
          height: "90%",
        }}
      >
        <div
          style={{
            width: "60%",
            display: "flex",
            justifyContent: "space-around",
            marginTop: "40px",
          }}
        ></div>

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
            data={graphData}
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
              dataKey="energy"
              stroke="#2b61af"
              fill="url(#colorUv)"
            ></Area>
            <XAxis dataKey="time" tick={false}>
              <Label style={{ fontSize: "130%", fill: "black" }}>Time</Label>
            </XAxis>
            <YAxis dataKey="energy" tick={false}>
              <Label
                style={{
                  textAnchor: "middle",
                  fontSize: "130%",
                  fill: "black",
                }}
                angle={270}
                value={"Energy"}
              />
            </YAxis>
            <Tooltip />
          </AreaChart>
          <button
            className="btn"
            style={{
              fontSize: "30px",
              fontWeight: "bold",
              width:"300px",
              // marginBottom: "150px",
            }}
            onClick={() => goToPage(3)}
          >
            Close
          </button>
          <button className="footer" onClick={() => goToPage(0)}>
            {" "}
            Go To Home
          </button>
        </div>
      </div>
    </div>
  );
}

export default THC;
