export const initalState = {
  current_user: null,
};

const reducer = (state, action) => {
  switch (action.type) {
    case "SET_CURRENT_USER":
      return {
        ...state,
        current_user: action.current_user,
      };

    default:
      return state;
  }
};

export default reducer;
