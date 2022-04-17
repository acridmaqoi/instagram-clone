import Button from "@mui/material/Button";
import { default as React } from "react";
import axios from "../axios";
import "./Profile.css";

function FollowButton({ user, setUser }) {
  const followProfileUser = () => {
    axios.post(`/follows/${user.id}`).then(() => {
      user.followedByViewer = true;
      setUser({ ...user });
    });
  };
  const unfollowProfileUser = () => {
    axios.delete(`/follows/${user.id}`).then(() => {
      user.followedByViewer = false;
      setUser({ ...user });
    });
  };
  return (
    <div>
      {user?.followedByViewer ? (
        <Button
          size="small"
          variant="contained"
          style={{ fontWeight: "600" }}
          onClick={unfollowProfileUser}
        >
          Following
        </Button>
      ) : (
        <Button
          size="small"
          variant="contained"
          style={{ fontWeight: "600" }}
          onClick={followProfileUser}
        >
          Follow
        </Button>
      )}
    </div>
  );
}

export default FollowButton;
