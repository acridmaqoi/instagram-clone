import React from "react";

function PostCommentsSmall({ comment }) {
  return (
    <div className="comment__main">
      <div className="comment__username">{comment.user.username}</div>
      <div className="comment__text">{comment.text}</div>
    </div>
  );
}

export default PostCommentsSmall;
