import { useEffect } from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import "./App.css";
import Header from "./Header";
import Home from "./Home";
import Login from "./Login";
import Post from "./Post";
import Profile from "./Profile";
import { setSession } from "./session";
import { useStateValue } from "./StateProvider";
import Upload from "./Upload";

function App() {
  const [{ user }, dispatch] = useStateValue();

  useEffect(() => {
    if (localStorage.getItem("token")) {
      setSession(dispatch);
    }
  }, []);

  return (
    <div className="app">
      {user ? (
        <Router>
          <Header />
          <div className="app__mainContent">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/:id" element={<Profile />} />
              <Route path="/p/:id" element={<Post />} />
              <Route path="/upload" element={<Upload />} />
            </Routes>
          </div>
        </Router>
      ) : (
        <Login />
      )}
    </div>
  );
}

export default App;
