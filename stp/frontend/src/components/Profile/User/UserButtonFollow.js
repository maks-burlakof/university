import BaseButtonFollow from "../Base/BaseButtonFollow";

export default function UserButtonFollow({ username, isFollowing }) {
  return (
    <BaseButtonFollow
      entityName={username}
      isFollowing={isFollowing}
      apiPrefix={"user"}
    />
  );
}