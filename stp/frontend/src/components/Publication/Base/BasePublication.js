import {getTimeAgo} from "../../../utils/dateUtils";
import {useEffect, useState} from "react";
import {apiRequest} from "../../../utils/apiRequest";

export default function BasePublication(
  {
    publication,
    publicationOwnerLink,
  }
) {
  const [liked, setLiked] = useState(publication.is_user_liked);

  useEffect(() => {
    setLiked(publication.is_user_liked);
  }, [publication.is_user_liked]);

  const handleLike = async () => {
    try {
      await apiRequest(`/api/post/${publication.id}/like`, { method: 'POST' });
      setLiked(true);
    } catch (error) {
      console.log(`Error while like post ${publication.id}.`, error);
    }
  };

  const handleUnlike = async () => {
    try {
      await apiRequest(`/api/post/${publication.id}/like`, { method: 'DELETE' });
      setLiked(false);
    } catch (error) {
      console.log(`Error while unlike post ${publication.id}.`, error);
    }
  };

  const [bookmarked, setBookmarked] = useState(publication.is_user_bookmarked);

  useEffect(() => {
    setBookmarked(publication.is_user_bookmarked);
  }, [publication.is_user_bookmarked]);

  const handleBookmark = async () => {
    try {
      await apiRequest(`/api/post/${publication.id}/bookmark`, { method: 'POST' });
      setBookmarked(true);
    } catch (error) {
      console.log(`Error while bookmark post ${publication.id}.`, error);
    }
  };

  const handleUnbookmark = async () => {
    try {
      await apiRequest(`/api/post/${publication.id}/bookmark`, { method: 'DELETE' });
      setBookmarked(false);
    } catch (error) {
      console.log(`Error while unbookmark post ${publication.id}.`, error);
    }
  };

  return (
    <div className="card post-card mb-4">
      <div className="card-header">
        <div className="d-flex justify-content-between align-items-center">
          <div>
            {publicationOwnerLink}
            <span className="text-muted small ms-1">· {getTimeAgo(publication.created_at)}</span>
          </div>
          <div>
            {/* TODO: modal here */}
            {/*{% block post-account-modal %}
            <a className="common-link fw-bold" data-bs-toggle="modal" data-bs-target="#post-modal"
               data-bs-whatever="{{ post.pk }}" data-bs-username="{{ post.user_profile.user.username }}"><i
              className="fa-solid fa-ellipsis"></i></a>
            {% endblock %}*/}
          </div>
        </div>
      </div>
      <img src={publication.image} className="card-img-top rounded" alt={publication.description}/>
      <div className="post-buttons post-buttons-flex">
        <div className="post-buttons-flex">
         <span>
            {liked ? (
              <i
                onClick={handleUnlike}
                className="fa-regular fa-heart submit-like like-liked"
              ></i>
            ) : (
              <i
                onClick={handleLike}
                className="fa-regular fa-heart submit-like"
              ></i>
            )}
           <span className="like-count">{publication.likes_num}</span>
         </span>
          {/*{% if post.is_allow_comments %}*/}
          {/*<a href="{{ post.get_absolute_url }}" className="d-flex ms-3">*/}
          {/*  <span><i className="fa-regular fa-comment"></i></span>*/}
          {/*  <span className="comment-count">{{post.get_num_of_comments |default: ""}}</span>*/}
          {/*</a>*/}
          {/*{% endif %}*/}
        </div>
        <div className="post-buttons-flex">
         <span className="me-3">
            <a className="common-link fw-bold lh-1" data-bs-toggle="modal" data-bs-target="#post-share-modal"
               data-type="post" data-pk="{{ post.pk }}"><i className="fa-solid fa-arrow-up-from-bracket"></i></a>
         </span>
          <span>
            {bookmarked ? (
              <i
                onClick={handleUnbookmark}
                className="fa-regular fa-bookmark submit-bookmark bookmark-marked"
              ></i>
            ) : (
              <i
                onClick={handleBookmark}
                className="fa-regular fa-bookmark submit-bookmark"
              ></i>
            )}
         </span>
        </div>
      </div>
      {publication.title && (
        <span className="small limit-str">
          <span className="fw-bold me-1">{publication.user.username}</span>
          {publication.title}
      </span>
      )}
    </div>
  );
}