import React, { useEffect, useState } from "react";
import {apiRequest} from "../../../utils/apiRequest";
import {userProfilePicUrl} from "../../../utils/userProfilePicUrl";

export default function UserProfileRecommendedUsers() {
  const [recommendedUsers, setRecommendedUsers] = useState(null);

  useEffect(() => {
    async function fetchRecommendedUsers() {
      try {
        const response = await apiRequest("api/users/explore");
        setRecommendedUsers(response);
      } catch (error) {
        console.error("Error fetching recommended users:", error);
      }
    }

    fetchRecommendedUsers();
  }, []);

  if (!recommendedUsers) {
    return (
      <div className="collapse" id="collapseRecommendedItems">
        <div className="pb-3">
          <h6 className="text-muted mb-2">Рекомендуемые</h6>
          <div className="text-muted">Загрузка...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="collapse" id="collapseRecommendedItems">
      <div className="pb-3">
        <h6 className="text-muted mb-2">Рекомендуемые</h6>
        {(recommendedUsers.results.length !== 0) ? (
          <div className="row row-cols-3 row-cols-md-4 row-cols-lg-6 g-2">
            {recommendedUsers.results.map(user => (
              <div className="col" key={user.id}>
                <div className="card card-body rounded-4 h-100">
                  <a href={`/user/${user.username}`} className="common-link text-center">
                    <img src={userProfilePicUrl(user)} className="profile-photo mb-3" style={{width: '80px', height: '80px'}}/>
                    <p className="fw-bold mb-0">{user.username}</p>
                    <p className="text-muted mb-0 limit-str"
                       style={{"--num-lines": 1}}>{user.first_name} {user.last_name}</p>
                  </a>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <span className="text-muted">
            Не смогли найти для вас рекомендуемых пользователей <i className="fa-regular fa-face-frown-open"></i>
          </span>
        )}
      </div>
    </div>
  );
}