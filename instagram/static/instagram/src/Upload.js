import React, { useEffect, useState } from "react";
import axios from "./axios";

function Upload() {
  const [images, setImages] = useState([]);
  const [imageURLs, setImageURLs] = useState([]);

  const uploadImage = async () => {
    const url = await axios.get("/utils/s3url").then((res) => res.data.url);

    var bodyFormData = new FormData();
    bodyFormData.append("image", images[0]);

    await fetch(url, {
      method: "PUT",
      body: images[0],
    });

    const imageUrl = url.split("?")[0];
    console.log(imageUrl);

    const img = document.createElement("img");
    img.src = imageUrl;
    document.body.appendChild(img);
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

      {images.length > 0 && <button onClick={uploadImage}>upload</button>}
    </>
  );
}
export default Upload;
