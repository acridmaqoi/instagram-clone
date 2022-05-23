import MoreHorizIcon from "@mui/icons-material/MoreHoriz";
import { Avatar, IconButton } from "@mui/material";
import React from "react";
import "./Post.css";

function PostHeader({ post, setOpen }) {
  return (
    <div className="post__content post--center">
      <div className="post__authorInfo">
        <Avatar src={post?.user.pictureUrl} />
        <div className="post__username">{post?.user.username}</div>
      </div>
      <IconButton onClick={() => setOpen(true)}>
        <MoreHorizIcon />
      </IconButton>
    </div>
  );
}

export default PostHeader;
