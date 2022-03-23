import React from "react";
import { useStateValue } from "./StateProvider";

function Dashboard() {
  const [{ user }, dispatch] = useStateValue();

  const logOut = () => {
    localStorage.removeItem("token");
    dispatch({ type: "SET_USER", value: null });
  };

  return (
    <div className="dashboard">
      Dashboard
      <button onClick={logOut}>Logout</button>
    </div>
  );
}

export default Dashboard;
