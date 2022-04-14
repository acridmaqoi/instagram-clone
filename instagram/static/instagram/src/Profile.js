import BookmarkBorderIcon from "@mui/icons-material/BookmarkBorder";
import GridViewIcon from "@mui/icons-material/GridView";
import { Divider } from "@mui/material";
import Avatar from "@mui/material/Avatar";
import Button from "@mui/material/Button";
import React, { useEffect, useState } from "react";
import {
  Link,
  Route,
  Routes,
  useLocation,
  useNavigate,
  useParams,
} from "react-router-dom";
import axios from "./axios";
import PostGrid from "./PostGrid";
import "./Profile.css";
import s3StaticImageUpload from "./s3";
import SavedPosts from "./SavedPosts";
import { useStateValue } from "./StateProvider";

function Profile() {
  const navigate = useNavigate();
  const location = useLocation();

  const [{ current_user }, dispatch] = useStateValue();

  const { id: username } = useParams();
  const [user, setUser] = useState();
  const [userPosts, setUserPosts] = useState();

  const isMe = () => {
    return current_user?.username === user?.username;
  };

  useEffect(() => {
    axios.get(`/users/username/${username}`).then((res) => {
      console.log(res.data);
      let _user = res.data;
      setUser(_user);

      axios.get(`/posts?user_id=${_user.id}`).then((res) => {
        console.log(res.data.posts);
        setUserPosts(res.data.posts);
      });
    });
  }, []);

  const updateUser = (user) => {
    axios.patch(`/users/current`, user);
  };

  const onUpdateAvatar = async (e) => {
    const urls = await s3StaticImageUpload([...e.target.files]);

    let _user = { ...user };
    _user.pictureUrl = urls[0];
    updateUser(_user);
    setUser(_user);
    dispatch({ type: "SET_CURRENT_USER", current_user: _user });
  };

  useEffect(() => {
    console.log("USER ", user);
  }, [user]);

  return (
    <div className="profile">
      <div className="profile__header">
        <div className="profile__headerImage">
          <label for="avatar_upload">
            <Avatar
              className="profile__avatar"
              style={{ cursor: `${isMe() ? "pointer" : "auto"}` }}
              src={user?.pictureUrl}
              sx={{ height: "100px", width: "100px" }}
            />
          </label>
          {isMe() && (
            <input
              id="avatar_upload"
              type="file"
              accept="image/*"
              onChange={onUpdateAvatar}
            />
          )}
        </div>
        <div className="profile__headerInfo">
          <div className="profile__main">
            <div className="profile__title">{user?.username}</div>
            <div className="profile__actions">
              {!isMe() ? (
                <Button
                  size="small"
                  variant="contained"
                  style={{ fontWeight: "600" }}
                >
                  Follow
                </Button>
              ) : (
                <Button size="small" variant="outlined" color="secondary">
                  Edit Profile
                </Button>
              )}
            </div>
          </div>
          <div className="profile__stats">
            <div className="profile__stat">
              <span className="profile__statNumber">{user?.postCount}</span>{" "}
              Posts
            </div>
            <div className="profile__stat">
              <span className="profile__statNumber">{user?.followerCount}</span>{" "}
              Followers
            </div>
            <div className="profile__stat">
              <span className="profile__statNumber">{user?.followCount}</span>{" "}
              Following
            </div>
          </div>
          <div className="profile__desc">
            <div className="profile__name">{user?.name}</div>
          </div>
        </div>
        <Divider />
      </div>

      <div className="profile__divider">
        <Divider />
      </div>

      <div className="profile__pages">
        <div className="profile__page">
          <Link to=".">
            <div
              className="profile__pageIcon"
              style={
                location.pathname === `/${current_user.username}`
                  ? { color: "black" }
                  : {}
              }
            >
              <GridViewIcon />
              Posts
            </div>
          </Link>
        </div>
        <div className="profile__page">
          <Link to="./saved">
            <div
              className="profile__pageIcon"
              style={
                location.pathname === `/${current_user.username}/saved`
                  ? { color: "black" }
                  : {}
              }
            >
              <BookmarkBorderIcon />
              Saved
            </div>
          </Link>
        </div>
      </div>

      <Routes>
        <Route path="/" element={<PostGrid posts={userPosts} />} />
        <Route path="/saved" element={<SavedPosts />} />
      </Routes>
      {/* {userPosts?.map((post, index) => (
          <div className="profile__postItem">
            <img
              className="profile__postItem"
              onClick={(e) => navigate(`/p/${post.id}`)}
              src={post.images[0].url}
            />
          </div>
        ))} */}
    </div>
  );
}

export default Profile;
