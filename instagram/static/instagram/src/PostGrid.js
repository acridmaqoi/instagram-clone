import React from "react";
import { useNavigate } from "react-router-dom";

function PostGrid(props) {
  const navigate = useNavigate();

  return (
    <div className="profile__postsContainer">
      {props.posts?.map((post, index) => (
        <div className="profile__postItem">
          <img
            className="profile__postItem"
            onClick={(e) => navigate(`/p/${post.id}`)}
            src={post.images[0].url}
          />
        </div>
      ))}
    </div>
  );
}

export default PostGrid;
