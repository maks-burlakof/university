import {useParams} from "react-router-dom";
import React, {useEffect, useState} from "react";
import {apiRequest} from "../../utils/apiRequest";
import Navbar from "../../components/Navbar/Navbar";
import Footer from "../../components/Footer/Footer";
import {useUser} from "../../context/UserContext";
import UserButtonFollow from "../../components/Profile/User/UserButtonFollow";
import {userProfilePicUrl} from "../../utils/userProfilePicUrl";
import LoaderFullSpace from "../../components/Loaders/LoaderFullSpace";
import {getTimeAgo} from "../../utils/dateUtils";

export default function PostPage() {
  const user = useUser();

  const { postId } = useParams();
  const [post, setPost] = useState(null);

  useEffect(() => {
    const fetchPostData = async () => {
      try {
        const postFetched = await apiRequest(`api/post/${postId}`);
        setPost(postFetched);
      } catch (error) {
        console.error("There was an error fetching the post data", error);
      }
    };

    fetchPostData();
  }, [postId]);

  if (!post) {
    return <LoaderFullSpace />;
  }

  return (
    <>
      <Navbar />
      <div className="container mt-5 mb-5">
        <div id="content-top-padding" className="pt-sm-4">
          <div className="row g-5 pt-3 justify-content-center">
            <div className="col-md-6">
              <img src={post.image} className="card-img-top rounded"/>
            </div>
            <div className="col-md-6 col-lg-5 col-xl-4">
              <div className="d-flex justify-content-between align-items-center mb-3">
                <a href={`/user/${post.user.username}`} className="common-link">
                  <span className="d-flex align-items-center">
                     <img src={userProfilePicUrl(post.user)} className="profile-photo me-3"
                          style={{width: "40px", height: "40px"}}/>
                     <span>
                        <p className="fw-bold mb-0">{post.user.username}</p>
                        <p className="small mb-0">
                          {post.user.first_name} {post.user.last_name}
                        </p>
                     </span>
                  </span>
                </a>
                {user.username !== post.user.username && (
                  <UserButtonFollow username={post.user.username} isFollowing={post.user.is_following}/>
                )}
              </div>
              <section
                data-post-id={post.id}
                className="d-flex align-items-center justify-content-between"
                style={{fontSize: '1.31rem'}}
              >
                <div className="d-flex align-items-center">
                  {/* TODO: implement post like */}
                  {/*<span>
                  <i className="fa-regular fa-heart submit-like {% if post.is_liked %}like-liked{% endif %}"
                     style="cursor: pointer"></i>
                  <span className="like-count">{{post.get_num_of_likes |default: ""}}</span>
               </span>*/}
                  {/* TODO: implement post comments */}
                  {/*{% if post.is_allow_comments %}
                  <a className="common-link ms-3" href="#id_comment">
                    <i className="fa-regular fa-comment"></i>
                    <span className="comment-count">{{post.get_num_of_comments |default: ""}}</span>
                  </a>
                  {% endif %}*/}
                </div>
                <div className="d-flex align-items-center">
                  <span className="text-muted me-3" style={{fontSize: '.8rem'}}>{getTimeAgo(post.created_at)}</span>
                  {/* TODO: implement post modal */}
                  {/*<a className="common-link fw-bold me-3" data-bs-toggle="modal" data-bs-target="#post-modal"
                     data-bs-whatever="{{ post.pk }}" data-bs-username="{{ post.user_profile.user.username }}"><i
                    className="fa-solid fa-ellipsis-vertical"></i></a>*/}
                  {user.username === post.user.username && (
                    <>
                      {/* TODO: implement post editing */}
                      {/*<a href="{{ post.get_edit_absolute_url }}" className="common-link fw-bold me-3"><i
                      className="fa-solid fa-gear"></i></a>*/}
                    </>
                  )}
                  <span className="me-3">
                    {/* TODO: implement post share modal */}
                    {/*<a className="common-link fw-bold lh-1" data-bs-toggle="modal" data-bs-target="#post-share-modal"
                        data-type="post" data-pk="{{ post.pk }}"><i
                       className="fa-solid fa-arrow-up-from-bracket"></i></a>*/}
                  </span>
                  <span>
                    {/* TODO: implement post bookmark */}
                    {/*<i
                       className="fa-regular fa-bookmark submit-bookmark {% if post.is_bookmark %}bookmark-marked{% endif %}"
                       style="cursor: pointer"></i>
                     <span className="bookmark-count">{{post.get_num_of_bookmarks |default: ""}}</span>*/}
                  </span>
                </div>
              </section>
              {post.title && (
                <div className="small mt-3">{post.title}</div>
              )}
              <hr/>
            </div>
          </div>
        </div>
      </div>
      <Footer/>
    </>
  )
}