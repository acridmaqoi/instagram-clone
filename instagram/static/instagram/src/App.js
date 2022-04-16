import { createTheme, ThemeProvider } from "@mui/material/styles";
import { useEffect } from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import "./App.css";
import Header from "./Header";
import Home from "./Home";
import Login from "./Login";
import Post from "./Post";
import Profile from "./profile/Profile";
import { setSession } from "./session";
import { useStateValue } from "./StateProvider";
import Upload from "./Upload";

const theme = createTheme({
  palette: {
    primary: {
      main: "#0095F6",
    },
    secondary: {
      main: "#212121",
    },
  },
  typography: {
    button: {
      textTransform: "none",
    },
  },
});

function App() {
  const [{ current_user }, dispatch] = useStateValue();

  useEffect(() => {
    if (localStorage.getItem("token")) {
      setSession(dispatch);
    }
  }, []);

  return (
    <ThemeProvider theme={theme}>
      <div className="app">
        {current_user ? (
          <Router>
            <Header />
            <div className="app__mainContent">
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/:id/*" element={<Profile />} />
                <Route path="/p/:id" element={<Post />} />
                <Route path="/upload" element={<Upload />} />
              </Routes>
            </div>
          </Router>
        ) : (
          <Login />
        )}
      </div>
    </ThemeProvider>
  );
}

export default App;
