import React from "react";

export default function UserProfilePostTabs() {
  return (
    <>
      <a href="#" className="common-link pt-3 posts-link-active">
        <i className="fa-solid fa-table-cells me-1"></i> ПУБЛИКАЦИИ
      </a>
      <a href="#" className="pt-3 common-link">
        <i className="fa-regular fa-bookmark me-1"></i> СОХРАНЕННОЕ
      </a>
      <a href="#" className="pt-3 common-link">
        <i className="fa-regular fa-folder me-1"></i> АРХИВ
      </a>
    </>
  );
}