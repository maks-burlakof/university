import BaseExplore from "../Base/BaseExplore";
import UsersExploreButtons from "./UsersExploreButtons";
import UsersExploreContent from "./UsersExploreContent";

export default function UsersExplore() {
  return (
    <>
      <BaseExplore
        exploreButtons={<UsersExploreButtons />}
        exploreContent={<UsersExploreContent />}
      />
    </>
  )
}