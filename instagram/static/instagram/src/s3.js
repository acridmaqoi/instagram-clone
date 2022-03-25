import axios from "./axios";

const s3StaticImageUpload = async (images) => {
  let s3Urls = [];

  for (const image of images) {
    const url = await axios.get("/utils/s3url").then((res) => res.data.url);

    await fetch(url, {
      method: "PUT",
      body: image,
    });

    s3Urls.push(url.split("?")[0]);
  }

  return s3Urls;
};

export default s3StaticImageUpload;
