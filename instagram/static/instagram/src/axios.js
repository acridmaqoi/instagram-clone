import axios from "axios";
import { camelizeKeys, decamelizeKeys } from "humps";

const instance = axios.create({
  baseURL: "http://localhost:8000/api",
});

// Append bearer token
instance.interceptors.request.use(function (config) {
  const token = localStorage.getItem("token");
  config.headers.Authorization = token ? `Bearer ${token}` : "";
  return config;
});

// Axios middleware to convert all api responses to camelCase
instance.interceptors.response.use((response) => {
  if (
    response.data &&
    response.headers["content-type"] === "application/json"
  ) {
    response.data = camelizeKeys(response.data);
  }

  return response;
});

// Axios middleware to convert all api requests to snake_case
instance.interceptors.request.use((config) => {
  const newConfig = { ...config };

  if (newConfig.headers["Content-Type"] === "multipart/form-data")
    return newConfig;

  if (config.params) {
    newConfig.params = decamelizeKeys(config.params);
  }

  if (config.data) {
    newConfig.data = decamelizeKeys(config.data);
  }

  return newConfig;
});

export default instance;
