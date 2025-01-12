import Navbar from "../../components/Navbar/Navbar";
import UserProfileSettings from "../../components/ProfileSettings/User/UserProfileSettings";
import Footer from "../../components/Footer/Footer";
import React from "react";
import {useUser} from "../../context/UserContext";
import LoaderFullSpace from "../../components/Loaders/LoaderFullSpace";


export default function UserProfileSettingsPage() {
  const user = useUser();

  if (!user) {
    return <LoaderFullSpace />;
  }

  return (
    <>
      <Navbar/>
      <div className="container mt-5 mb-5">
        <div id="content-top-padding" className="pt-sm-4"></div>
        <UserProfileSettings user={user} />
      </div>
      <Footer/>
    </>
  )
}