import formatDistance from "date-fns/formatDistance";
import React from "react";
import "./Post.css";

function PostDate({ post }) {
  return (
    <div className="post__date">
      {post &&
        formatDistance(new Date(post?.postedAt), new Date(), {
          addSuffix: true,
        })}
    </div>
  );
}

export default PostDate;
