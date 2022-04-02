import BookmarkBorderOutlinedIcon from "@mui/icons-material/BookmarkBorderOutlined";
import ChatBubbleOutlineIcon from "@mui/icons-material/ChatBubbleOutline";
import FavoriteBorderIcon from "@mui/icons-material/FavoriteBorder";
import SendOutlined from "@mui/icons-material/SendOutlined";
import { Avatar } from "@mui/material";
import Grid from "@mui/material/Grid";
import { formatDistance } from "date-fns";
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
            <div className="post__content post--horizontal">
              <div className="post__buttons">
                <div className="post__buttonsLeft">
                  <Grid container spacing={1}>
                    <Grid item>
                      <FavoriteBorderIcon />
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
                  <BookmarkBorderOutlinedIcon />
                </div>
              </div>
              <div className="post__date">
                {post &&
                  formatDistance(new Date(post?.posted_at), new Date(), {
                    addSuffix: true,
                  })}
              </div>
            </div>
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
