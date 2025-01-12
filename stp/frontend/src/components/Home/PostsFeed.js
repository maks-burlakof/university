import {useEffect, useState} from "react";
import {apiRequest} from "../../utils/apiRequest";
import UserPublicationsLineView from "../Publications/User/UserPublicationsLineView";
import LoaderFullSpace from "../Loaders/LoaderFullSpace";

export default function PostsFeed() {
  const [postsData, setPostsData] = useState(null);

  useEffect(() => {
    const fetchPostsData = async () => {
      try {
        const postsFetched = await apiRequest(`api/posts/following`);
        setPostsData(postsFetched);
      } catch (error) {
        console.error("There was an error fetching the posts data", error);
      }
    };

    fetchPostsData();
  }, []);

  if (!postsData) {
    return <LoaderFullSpace />;
  }

  return (
    <>
      {postsData.results.length !== 0 ? (
        <>
          <UserPublicationsLineView publicationsData={postsData.results}/>
        </>
      ) : (
        <>
          {/* TODO: suggest here to explore users. Show text: This is your feeds with publications from users that you follow. Find interesting users and subscribe */}
        </>
      )}
    </>
  );
}