import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "./axios";
import s3StaticImageUpload from "./s3";

function Upload() {
  const navigate = useNavigate();

  const [images, setImages] = useState([]);
  const [imageURLs, setImageURLs] = useState([]);

  const [caption, setCaption] = useState("");

  const uploadImages = async (e) => {
    e.preventDefault();
    const staticImageUrls = await s3StaticImageUpload(images);

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
