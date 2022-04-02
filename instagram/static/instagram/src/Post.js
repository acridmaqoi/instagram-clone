import { Avatar } from "@mui/material";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "./axios";
import "./Post.css";

function Post() {
  const { id: post_id } = useParams();
  const [post, setPost] = useState();

  useEffect(() => {
    axios.get(`/posts/${post_id}`).then((res) => {
      console.log(res.data);
      setPost(res.data);
    });
  }, []);

  return (
    <div className="post">
      <div className="post__container">
        <div className="post__photo">
          <img src={post?.images[0].url} />
        </div>
        <div className="post__info">
          <div className="post__author">
            <div className="post__content">
              <Avatar src={post?.user.picture_url} />
              <div className="post__username">{post?.user.username}</div>
            </div>
          </div>
          <div className="post__comments">
            <div className="post__content">comments</div>
          </div>
          <div className="post__actions">
            <div className="post__content">actions</div>
          </div>
          <div className="post__addComment">
            <div className="post__content">add comment</div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Post;
