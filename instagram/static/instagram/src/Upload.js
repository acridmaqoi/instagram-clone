import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "./axios";

function Upload() {
  const navigate = useNavigate();

  const [images, setImages] = useState([]);
  const [imageURLs, setImageURLs] = useState([]);

  const [caption, setCaption] = useState("");

  const uploadImages = async (e) => {
    e.preventDefault();

    // upload images to s3
    let staticImageUrls = [];
    for (const image of images) {
      const url = await axios.get("/utils/s3url").then((res) => res.data.url);

      await fetch(url, {
        method: "PUT",
        body: image,
      });

      staticImageUrls.push(url.split("?")[0]);
    }

    // create post
    axios
      .post("/posts", {
        caption: caption,
        images: staticImageUrls.map((url) => ({ url: url })),
      })
      .then((res) => {
        navigate(`/p/${res.data.id}`);
      });
  };

  useEffect(() => {
    if (images.length < 1) return;
    const newImageURLs = [];
    images.forEach((image) => newImageURLs.push(URL.createObjectURL(image)));
    setImageURLs(newImageURLs);
  }, [images]);

  function onImageChange(e) {
    setImages([...e.target.files]);
  }

  return (
    <>
      <input type="file" multiple accept="image/*" onChange={onImageChange} />
      {imageURLs.map((imageSrc) => (
        <img src={imageSrc} />
      ))}

      {images.length > 0 && (
        <form>
          <input
            type="text"
            value={caption}
            onChange={(e) => setCaption(e.target.value)}
          />
          <button onClick={uploadImages}>upload</button>
        </form>
      )}
    </>
  );
}
export default Upload;
