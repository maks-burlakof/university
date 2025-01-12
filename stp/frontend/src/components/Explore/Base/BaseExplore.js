import Navbar from "../../Navbar/Navbar";
import React from "react";

export default function BaseExplore({exploreButtons, exploreContent}) {
  return (
    <>
      <style>
        {`
          .container {
            @media(min-width: 1200px) {
              max-width: 1100px;
            }
          }
        `}
      </style>

      <Navbar/>
      <div className="container mt-5 mb-5">
        <div id="content-top-padding" className="pt-sm-4"></div>
        {exploreButtons}
        {exploreContent}
      </div>
    </>
  );
}