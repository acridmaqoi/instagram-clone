import { Avatar, List, Paper } from "@mui/material";
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
          <Link to={`/${user?.username}`}>
            <Avatar src={user.pictureUrl} />
          </Link>
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
          let users = res.data.users;
          for (let i = 0; i < 40; i++) {
            users.push(res.data.users[0]);
          }
          setUsers(res.data.users);
        });
    }
  }, [open]);

  return (
    <div>
      <Modal open={open} onClose={onClose} disableAutoFocus={true}>
        <Paper
          style={{ maxHeight: 500, overflow: "auto" }}
          sx={{
            position: "absolute",
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)",
            width: 400,
            p: 2,
          }}
        >
          <List>
            {users?.map((follower) => (
              <div className="follow__row">
                <FollowRow follow_user={follower} />
              </div>
            ))}
          </List>
        </Paper>
      </Modal>
    </div>
  );
}

export default FollowModal;
