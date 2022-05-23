import { useState } from "react";
import UserLikesModal from "./UserLikesModal.js";

function PostLikeCount({ post }) {
  const [likesOpen, setLikesOpen] = useState(false);

  return (
    <>
      <div className="post__likes" onClick={() => setLikesOpen(true)}>
        {post?.likeCount} likes
      </div>

      <UserLikesModal
        open={likesOpen}
        post={post}
        onClose={() => setLikesOpen(false)}
      />
    </>
  );
}

export default PostLikeCount;
