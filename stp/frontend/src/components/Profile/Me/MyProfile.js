import BaseProfile from "../Base/BaseProfile";
import ProfileImage from "../ProfileImage";
import UserProfileUsername from "../User/UserProfileUsername";
import UserProfileFollowing from "../User/UserProfileFollowing";
import UserProfileDescription from "../User/UserProfileDescription";
import UserProfileRecommendedUsers from "../User/UserProfileRecommendedUsers";
import MyProfileButtons from "./MyProfileButtons";
import MyProfilePostTabs from "./MyProfilePostTabs";
import {userProfilePicUrl} from "../../../utils/userProfilePicUrl";


export default function MyProfile( { user } ) {
  return (
    <>
      <BaseProfile
        entityType={"user"}
        entityName={user.username}
        profileImage={<ProfileImage imageUrl={userProfilePicUrl(user)} />}
        profileUsername={<UserProfileUsername name={user.username} />}
        profileButtons={<MyProfileButtons />}
        profileFollowersCount={user.followers_count}
        profileFollowing={<UserProfileFollowing profileFollowingCount={user.following_count} />}
        profileDescription={<UserProfileDescription user={user} />}
        profileRecommendedBlock={<UserProfileRecommendedUsers />}
        profilePostLinks={<MyProfilePostTabs />}
      />
    </>
  )
}