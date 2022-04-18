import FavoriteIcon from "@mui/icons-material/Favorite";
import FavoriteBorderIcon from "@mui/icons-material/FavoriteBorder";
import { Avatar } from "@mui/material";
import { formatDistanceToNowStrict } from "date-fns";
import React, { useState } from "react";
import axios from "../axios";
import "./PostComments.css";

function PostComment({ comment: initalComment }) {
  const [comment, setComment] = useState(initalComment);

  const likeComment = () => {
    axios.post(`/likes/${comment.id}`).then(() => {});
    let _comment = { ...comment };
    _comment.hasLiked = true;
    setComment(_comment);
  };

  const dislikeComment = () => {
    axios.delete(`/likes/${comment.id}`).then(() => {
      let _comment = { ...comment };
      _comment.hasLiked = false;
      setComment(_comment);
    });
  };

  return (
    <div className="comment">
      <Avatar className="comment__avatar" />
      <div className="comment__content">
        <div className="comment__header">
          <div className="comment__main">
            <div className="comment__username">{comment.user.username}</div>
            <div className="comment__text">{comment.text}</div>
          </div>
          <div className="comment__like">
            {comment.hasLiked ? (
              <FavoriteIcon
                style={{ color: "#ED4956" }}
                onClick={() => dislikeComment()}
              />
            ) : (
              <FavoriteBorderIcon onClick={() => likeComment()} />
            )}
          </div>
        </div>
        <div className="comment__meta">
          {formatDistanceToNowStrict(new Date(comment?.createdAt))}
        </div>
      </div>
    </div>
  );
}

function PostComments({ comments }) {
  return (
    <div className="comments">
      {comments?.map((comment) => (
        <PostComment comment={comment} />
      ))}
    </div>
  );
}

export default PostComments;
