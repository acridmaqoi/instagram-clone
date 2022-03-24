import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import axios from "./axios";

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
        console.log(res.data);
        setUserPosts(res.data);
      });
    });
  }, []);

  return (
    <div className="profile">
      <div className="profile__container">
        <div className="profile__lineOne">{user?.username}</div>

        <div className="profile__lineTwo">
          <div className="profile__sectionOne">{user?.post_count} Posts</div>
          <div className="profile__sectionTwo">
            {user?.follower_count} Followers
          </div>
          <div className="profile__sectionTwo">
            {user?.follow_count} Following
          </div>
        </div>
        <div className="profile__lineThree">{user?.name}</div>
      </div>

      <div className="posts__container">
        {userPosts?.posts.map((post) => (
          <img
            onClick={(e) => navigate(`/p/${post.id}`)}
            src={post.images[0].url}
          />
        ))}
      </div>
    </div>
  );
}

export default Profile;
