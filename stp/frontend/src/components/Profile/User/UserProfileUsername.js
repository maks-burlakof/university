import React from "react";

export default function UserProfileUsername({ name }) {
  return (
    <>
      <span className={"me-1"}><i className="fa-solid fa-at"></i></span>
      <span>{name}</span>
    </>
  );
}