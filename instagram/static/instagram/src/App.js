import { useEffect } from "react";
import "./App.css";
import Home from "./Home";
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

  return <div className="app">{user ? <Home /> : <Login />}</div>;
}

export default App;
