import { Dialog, Divider } from "@mui/material";
import ListItem from "@mui/material/ListItem";
import PropTypes from "prop-types";
import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import axios from "../axios";
import PostGrid from "../PostGrid";
import AddComment from "./AddComment";
import "./Post.css";
import PostActions from "./PostActions";
import PostComments from "./PostComments";
import PostDate from "./PostDate";
import PostHeader from "./PostHeader";
import PostLikeCount from "./PostLikeCount";

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
  const [relatedPosts, setRelatedPosts] = useState();
  const [open, setOpen] = useState(false);

  useEffect(() => {
    axios.get(`/posts/${post_id}`).then((res) => {
      console.log(res.data);

      const _post = res.data;
      setPost(_post);

      axios
        .get(`/posts?user_id=${_post?.user.id}&exclude_post=${_post?.id}`)
        .then((res) => {
          setRelatedPosts(res.data.posts);
        });
    });
  }, [post_id]);

  const handleClose = (value) => {
    setOpen(false);
    if (value === "deletePost") {
      axios.delete(`/posts/${post_id}`);
      navigate("/");
    }
  };

  return (
    <div className="post">
      <div className="post__container">
        <div className="post__photo">
          <img src={post?.images[0].url} />
        </div>
        <div className="post__info">
          <div className="post__author">
            <PostHeader post={post} setOpen={setOpen} />
          </div>
          <div className="post__comments">
            <div className="post__content">
              <PostComments comments={post?.comments} />
            </div>
          </div>
          <div className="post__actions">
            <div className="post__content post--horizontal">
              <PostActions post={post} setPost={setPost} />
              <PostLikeCount post={post} />
              <PostDate post={post} />
            </div>
          </div>
          <div className="post__addComment">
            <div className="post__content">
              <AddComment post={post} setPost={setPost} />
            </div>
          </div>
        </div>
        <PostDialog selectedValue={"add"} open={open} onClose={handleClose} />
      </div>

      <div className="post__divider">
        <Divider />
      </div>

      <div className="post__suggested">
        <div className="post__suggestedTitle">
          More posts from{" "}
          <span style={{ color: "black" }}>{post?.user.username}</span>
        </div>
        <PostGrid posts={relatedPosts} />
      </div>
    </div>
  );
}

export default Post;
