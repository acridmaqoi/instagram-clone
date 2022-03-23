import React from "react";
import { useParams } from "react-router-dom";

function Profile() {
  const { id: username } = useParams();
  return <div className="profile">Profile {username}</div>;
}

export default Profile;
