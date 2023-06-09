import { AreaChart, Area, Tooltip, XAxis, YAxis, Label } from "recharts";
import React from "react";
import axios from "axios";
import { REACT_APP_API_URL } from "./utils";

function THC({ goToPage, token, machine }) {
  var b = document.getElementsByTagName("svg");
  b[0]?.setAttribute("viewBox", "60 0 880 450");
  const [loader, setLoader] = React.useState(true);
  const [graphDataS, setGraphData] = React.useState([]);
  const getLastTenPredValues = async () => {
    try {
      const resp = await axios.get(
        REACT_APP_API_URL + `/user/last-ten-predict/?machine=${machine}`,
        {
          headers: {
            Authorization: "Bearer " + token,
          },
        }
      );
      if (resp && resp.data) {
        setGraphData(resp.data.predict_values);
        setLoader(false);
      }
    } catch (err) {
      console.log("error while getMachineData", err);
    }
  };
  React.useEffect(() => {
    getLastTenPredValues();
  }, []);
  const Spinner = () => <div className="loader"></div>;

  return (
    <div className="maindiv background">
      {loader ? (
        <Spinner />
      ) : (
        <div
          style={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
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
                width={1000}
                height={400}
                data={graphDataS}
                margin={{ top: 5, left: 0 }}
              >
                <defs>
                  <linearGradient id="colorUv" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="20%" stopColor="#4AA6ED" stopOpacity={0.9} />
                    <stop offset="80%" stopColor="#FFFFFF" stopOpacity={0.3} />
                  </linearGradient>
                </defs>
                <Area
                  type="monotone"
                  dataKey="value"
                  stroke="#2b61af"
                  fill="url(#colorUv)"
                ></Area>
                <XAxis dataKey="time" tick={false}>
                  <Label style={{ fontSize: "130%", fill: "black" }}>
                    Time
                  </Label>
                </XAxis>
                <YAxis dataKey="value" tick={false}>
                  <Label
                    style={{
                      textAnchor: "middle",
                      fontSize: "130%",
                      fill: "black",
                    }}
                    angle={270}
                    value={"Predictions"}
                  />
                </YAxis>
                <Tooltip />
              </AreaChart>
              <button
                className="btn"
                style={{
                  fontSize: "30px",
                  fontWeight: "bold",
                  width: "300px",
                  // marginBottom: "150px",
                }}
                onClick={() => goToPage(12)}
              >
                Close
              </button>
            </div>
          </div>
          <div className="percent">
            <div
              style={{
                color: "black",
                marginLeft: "80px",
                fontSize: "50px",
              }}
            >
              TOTAL THC
            </div>
            <p className="percentage">
              31.6
              <span
                style={{
                  color: "white",
                  fontSize: "100px",
                  fontWeight: "bold",
                }}
              >
                %
              </span>
            </p>
          </div>
          <button
            className="footer"
            onClick={() => goToPage(14)}
            style={{ marginBottom: "-70px" }}
          >
            {" "}
            Go To Home
          </button>
        </div>
      )}
    </div>
  );
}

export default THC;
