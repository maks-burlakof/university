import {useEffect, useState} from "react";
import {apiRequest} from "../../../utils/apiRequest";
import LoaderFullSpace from "../../Loaders/LoaderFullSpace";
import PublicationsCardView from "../../Publications/PublicationsCardView";

export default function PostsExploreContent() {
  const [postsData, setPostsData] = useState(null);

  useEffect(() => {
    const fetchPostsData = async () => {
      try {
        const postsFetched = await apiRequest(`api/posts/explore?limit=24`);
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

  const publications = postsData.results;

  return (
    <div class="row g-2">
      <PublicationsCardView publications={publications}/>

      {publications.length === 0 && (
        <div class="text-muted opacity-50 p-4 mx-auto">
          <h1 class="fw-bold" style={{fontSize: '4.5rem'}}>
            Так-так...
            <i class="fa-regular fa-snowflake fa-spin-pulse ms-1"></i>
          </h1>
          <h5 class="mb-4">Здесь пока пусто, но именно ты можешь все <strong>исправить</strong>!</h5>
          <a href="/create/post" class="btn text-bg-gray rounded-pill">Запостить первым!</a>
        </div>
      )}
    </div>
  )
}