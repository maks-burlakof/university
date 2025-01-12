import BaseProfileButtons from "../Base/BaseProfileButtons";
import UserButtonFollow from "./UserButtonFollow";


export default function UserProfileButtons({ username, isFollowing }) {
  return (
    <>
      <UserButtonFollow
        username={username}
        isFollowing={isFollowing}
      />
      <span className={"ms-2"}></span>
      <BaseProfileButtons />
    </>
  );
}