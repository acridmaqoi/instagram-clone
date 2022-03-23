import { useEffect } from "react";
import "./App.css";
import Dashboard from "./Dashboard";
import Login from "./Login";
import { setSession } from "./session";
import { useStateValue } from "./StateProvider";

function App() {
  const [{ user }, dispatch] = useStateValue();

  useEffect(() => {
    if (localStorage.getItem("token")) {
      setSession(dispatch);
    }
  }, []);

  return <div className="app">{user ? <Dashboard /> : <Login />}</div>;
}

export default App;
