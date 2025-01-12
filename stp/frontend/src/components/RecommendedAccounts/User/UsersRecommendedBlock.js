import React, {useEffect, useState} from "react";
import {apiRequest} from "../../../utils/apiRequest";
import {userProfilePicUrl} from "../../../utils/userProfilePicUrl";
import LoaderInlineBlock from "../../Loaders/LoaderInlineBlock";

export default function UsersRecommendedBlock() {
  const [recommendedUsersData, setRecommendedUsersData] = useState(null);

  useEffect(() => {
    const fetchRecommendedUsersData = async () => {
      try {
        const recommendedUsersFetched = await apiRequest(`api/users/explore?limit=5`);
        setRecommendedUsersData(recommendedUsersFetched);
      } catch (error) {
        console.error("There was an error fetching the users data", error);
      }
    };

    fetchRecommendedUsersData();
  }, []);

  if (!recommendedUsersData) {
    return <LoaderInlineBlock />;
  }

  return (
    <>
      {recommendedUsersData.results.length !== 0 && (
        <>
          <a href={"/explore/users"} className="common-link text-muted fw-bold mb-2">
            Рекомендации для вас <i className="fa-solid fa-angle-right small"></i>
          </a>
          {recommendedUsersData.results.map((recommendedUser, index) => (
            <div className="d-flex align-items-center mb-2" key={index}>
              <a href={`/user/${recommendedUser.username}`}>
                <img
                  src={userProfilePicUrl(recommendedUser)}
                  className="profile-photo me-3"
                  style={{width: '45px', height: '45px'}}
                  alt={recommendedUser.username}
                />
              </a>
              <div>
                <a className="common-link fw-bold mb-0" href={`/user/${recommendedUser.username}`}>
                  {recommendedUser.username}
                </a>
                <p className="text-muted small limit-str mb-0" style={{"--num-lines": 1}}>
                  {recommendedUser.first_name} {recommendedUser.last_name}
                </p>
              </div>
            </div>
          ))}
        </>
      )}
    </>
  );
}