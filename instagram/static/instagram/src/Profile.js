import Avatar from "@mui/material/Avatar";
import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import axios from "./axios";
import "./Profile.css";

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

  return (
    <div className="profile">
      <div className="profile__header">
        <div className="profile__headerImage">
          <Avatar />
        </div>
        <div className="profile__headerInfo">
          <div className="profile__title">{user?.username}</div>
          <div className="profile__stats">
            <div className="profile__stat">{user?.post_count} Posts</div>
            <div className="profile__stat">
              {user?.follower_count} Followers
            </div>
            <div className="profile__stat">{user?.follow_count} Following</div>
          </div>
          <div className="profile__desc">
            <div className="profile__name">{user?.name}</div>
          </div>
        </div>
      </div>

      <div className="profile_postsContainer">
        {userPosts?.map((post, index) => {
          if (!index % 3)
            return (
              <div className="profile__postsRow">
                <img
                  className="profile__postImage"
                  onClick={(e) => navigate(`/p/${userPosts[index].id}`)}
                  src={userPosts[index].images[0].url}
                />
                <img
                  className="profile__postImage"
                  onClick={(e) => navigate(`/p/${userPosts[index + 1].id}`)}
                  src={userPosts[index + 1]?.images[0].url}
                />
                <img
                  className="profile__postImage"
                  onClick={(e) => navigate(`/p/${userPosts[index + 2].id}`)}
                  src={userPosts[index + 2]?.images[0].url}
                />
              </div>
            );
        })}
      </div>
    </div>
  );
}

export default Profile;
