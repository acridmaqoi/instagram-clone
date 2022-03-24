import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "./axios";

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
      <div className="post__caption">{post?.caption}</div>
      <div className="post__images">
        {post?.images.map((image) => (
          <img src={image.url} alt="" />
        ))}
      </div>
    </div>
  );
}

export default Post;
