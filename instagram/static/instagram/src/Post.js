import BookmarkBorderOutlinedIcon from "@mui/icons-material/BookmarkBorderOutlined";
import ChatBubbleOutlineIcon from "@mui/icons-material/ChatBubbleOutline";
import FavoriteIcon from "@mui/icons-material/Favorite";
import FavoriteBorderIcon from "@mui/icons-material/FavoriteBorder";
import MoreHorizIcon from "@mui/icons-material/MoreHoriz";
import SendOutlined from "@mui/icons-material/SendOutlined";
import { Avatar, Dialog, IconButton } from "@mui/material";
import Grid from "@mui/material/Grid";
import ListItem from "@mui/material/ListItem";
import { formatDistance } from "date-fns";
import PropTypes from "prop-types";
import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import axios from "./axios";
import "./Post.css";

function PostDialog(props) {
  const { onClose, selectedValue, open } = props;

  const handleClose = () => {
    onClose(selectedValue);
  };

  const handleListItemClick = (value) => {
    onClose(value);
  };

  return (
    <Dialog onClose={handleClose} open={open}>
      <ListItem
        button
        style={{ color: "red" }}
        onClick={() => handleListItemClick("deletePost")}
      >
        Delete
      </ListItem>
      <ListItem button onClick={() => handleListItemClick("cancel")}>
        Cancel
      </ListItem>
    </Dialog>
  );
}

PostDialog.propTypes = {
  onClose: PropTypes.func.isRequired,
  open: PropTypes.bool.isRequired,
  selectedValue: PropTypes.string.isRequired,
};

function Post() {
  const navigate = useNavigate();
  const { id: post_id } = useParams();
  const [post, setPost] = useState();
  const [open, setOpen] = useState(false);

  useEffect(() => {
    axios.get(`/posts/${post_id}`).then((res) => {
      console.log(res.data);
      setPost(res.data);
    });
  }, []);

  const handleClose = (value) => {
    setOpen(false);
    if (value === "deletePost") {
      axios.delete(`/posts/${post_id}`);
      navigate("/");
    }
  };

  const likePost = () => {
    axios.post(`/likes/${post_id}`).then((res) => {
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

  return (
    <div className="post">
      <div className="post__container">
        <div className="post__photo">
          <img src={post?.images[0].url} />
        </div>
        <div className="post__info">
          <div className="post__author">
            <div className="post__content post--center">
              <div className="post__authorInfo">
                <Avatar src={post?.user.pictureUrl} />
                <div className="post__username">{post?.user.username}</div>
              </div>
              <IconButton onClick={() => setOpen(true)}>
                <MoreHorizIcon />
              </IconButton>
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
                  <BookmarkBorderOutlinedIcon />
                </div>
              </div>
              <div className="post__likes">{post?.likeCount} likes</div>
              <div className="post__date">
                {post &&
                  formatDistance(new Date(post?.postedAt), new Date(), {
                    addSuffix: true,
                  })}
              </div>
            </div>
          </div>
          <div className="post__addComment">
            <div className="post__content">add comment</div>
          </div>
        </div>
        <PostDialog selectedValue={"add"} open={open} onClose={handleClose} />
      </div>
    </div>
  );
}

export default Post;
