import { Avatar, List, Paper } from "@mui/material";
import Modal from "@mui/material/Modal";
import { default as React, useState } from "react";
import { Link } from "react-router-dom";
import FollowButton from "./FollowButton";
import "./Profile.css";
import "./UserListModal.css";

function UserRow({ follow_user }) {
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

function UserListModal({ open, users, onClose }) {
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
                <UserRow follow_user={follower} />
              </div>
            ))}
          </List>
        </Paper>
      </Modal>
    </div>
  );
}

export default UserListModal;
