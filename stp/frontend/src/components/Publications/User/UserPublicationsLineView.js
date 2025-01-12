import React from "react";
import UserPublication from "../../Publication/User/UserPublication";

export default function UserPublicationsLineView({ publicationsData }) {
  return (
    <>
      <div className="row g-2">
        {publicationsData.map((publication, index) => (
          <UserPublication publication={publication}/>
        ))}
      </div>
    </>
  );
}