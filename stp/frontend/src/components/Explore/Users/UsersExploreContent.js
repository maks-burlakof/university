import React, {useEffect, useState} from "react";
import {apiRequest} from "../../../utils/apiRequest";
import LoaderFullSpace from "../../Loaders/LoaderFullSpace";
import {userProfilePicUrl} from "../../../utils/userProfilePicUrl";

export default function UsersExploreContent() {
  const [usersData, setUsersData] = useState(null);

  useEffect(() => {
    const fetchUsersData = async () => {
      try {
        const usersFetched = await apiRequest(`api/users/explore?limit=24`);
        setUsersData(usersFetched);
      } catch (error) {
        console.error("There was an error fetching the users data", error);
      }
    };

    fetchUsersData();
  }, []);

  if (!usersData) {
    return <LoaderFullSpace />;
  }

  const users = usersData.results;

  return (
    <>
      {users ? (
        <div className="row row-cols-2 g-5">
          {users.map((exploredUser, index) => (
            <div class="col d-flex align-items-center">
              <a href={`/user/${exploredUser.username}`}>
                <img
                  src={userProfilePicUrl(exploredUser)}
                  class="profile-photo"
                  style={{'width': '110px', 'height': '110px'}}
                />
              </a>
              <div class="ms-4">
                <a href={`/user/${exploredUser.username}`} class="fs-5 fw-bold common-link mb-0">
                  {exploredUser.username}
                </a>
                <p class="mb-0 limit-str" style={{'--num-lines': '1'}}>
                  {exploredUser.first_name} {exploredUser.last_name}
                </p>
                <p class="text-muted small mt-2 mb-2 limit-str" style={{'--num-lines': '2'}}>
                  {exploredUser.description}
                </p>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div class="text-muted opacity-50 p-4 mx-auto">
          <h1 class="fw-bold" style={{fontSize: '4.5rem'}}>
            Хм... <i class="fa-regular fa-circle fa-flip ms-1"></i>
          </h1>
          <h5 class="mb-4">Станьте первым зарегистрированным пользователем!</h5>
          <a href="/signup" class="btn text-bg-gray rounded-pill">Регистрация</a>
        </div>
      )}
    </>
  )
}