import BaseProfile from "../Base/BaseProfile";
import ProfileImage from "../ProfileImage";
import UserProfileUsername from "./UserProfileUsername";
import UserProfileButtons from "./UserProfileButtons";
import UserProfileFollowing from "./UserProfileFollowing";
import UserProfileDescription from "./UserProfileDescription";
import UserProfileRecommendedUsers from "./UserProfileRecommendedUsers";
import UserProfilePostTabs from "./UserProfilePostTabs";
import React from "react";
import {userProfilePicUrl} from "../../../utils/userProfilePicUrl";


export default function UserProfile( { user } ) {
  return (
    <>
      <BaseProfile
        entityType={"user"}
        entityName={user.username}
        profileImage={<ProfileImage imageUrl={userProfilePicUrl(user)} />}
        profileUsername={<UserProfileUsername name={user.username} />}
        profileButtons={
          <UserProfileButtons
            username={user.username}
            isFollowing={user.is_following}
          />
        }
        profileFollowersCount={user.followers_count}
        profileFollowing={<UserProfileFollowing profileFollowingCount={user.following_count}/>}
        profileDescription={<UserProfileDescription user={user} />}
        profileRecommendedBlock={<UserProfileRecommendedUsers />}
        profilePostLinks={<UserProfilePostTabs />}
      />
    </>
  )
}