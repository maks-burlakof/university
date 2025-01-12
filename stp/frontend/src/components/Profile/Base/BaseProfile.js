import React, {useEffect, useState} from "react";

import {getRuPluralCount} from "../../../utils/getRuPluralCount";
import {apiRequest} from "../../../utils/apiRequest";
import LoaderFullSpace from "../../Loaders/LoaderFullSpace";
import PublicationsCardView from "../../Publications/PublicationsCardView";


export default function BaseProfile(
  {
    entityType,
    entityName,
    profileImage,
    profileUsername,
    profileButtons,
    profileFollowersCount,
    profileFollowing,
    profileDescription,
    profileRecommendedBlock,
    profilePostLinks,
  }
) {
  const [publicationsData, setPublicationsData] = useState([]);

  useEffect(() => {
    const fetchPublicationsData = async (entityType, entityName) => {
      try {
        const publicationsFetched = await apiRequest(`api/posts/${entityType}/${entityName}?limit=12`);
        /* TODO: implement pagination support */
        setPublicationsData(publicationsFetched);
      } catch (error) {
        console.error("There was an error fetching the publications data!", error);
      }
    };

    fetchPublicationsData(entityType, entityName);
  }, [entityType, entityName]);

  if (publicationsData.length === 0) {
    return <LoaderFullSpace />;
  }

  let publications = publicationsData.results;

  return (
    <>
      <style>
        {`
          .container {
            @media(min-width: 1200px) {
              max-width: 1100px;
            }
          }
        `}
      </style>
      <div className="row pt-sm-3 mb-5">
        <div className="col-3 col-lg-2 col-xl-2 me-2 me-sm-4 me-lg-5">
          {profileImage}
        </div>
        <div className="col-8 col-lg-8 col-xl-9">
          <div className="d-flex justify-content-between align-items-center mb-2">
            <div className="align-items-center fs-3 fw-bold">
              {profileUsername}
            </div>
            <div className="float-end">
              {profileButtons}
            </div>
          </div>
          <div className="d-flex align-items-center mb-4">
            <span className="lh-sm me-5">
              <strong>{publications.length}</strong> {getRuPluralCount(publications.length, ["публикация", "публикации", "публикаций"])}
            </span>
            <a className="common-link lh-sm me-5" data-bs-toggle="modal" data-bs-target="#followers-list">
              <strong
                id="followers-count">{profileFollowersCount}</strong> {getRuPluralCount(profileFollowersCount, ["подписчик", "подписчика", "подписчиков"])}
            </a>
            {profileFollowing}
          </div>
          <div>
            {profileDescription}
          </div>
        </div>
      </div>
      {profileRecommendedBlock}
      <div className="row">
        <div className="col-12">
          <span className="d-flex w-100 border-bottom"></span>
        </div>
      </div>
      <div className="row mb-3">
        <div className="col">
          <div className="d-flex justify-content-evenly align-items-center small text-muted fw-bold">
            {profilePostLinks}
          </div>
        </div>
      </div>
      {<PublicationsCardView publications={publications}/>}
    </>
  );
}