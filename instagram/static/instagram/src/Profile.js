import Avatar from "@mui/material/Avatar";
import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import axios from "./axios";
import "./Profile.css";
import s3StaticImageUpload from "./s3";

function Profile() {
  const navigate = useNavigate();

  const { id: username } = useParams();
  const [user, setUser] = useState();
  const [userPosts, setUserPosts] = useState();

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
    _user.picture_url = urls[0];
    updateUser(_user);
    setUser(_user);
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
              src={user?.picture_url}
              sx={{ height: "100px", width: "100px" }}
            />
          </label>
          <input
            id="avatar_upload"
            type="file"
            accept="image/*"
            onChange={onUpdateAvatar}
          />
        </div>
        <div className="profile__headerInfo">
          <div className="profile__title">{user?.username}</div>
          <div className="profile__stats">
            <div className="profile__stat">
              <span className="profile__statNumber">{user?.post_count}</span>{" "}
              Posts
            </div>
            <div className="profile__stat">
              <span className="profile__statNumber">
                {user?.follower_count}
              </span>{" "}
              Followers
            </div>
            <div className="profile__stat">
              <span className="profile__statNumber">{user?.follow_count}</span>{" "}
              Following
            </div>
          </div>
          <div className="profile__desc">
            <div className="profile__name">{user?.name}</div>
          </div>
        </div>
      </div>
      <div className="profile__postsContainer">
        {userPosts?.map((post, index) => (
          <div className="profile__postItem">
            <img
              className="profile__postItem"
              onClick={(e) => navigate(`/p/${post.id}`)}
              src={post.images[0].url}
            />
          </div>
        ))}
      </div>
    </div>
  );
}

export default Profile;
