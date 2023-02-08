import React, { useState } from "react";
import axios from "axios";
import "./signup.css";
import { REACT_APP_API_URL } from "../utils";

function Signup({ goToPage, setToken }) {
  const [obj, setObj] = useState({
    email: "",
    password: "",
    cpassword: "",
    name: "",
  });

  const [errors, setErrors] = useState({
    email: "",
    password: "",
    cpassword: "",
    name: "",
    serverError: "",
  });

  const headers = {
    "Content-Type": "multipart/form-data",
    accept: "application/json",
  };

  const onChange = (e) => {
    const { value, name } = e.target;
    setObj({ ...obj, [name]: value });
    if (errors[name].length > 0) {
      setErrors({ ...errors, [name]: "" });
    }
    if (errors["serverError"].length > 0) {
      setErrors({ ...errors, serverError: "" });
    }
  };

  const register = async (e) => {
    e.preventDefault();
    if (obj.name.length === 0) {
      setErrors({ ...errors, name: "Name is required" });
      return;
    }
    if (obj.email.length === 0) {
      setErrors({ ...errors, email: "Email is required" });
      return;
    }
    if (obj.password.length === 0) {
      setErrors({ ...errors, password: "Password is required" });
      return;
    }
    if (obj.cpassword.length === 0) {
      setErrors({ ...errors, cpassword: "Confirm Password is required" });
      return;
    } else if (
      obj.cpassword.length > 0 &&
      obj.password.length > 0 &&
      obj.password !== obj.cpassword
    ) {
      setErrors({ ...errors, cpassword: "Password should match" });
      return;
    }

    try {
      const resp = await axios.post(
        REACT_APP_API_URL + "/user/register/",
        {
          email: obj.email,
          name: obj.name,
          password: obj.password,
          password2: obj.cpassword,
        },
        {
          headers,
        }
      );
      if (resp.data && resp.status === 201) {
        setToken(resp.data.token.access);
        goToPage(3);
      }
    } catch (error) {
      console.log("error while signing up", error);
      if (
        error &&
        error.response &&
        error.response.data &&
        error.response.data.errors &&
        error.response.data.errors.email
      ) {
        setErrors({
          ...errors,
          serverError: error.response.data.errors.email[0],
        });
        return;
      }
      setErrors({ ...errors, serverError: error.message });
    }
  };

  return (
    <div className="h-full">
      <div className="container h-full" id="mainclass">
        <div className="form ">
          <h1 className="login">Sign Up </h1>
          <form className="col g-3" id="registrationForm">
            <div className="col-md-3">
              <label htmlFor="validationDefaultUsername" className="form-label">
                UserName
              </label>
              <input
                type="text"
                className="form-control"
                id="validationDefaultUsername"
                aria-describedby="inputGroupPrepend2"
                value={obj.name}
                name={"name"}
                onChange={onChange}
              />
              {errors["name"].length > 0 && (
                <span style={{ color: "red", fontSize: 13 }}>
                  {errors["name"]}
                </span>
              )}
            </div>
            <div className="col-md-3">
              <label htmlFor="email" className="form-label">
                Email
              </label>
              <input
                type="email"
                pattern="^(.+)@(.+)$"
                className="form-control"
                id="email"
                required
                minLength="2"
                value={obj.email}
                name={"email"}
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
                id="password"
                required
                value={obj.password}
                name={"password"}
                onChange={onChange}
              />
              {errors["password"].length > 0 && (
                <span style={{ color: "red", fontSize: 13 }}>
                  {errors["password"]}
                </span>
              )}
            </div>
            <div className="col-md-3">
              <label htmlFor="validationDefault05" className="form-label">
                Confirm Password
              </label>
              <input
                type="password"
                className={
                  obj.password === obj.cpassword
                    ? "form-control"
                    : "red_border form-control"
                }
                id="cpassword"
                required
                value={obj.cpassword}
                name={"cpassword"}
                onChange={onChange}
              />
              {errors["cpassword"].length > 0 && (
                <span style={{ color: "red", fontSize: 13 }}>
                  {errors["cpassword"]}
                </span>
              )}
            </div>
            {errors["serverError"].length > 0 && (
              <span style={{ color: "red", fontSize: 13 }}>
                {errors["serverError"]}
              </span>
            )}
            <div className="col-12 btn-login ">
              <button
                className="btn btn-danger"
                onClick={register}
                style={{ padding: "0rem" }}
                type="submit"
                value="submit"
                id="register"
              >
                Register
              </button>
              <button
                className="btn"
                style={{ padding: "0rem" }}
                onClick={() => goToPage(1)}
                type="button"
              >
                Login
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default Signup;
