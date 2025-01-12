import React from 'react';
import { Route, Routes } from 'react-router-dom';

import { UserProvider } from './context/UserContext';

import Home from './pages/Home';
import SignInPage from './pages/Auth/SignInPage';
import SignUpPage from './pages/Auth/SignUpPage';
import UserProfilePage from './pages/User/UserProfilePage';
import GroupProfilePage from './pages/Group/GroupProfilePage';
import UserProfileSettingsPage from "./pages/User/UserProfileSettingsPage";
import UserProfileSettingsSecurityPage from "./pages/User/UserProfileSettingsSecurityPage";
import PostCreatePage from "./pages/Post/PostCreatePage";
import ExploreUsersPage from "./pages/Explore/ExploreUsersPage";
import PostPage from "./pages/Post/PostPage";
import Logout from "./pages/Auth/Logout";
import ExplorePostsPage from "./pages/Explore/ExplorePostsPage";


export default function App() {
  return (
    <div className="App">
      <UserProvider>
        <Routes>
          <Route exact path="/" element={<Home />} />
          <Route path="/login" element={<SignInPage />} />
          <Route path="/signup" element={<SignUpPage />} />
          <Route path="/logout" element={<Logout />} />
          <Route path="/user/" element={<UserProfilePage />} />
          <Route path="/user/edit/" element={<UserProfileSettingsPage />} />
          <Route path="/user/edit/security/" element={<UserProfileSettingsSecurityPage />} />
          <Route path="/user/:username" element={<UserProfilePage />} />
          <Route path="/group/:groupname" element={<GroupProfilePage />} />
          <Route path="/post/:postId" element={<PostPage />} />
          <Route path="/create/post" element={<PostCreatePage />} />
          <Route path="/explore/users" element={<ExploreUsersPage />} />
          <Route path="/explore/posts" element={<ExplorePostsPage />} />
        </Routes>
      </UserProvider>
    </div>
  );
}
