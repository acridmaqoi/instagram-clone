import React, { useState } from "react";
import axios from "./axios";
import { setSession } from "./session";
import { useStateValue } from "./StateProvider";

function Login() {
  // const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [{ current_user }, dispatch] = useStateValue();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const login = async (e) => {
    const response = await axios({
      method: "post",
      url: `/users/login`,
      data: {
        username: username,
        email: email,
        password: password,
      },
    }).then((res) => {
      localStorage.setItem("token", res.data.token);
      setSession(dispatch);
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

      <button onClick={login}>Login</button>
    </div>
  );
}

export default Login;
