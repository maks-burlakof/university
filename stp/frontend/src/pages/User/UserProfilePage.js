import React, {useEffect, useState} from "react";
import {useParams} from "react-router-dom";

import { apiRequest } from "../../utils/apiRequest";
import { useUser } from '../../context/UserContext';
import UserProfile from "../../components/Profile/User/UserProfile";
import MyProfile from "../../components/Profile/Me/MyProfile";
import Navbar from "../../components/Navbar/Navbar";
import Footer from "../../components/Footer/Footer";
import LoaderFullSpace from "../../components/Loaders/LoaderFullSpace";


export default function UserProfilePage() {
  const {username} = useParams();
  const user = useUser();

  const [userData, setUserData] = useState(null);

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const userFetched = await apiRequest(`api/user/${username}`);
        setUserData(userFetched);
        console.log("Fetched user data:", userFetched);
      } catch (error) {
        console.error("There was an error fetching the user data!", error);
      }
    };

    if (!username || username === "me") {
      setUserData(user);
    } else {
      fetchUserData();
    }
  }, [user, username]);

  if (!userData) {
    return <LoaderFullSpace />;
  }

  const isOwnProfile = user && user.username === userData.username;
  const profileComponent = isOwnProfile ? (
    <MyProfile user={userData} />
  ) : (
    <UserProfile user={userData} />
  );

  return (
    <>
      <Navbar />
      <div className="container mt-5 mb-5">
        <div id="content-top-padding" className="pt-sm-4"></div>
        {profileComponent}
      </div>
    </>
  )
}