import Navbar from "../../components/Navbar/Navbar";
import UserProfileSecuritySettings from "../../components/ProfileSettings/UserSecurity/UserProfileSecuritySettings";
import Footer from "../../components/Footer/Footer";
import React from "react";
import {useUser} from "../../context/UserContext";
import LoaderFullSpace from "../../components/Loaders/LoaderFullSpace";


export default function UserProfileSecuritySettingsPage() {
  const user = useUser();

  if (!user) {
    return <LoaderFullSpace />;
  }

  return (
    <>
      <Navbar/>
      <div className="container mt-5 mb-5">
        <div id="content-top-padding" className="pt-sm-4"></div>
        <UserProfileSecuritySettings user={user} />
      </div>
      <Footer/>
    </>
  )
}