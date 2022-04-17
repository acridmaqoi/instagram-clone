import { Avatar } from "@mui/material";
import React from "react";
import "./PostComments.css";

function PostComments({ comments }) {
  return (
    <div>
      {comments?.map((comment) => (
        <div className="comment">
          <Avatar className="comment__avatar" />
          <div className="comment__content">
            <div className="comment__header">
              <div className="comment__username">{comment.user.username}</div>
              <div className="comment__text">{comment.text}</div>
            </div>
            <div className="comment__meta">date</div>
          </div>
        </div>
      ))}
    </div>
  );
}

export default PostComments;
