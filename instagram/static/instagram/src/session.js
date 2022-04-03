import axios from "./axios";

export const setSession = (dispatch) => {
  axios.get("/users/current").then((res) => {
    // session is active
    dispatch({
      type: "SET_CURRENT_USER",
      current_user: res.data,
    });
  });
};
