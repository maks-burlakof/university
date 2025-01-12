import React from 'react';

import Navbar from '../../components/Navbar/Navbar';
import SignInForm from '../../components/Auth/SignInForm';

export default function SignInPage() {
  return (
    <>
      <Navbar/>
      <div className="container mt-5">
        <div id="content-top-padding" className="pt-sm-4">
          <div className="row">
            <div className="col-6 col-xl-7 d-none d-lg-block">
              <div className="mobile-slider"
                   style={{backgroundImage: `url(${process.env.PUBLIC_URL}/img/home-phones.png)`}}>
                <img className="mobile-slider-img1" src={`${process.env.PUBLIC_URL}/img/screenshot1.png`}/>
                <img className="mobile-slider-img2" src={`${process.env.PUBLIC_URL}/img/screenshot2.png`}/>
                <img className="mobile-slider-img3" src={`${process.env.PUBLIC_URL}/img/screenshot3.png`}/>
                <img className="mobile-slider-img4" src={`${process.env.PUBLIC_URL}/img/screenshot4.png`}/>
              </div>
            </div>
            <SignInForm/>
          </div>
        </div>
      </div>
    </>
  );
};