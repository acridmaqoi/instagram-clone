import React from "react";
import Header from "./Header";
import { useStateValue } from "./StateProvider";

function Home() {
  const [{ user }, dispatch] = useStateValue();

  const logOut = () => {
    localStorage.removeItem("token");
    dispatch({ type: "SET_USER", value: null });
  };

  return (
    <div className="home">
      <Header />
      Home
      <button onClick={logOut}>Logout</button>
    </div>
  );
}

export default Home;
