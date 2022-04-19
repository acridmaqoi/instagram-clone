import { useEffect, useState } from "react";
import axios from "../axios";
import "./Profile.css";
import UserListModal from "./UserListModal";
import "./UserListModal.css";

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

  return <UserListModal users={users} open={open} onClose={onClose} />;
}

export default FollowModal;
