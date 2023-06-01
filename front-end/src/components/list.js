import React, { useState } from "react";
import axios from "axios";
import { REACT_APP_API_URL } from "./utils";

function List({ goToPage, token, setMachine }) {
  let [val, setVal] = useState([]);

  const fetchMachines = async () => {
    try {
      const resp = await axios
        .get(
          REACT_APP_API_URL + "/user/sys-info/",

          {
            headers: {
              "Content-Type": "multipart/form-data",
              Authorization: "Bearer " + token,
            },
          }
        )
        .then((response) => {
          setVal(response.data);
          // val = ;
          val = JSON.stringify(response.data.connected_user_info);
          console.log(val);
        });
    } catch (err) {
      console.log("error while fetching Mahchine", err);
    }
  };

  const getMachineData = async (machine_name) => {
    setMachine(machine_name)
    goToPage(3);
    // try {
    //   const resp = await axios.post(
    //     REACT_APP_API_URL + "/user/itgnir-data/",
    //     { machine_name: machine_name },
    //     {
    //       headers: {
    //         "Content-Type": "*/*",
    //         accept: "application/json",
    //         Authorization: "Bearer " + token,
    //       },
    //     }
    //   );
    //   console.log(resp.data);
    //   if (resp && resp.data && resp.data.itgnir_data) {
    //     console.log(resp.data.itgnir_data);
    //     setMachineGraphData(resp.data.itgnir_data);
    //     goToPage(3);
    //   }
    // } catch (err) {
    //   console.log("error while getMachineData", err);
    // }
  };
  return (
    <div
      className="maindiv1 background"
      style={{ display: "flex", flexDirection: "column", alignItems: "center" }}
    >
      <div>
        <h1
          style={{
            marginTop: "15px",
            fontSize: "30px",
            fontWeight: "700",
            marginBottom: "2rem",
          }}
        >
          Machines List
        </h1>
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
          }}
        >
          <div onClick={fetchMachines} className="machine ">
            Fetch
          </div>
        </div>

        {val?.connected_user_info?.map((val1) => {
          return (
            <h2
              className="machine "
              onClick={() => getMachineData(val1.machine_name)}
              key={val1.machine_name}
            >
              {val1.machine_name}
            </h2>
          );
        })}
      </div>
      <button className="footer" onClick={() => goToPage(0)}>
        {" "}
        Go To Home
      </button>
    </div>
  );
}

export default List;
