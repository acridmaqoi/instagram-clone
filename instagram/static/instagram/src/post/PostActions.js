import BookmarkIcon from "@mui/icons-material/Bookmark";
import BookmarkBorderOutlinedIcon from "@mui/icons-material/BookmarkBorderOutlined";
import ChatBubbleOutlineIcon from "@mui/icons-material/ChatBubbleOutline";
import FavoriteIcon from "@mui/icons-material/Favorite";
import FavoriteBorderIcon from "@mui/icons-material/FavoriteBorder";
import SendOutlined from "@mui/icons-material/SendOutlined";
import Grid from "@mui/material/Grid";
import React, { useState } from "react";
import axios from "../axios";
import "./Post.css";

function PostActions({ post, setPost }) {
  const [likesOpen, setLikesOpen] = useState(false);

  const likePost = () => {
    axios.post(`/likes/${post.id}`).then((res) => {
      post.likeCount++;
      post.hasLiked = true;
      setPost({ ...post });
    });
  };

  const dislikePost = () => {
    axios.delete(`/likes/${post.id}`).then((res) => {
      post.likeCount--;
      post.hasLiked = false;
      setPost({ ...post });
    });
  };

  const savePost = () => {
    axios.post(`/saves/${post.id}`).then((res) => {
      post.hasSaved = true;
      setPost({ ...post });
    });
  };

  const unsavePost = () => {
    axios.delete(`/saves/${post.id}`).then((res) => {
      post.hasSaved = false;
      setPost({ ...post });
    });
  };

  return (
    <div className="post__buttons">
      <div className="post__buttonsLeft">
        <Grid container spacing={1}>
          <Grid item>
            {post?.hasLiked ? (
              <FavoriteIcon
                style={{ color: "#ED4956" }}
                onClick={() => dislikePost()}
              />
            ) : (
              <FavoriteBorderIcon onClick={() => likePost()} />
            )}
          </Grid>
          <Grid item>
            <ChatBubbleOutlineIcon />
          </Grid>
          <Grid item>
            <SendOutlined />
          </Grid>
        </Grid>
      </div>
      <div className="post__buttonsRight">
        {post?.hasSaved ? (
          <BookmarkIcon onClick={() => unsavePost()} />
        ) : (
          <BookmarkBorderOutlinedIcon onClick={() => savePost()} />
        )}
      </div>
    </div>
  );
}

export default PostActions;
