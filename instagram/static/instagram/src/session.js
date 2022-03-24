import axios from "./axios";

export const setSession = (dispatch) => {
  axios.get("/profile/current").then((res) => {
    // session is active
    dispatch({
      type: "SET_USER",
      user: res.data,
    });
  });
};
