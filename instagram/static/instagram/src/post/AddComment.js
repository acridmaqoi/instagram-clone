import React, { useState } from "react";
import axios from "../axios";
import "./AddComment.css";

function AddComment({ post, setPost }) {
  const [comment, setComment] = useState();

  const postComment = () => {
    axios
      .post(`/comments/${post.id}`, {
        text: comment,
      })
      .then((res) => {
        let _post = { ...post };
        post.comments.push(res.data);
        setPost(_post);
      });
  };

  return (
    <div className="commentAdd">
      <input
        value={comment}
        onChange={(e) => setComment(e.target.value)}
        className="commentAdd__input"
        placeholder="Add a comment..."
      ></input>

      <button
        className="comment__button"
        onClick={postComment}
        disabled={!comment}
      >
        Post
      </button>
    </div>
  );
}

export default AddComment;
