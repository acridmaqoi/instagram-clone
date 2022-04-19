import React, { useEffect, useState } from "react";
import axios from "../axios";
import UserListModal from "../profile/UserListModal";

function UserLikesModal({ post, open, onClose }) {
  const [users, setUsers] = useState();

  useEffect(() => {
    if (open) {
      axios.get(`/likes?id=${post.id}`).then((res) => {
        setUsers(res.data.users);
      });
    }
  }, [open]);

  return <UserListModal users={users} open={open} onClose={onClose} />;
}

export default UserLikesModal;
