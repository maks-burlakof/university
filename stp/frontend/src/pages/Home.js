import React from 'react';

import Navbar from '../components/Navbar/Navbar';
import PostsFeed from "../components/Home/PostsFeed";
import UserProfileCard from "../components/Home/UserProfileCard";
import UsersRecommendedBlock from "../components/RecommendedAccounts/User/UsersRecommendedBlock";

export default function Home() {
  return (
    <>
      <Navbar/>
      <div className="container mt-5 mb-5">
        <div id="content-top-padding" className="pt-sm-4"></div>
        <div className="row g-5">
          <div className="col-12 col-sm-12 col-md-7 col-lg-7 col-xl-6 offset-lg-1 offset-xl-2">
            <PostsFeed/>
          </div>
          <div className="d-none d-md-block col-md-5 col-lg-4 col-xl-3">
            <div className="card card-body border-0">
              <UserProfileCard/>
              <UsersRecommendedBlock/>
              <div style={{fontSize: '0.8em', color: 'rgb(204,204,204)'}} className="mt-4">
                <span><a href="#" className="common-link">Информация</a> · </span>
                <span><a href="#" className="common-link">Рейтинг аккаунтов</a> · </span>
                <span><a href="#" className="common-link">Хэштэги</a> · </span>
                <span><a href="#" className="common-link">Места</a></span>
                <p className="mb-0 mt-2"><i className="fa-regular fa-copyright"></i> 2024 BABUSHKA FROM BSUIR</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};