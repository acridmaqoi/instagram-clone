import Avatar from "@mui/material/Avatar";
import React from "react";
import "./Header.css";

function Header() {
  return (
    <div className="header">
      <img
        className="header__logo"
        src="https://www.instagram.com/static/images/web/mobile_nav_type_logo-2x.png/1b47f9d0e595.png"
      />

      <input placeholder="Search" type="text" />
      <Avatar />
    </div>
  );
}

export default Header;
