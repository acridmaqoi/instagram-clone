import React from "react";
import { useStateValue } from "./StateProvider";

function Home() {
  const [{ current_user }, dispatch] = useStateValue();

  const logOut = () => {
    localStorage.removeItem("token");
    dispatch({ type: "SET_CURRENT_USER", value: null });
  };

  return (
    <div className="home">
      Home
      <button onClick={logOut}>Logout</button>
    </div>
  );
}

export default Home;
