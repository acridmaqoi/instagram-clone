import React, { useEffect, useState } from "react";
import axios from "./axios";
import PostGrid from "./PostGrid";

function SavedPosts() {
  const [savedPosts, setSavedPosts] = useState();

  useEffect(() => {
    axios.get(`/saves`).then((res) => {
      setSavedPosts(res.data.posts);
    });
  }, [savedPosts]);

  return (
    <div>
      <PostGrid posts={savedPosts} />
    </div>
  );
}

export default SavedPosts;
