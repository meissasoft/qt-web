import React, { useState } from "react";
import "./login.css";
import axios from "axios";
import { REACT_APP_API_URL } from "../utils";

function Login({ goToPage, setToken }) {
  const [obj, setObj] = useState({
    email: "",
    password: "",
  });

  const [errors, setErrors] = useState({
    email: "",
    password: "",
  });

  const onChange = (e) => {
    const { value, name } = e.target;
    setObj({ ...obj, [name]: value });
    if (errors[name].length > 0) {
      setErrors({ ...errors, [name]: "" });
    }
  };

  const clickLogin = async () => {
    if (obj.email.length === 0) {
      setErrors({ ...errors, email: "Email is required" });
      return;
    }
    if (obj.password.length === 0) {
      setErrors({ ...errors, password: "Password is required" });
      return;
    }
    try {
      const resp = await axios.post(
        REACT_APP_API_URL + "/user/login/",
        {
          email: obj["email"],
          password: obj["password"],
        },
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      if (resp.data && resp.status === 200) {
        setToken(resp.data.token.access);
        goToPage(3);
      }
    } catch (err) {
      console.log("error while login", err);
    }
  };

  return (
    <div className="h-full">
      <div className="container h-full" id="mainclass">
        <div className="form mt-5">
          <h4 className="login">Login to your account </h4>
          <div className="col-md-3">
            <label htmlFor="validationDefault03" className="form-label">
              Email
            </label>
            <input
              type="email"
              className="form-control"
              name="email"
              required
              value={obj.email}
              onChange={onChange}
            />
            {errors["email"].length > 0 && (
              <span style={{ color: "red", fontSize: 13 }}>
                {errors["email"]}
              </span>
            )}
          </div>
          <div className="col-md-3">
            <label htmlFor="validationDefault05" className="form-label">
              Password
            </label>
            <input
              type="password"
              className="form-control"
              name="password"
              required
              value={obj.password}
              onChange={onChange}
            />
            {errors["password"].length > 0 && (
              <span style={{ color: "red", fontSize: 13 }}>
                {errors["password"]}
              </span>
            )}
          </div>
          <div className="col-12 btn-login ">
            <button
              className="btn"
              style={{ padding: "0rem" }}
              type="button"
              onClick={() => goToPage(2)}
            >
              Register
            </button>
            <button
              className="btn btn-danger"
              style={{ padding: "0rem" }}
              onClick={clickLogin}
              id="submit"
            >
              Login
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Login;
