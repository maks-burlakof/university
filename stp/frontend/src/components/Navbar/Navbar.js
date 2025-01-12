import React from 'react';

import { useUser } from '../../context/UserContext';

import UserProfileImageLink from "../User/UserProfileImageLink";

export default function Navbar() {
  const user = useUser();

  return (
    <div className="d-none d-sm-inline-flex navbar navbar-expand-sm border fixed-top"
         style={{backgroundColor: "#ffffff", height: "54px"}}>
      <div className="container-fluid justify-content-evenly align-items-center">
        <div className="navbar-brand">
          <a href="/">
            <img width="170" src={`${process.env.PUBLIC_URL}/img/babushka-logo.png`} alt="Logo"/>
          </a>
        </div>
        <div>
          <form method="get" action="search/">
            <div className="d-flex align-items-center">
              <button className="btn" type="submit"><i className="fa-solid fa-magnifying-glass"></i></button>
              <input name="q" className="form-control form-control-sm border-0 bg-transparent" type="search"
                     placeholder="Поиск..." aria-label="Поиск..."/>
              <input className="d-none" type="checkbox" role="switch" name="users" checked/>
              <input className="d-none" type="checkbox" role="switch" name="groups" checked/>
              <input className="d-none" type="checkbox" role="switch" name="posts" checked/>
            </div>
          </form>
        </div>
        <div>
          <ul className="navbar-nav">
            <li className="nav-item active">
              <a className="nav-link fs-5 text-dark" href="/">
                <i className="fa-solid fa-house"></i>
              </a>
            </li>
            <li className="nav-item">
              <a className="nav-link fs-5 text-dark" href="/explore/users">
                <i className="fa-solid fa-user-group"></i>
              </a>
            </li>
            <li className="nav-item">
              <a className="nav-link fs-5 text-dark" href="/explore/posts">
                <i className="fa-regular fa-compass fa-spin"></i>
              </a>
            </li>
            <li className="nav-item ms-2 me-2">
              <a className="nav-link fs-5" href="/create/post">
                <span className="badge text-bg-gray rounded-pill" style={{color: "rgb(1,92,227)!important"}}><i
                  className="fa-solid fa-circle-plus"></i> Создать</span>
              </a>
            </li>
            <li className="nav-item">
              <UserProfileImageLink user={user} />
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
}