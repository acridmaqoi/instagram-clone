import React, { useState } from "react";
import axios from "./axios";

function Login() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const register = async (e) => {
    const response = await axios({
      method: "post",
      url: `/auth/login`,
      data: {
        username: username,
        email: email,
        password: password,
      },
    }).then((res) => {
      console.log(res);
    });
  };

  return (
    <div className="login">
      <h5>Username</h5>
      <input
        type="text"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      ></input>

      <h5>Email</h5>
      <input
        type="text"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      ></input>

      <h5>Password</h5>
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      ></input>

      <button onClick={register}>Register</button>
    </div>
  );
}

export default Login;
