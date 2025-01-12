import { useState, useEffect } from 'react';
import { apiRequest } from "../../../utils/apiRequest";

export default function BaseButtonFollow({ entityName, isFollowing, apiPrefix }) {
  const [following, setFollowing] = useState(isFollowing);

  useEffect(() => {
    setFollowing(isFollowing);
  }, [isFollowing]);

  const handleFollow = async () => {
    try {
      await apiRequest(`/api/${apiPrefix}/${entityName}/follow`, { method: 'POST' });
      setFollowing(true);
    } catch (error) {
      console.log(`Error while following ${apiPrefix} ${entityName}.`, error);
    }
  };

  const handleUnfollow = async () => {
    try {
      await apiRequest(`/api/${apiPrefix}/${entityName}/follow`, { method: 'DELETE' });
      setFollowing(false);
    } catch (error) {
      console.log(`Error while unfollowing ${apiPrefix} ${entityName}.`, error);
    }
  };

  return (
    <>
      {following ? (
        <button
          onClick={handleUnfollow}
          className="submit-follow follow-followed btn btn-sm rounded-pill fw-bold px-3"
        >
          Вы подписаны
        </button>
      ) : (
        <button
          onClick={handleFollow}
          className="submit-follow btn btn-sm rounded-pill fw-bold px-3"
        >
          Подписаться
        </button>
      )}
    </>
  );
}