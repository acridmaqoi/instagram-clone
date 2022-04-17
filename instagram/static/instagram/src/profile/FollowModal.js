import { Avatar } from "@mui/material";
import Box from "@mui/material/Box";
import Modal from "@mui/material/Modal";
import { default as React, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import axios from "../axios";
import FollowButton from "./FollowButton";
import "./FollowModal.css";
import "./Profile.css";

function FollowRow({ follow_user }) {
  const [user, setUser] = useState(follow_user);

  return (
    <div className="follower">
      <div className="follower__user">
        <div className="follower__avatar">
          <Avatar src={user.pictureUrl} />
        </div>
        <div className="follower__titles">
          <div className="follower__username">
            <Link to={`/${user?.username}`}>{user?.username}</Link>
          </div>
          <div className="follower__name">{user?.name}</div>
        </div>
      </div>
      <div className="follower__button">
        <FollowButton user={user} setUser={setUser} />
      </div>
    </div>
  );
}

function FollowModal({ open, user, following, onClose }) {
  const [users, setUsers] = useState();

  useEffect(() => {
    if (open) {
      axios
        .get(`/follows/${user.id}/${following ? "following" : "followers"}`)
        .then((res) => {
          setUsers(res.data.users);
        });
    }
  }, [open]);

  return (
    <div>
      <Modal open={open} onClose={onClose} disableAutoFocus={true}>
        <Box
          sx={{
            position: "absolute",
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)",
            width: 400,
            bgcolor: "background.paper",
            //border: "2px solid #000",
            boxShadow: 24,
            p: 4,
          }}
        >
          <div>
            {users?.map((follower) => (
              <FollowRow follow_user={follower} />
            ))}
          </div>
        </Box>
      </Modal>
    </div>
  );
}

export default FollowModal;
