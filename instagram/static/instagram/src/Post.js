import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "./axios";
import "./Post.css";

function Post() {
  const { id: post_id } = useParams();
  const [post, setPost] = useState();

  useEffect(() => {
    axios.get(`/posts/${post_id}`).then((res) => {
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
          <div className="post__author">author</div>
          <div className="post__comments">comments</div>
          <div className="post__actions">actions</div>
          <div className="post__addComment">add comment</div>
        </div>
      </div>
    </div>
  );
}

export default Post;
