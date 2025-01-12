import PostsExploreButtons from "./PostsExploreButtons";
import PostsExploreContent from "./PostsExploreContent";
import BaseExplore from "../Base/BaseExplore";

export default function PostsExplore() {
  return (
    <>
      <BaseExplore
        exploreButtons={<PostsExploreButtons />}
        exploreContent={<PostsExploreContent />}
      />
    </>
  )
}