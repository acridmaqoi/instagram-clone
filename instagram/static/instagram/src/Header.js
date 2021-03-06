import Avatar from "@mui/material/Avatar";
import React from "react";
import { Link } from "react-router-dom";
import "./Header.css";
import { useStateValue } from "./StateProvider";

function Header() {
  const [{ current_user }, dispatch] = useStateValue();

  return (
    <div className="header">
      <Link to="/">
        <img
          className="header__logo"
          src="https://www.instagram.com/static/images/web/mobile_nav_type_logo-2x.png/1b47f9d0e595.png"
        />
      </Link>

      <input placeholder="Search" type="text" />

      <Link to={`/${current_user.username}`}>
        <Avatar src={current_user.pictureUrl} />
      </Link>
    </div>
  );
}

export default Header;
