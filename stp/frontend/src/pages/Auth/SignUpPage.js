import React from "react";

import Navbar from "../../components/Navbar/Navbar";
import SignUpForm from "../../components/Auth/SignUpForm";

export default function SignUpPage() {
  return (
    <>
      <style>
        {`
          body {
            background: linear-gradient(-45deg, #2196F3 50%, #EEEEEE 50%) no-repeat;
            overflow-x: hidden;
            background-size: 100% 100%;
          }
        `}
      </style>
      <Navbar/>
      <div className="container mt-5 pt-5 mb-5 pb-3">
        <div id="content-top-padding" className="pt-sm-4">
          <div className="card shadow-lg rounded-5 mx-auto mt-3 mb-3" style={{maxWidth: '30rem'}}>
            <SignUpForm/>
          </div>
          <div className="card shadow-lg rounded-5 mx-auto mb-5" style={{maxWidth: '30rem'}}>
            <div className="card-body p-3">
              <p className="text-center mb-0">
                Есть аккаунт?
                <a href="/login" className="btn btn-primary btn-sm rounded-pill ms-2 px-3">Вход</a>
              </p>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}