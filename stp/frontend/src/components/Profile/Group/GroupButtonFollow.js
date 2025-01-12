import BaseButtonFollow from "../Base/BaseButtonFollow";

export default function GroupButtonFollow({ groupName, isFollowing }) {
  return (
    <BaseButtonFollow entityName={groupName} isFollowing={isFollowing} apiPrefix={"group"} />
  );
}