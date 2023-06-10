import "./App.css";
import Intro from "./components/Intro";
import WhatToDo from "./components/WhatToDo";
import Reference from "./components/Reference";
import Ensure from "./components/Ensure";
import RefSuccess from "./components/Ref-Success";
import SaveInfo from "./components/SaveInfo";
import EnsureClean from "./components/Ensure-Clean";
import PureSolvent from "./components/Pure-Solvent";
import Sure from "./components/Sure";
import DisplayThc from "./components/Display-THC";
import THC from "./components/THC";
import { useCallback, useState } from "react";
import Login from "./components/login";
import Signup from "./components/signup";
import List from "./components/list";
import Welcome from "./components/Welcome";

function App() {
  const [page, setPage] = useState(0);
  const [token, setToken] = useState("");
  const [scanId, setScanId] = useState("");
  const [machine, setMachine] = useState("");
  const [check, setCheck] = useState(false);
  const [graphData, setGraphData] = useState([]);

  const goToPage = useCallback((pageNumber) => {
    setPage(pageNumber);
  }, []);

  const setMachineGraphData = (data) => {
    if (data.length > 0) {
      // data.forEach((element,ind) => {
      //   element.time = +new Date(element.time)
      // });
      setGraphData(data);
    }
  };

  const content = {
    0: <Intro goToPage={goToPage} />,
    1: <Login goToPage={goToPage} setToken={setToken} />,
    2: <Signup goToPage={goToPage} setToken={setToken} />,
    3: <WhatToDo goToPage={goToPage} token={token} setScanId={setScanId} machine={machine}/>,
    4: <THC goToPage={goToPage} graphData={graphData}  token={token} machine={machine} checkData = {check}/>,
    5: <Reference goToPage={goToPage} token={token} scanId={scanId} setCheckData = {setCheck}/>,
    6: <Ensure goToPage={goToPage} />,
    7: <RefSuccess goToPage={goToPage} />,
    8: <SaveInfo goToPage={goToPage} />,
    9: <EnsureClean goToPage={goToPage} />,
    10: <PureSolvent goToPage={goToPage} />,
    11: <DisplayThc goToPage={goToPage} />,
    12: <Sure goToPage={goToPage} />,
    13: <List goToPage={goToPage}  token={token}  setMachine={setMachine} />,
    14: <Welcome goToPage={goToPage} />,
  };

  return <div>{content[page]}</div>;
}

export default App;
