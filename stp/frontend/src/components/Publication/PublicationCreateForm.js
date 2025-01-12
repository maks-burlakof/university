import React, {useState} from "react";
import { UploadDropzone } from "@bytescale/upload-widget-react";

import {userProfilePicUrl} from "../../utils/userProfilePicUrl";
import {apiRequest} from "../../utils/apiRequest";
import {useNavigate} from "react-router-dom";
import FormErrorContainer from "../FormError/FormErrorContainer";

export default function PublicationCreateForm({user}) {
  const navigate = useNavigate();

  const ImageUploaderOptions = {
    apiKey: "free",
    maxFileCount: 1,
    maxFileSizeBytes: 10 * 1024 * 1024,
    showFinishButton: false,
    showRemoveButton: false,
    multi: false,
    mimeTypes: ["image/jpeg", "image/png"],
    crop: false,
    styles: {
      colors: {
        primary: "#377dff"
      }
    },
    locale: {
      cancelBtn: "Отмена",
      cancelPreviewBtn: "Отмена",
      continueBtn: "Продолжить",
      orDragDropImage: "или перетащи её сюда",
      uploadImageBtn: "Загрузи пикчу",
    }
  };

  const [postImage, setPostImage] = useState(null);
  const [postTitle, setPostTitle] = useState("");
  const [isAllowComments, setIsAllowComments] = useState(true);

  const [formReady, setFormReady] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const handleUploadComplete = (callback) => {
    if (callback.pendingFiles.length !== 0) {
      setPostImage(callback.pendingFiles[0].file);
      setFormReady(true);
      console.log('File: ', callback.pendingFiles[0].file);
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!postImage || formReady === false) {
      alert("Please upload an image.");
      return;
    }

    try {
      const formData = new FormData();
      formData.append('title', postTitle);
      formData.append('image', postImage);
      formData.append('is_allow_comments', isAllowComments);

      const response = await apiRequest('/api/post', {
        method: 'POST',
        body: formData,
      });

      const createdPostId = response.id;
      navigate(`/post/${createdPostId}`);
      window.location.reload();

    } catch (error) {
      setErrorMessage('Произошла ошибка...');
    }
  };

  return (
    <>
      <form encType="multipart/form-data" id="post-form" onSubmit={handleSubmit}>
        <div className="row g-4 create-post-form justify-content-center" style={{opacity: '.90'}}>
          <div className="col-11 col-sm-9 col-md-5 col-lg-5 col-xl-3">
            <div className="post-upload-image card card-body shadow border-0 p-4">
              <UploadDropzone
                options={ImageUploaderOptions}
                onUpdate={handleUploadComplete}
              />
            </div>
          </div>
          <div className="col-11 col-sm-9 col-md-6 col-lg-5 col-xl-4">
            <div className="post-upload-form card card-body shadow border-0 p-4">
              <div className="d-flex justify-content-between align-items-center mb-3">
                <div className="d-flex align-items-center">
                  <a href="/" className="btn-close me-3"></a>
                  <div id="chosen-account">
                    <img
                      src={userProfilePicUrl(user)}
                      className="profile-photo me-2"
                      style={{width: '30px', height: '30px'}}
                    />
                    <span className="fw-bold">{user.username}</span>
                    <a
                      type="button"
                      className="common-link fw-bold ps-1 pe-3"
                      data-bs-toggle="modal"
                      data-bs-target="#choose-account-modal"
                    >
                      <i className="fa-solid fa-chevron-right"></i>
                    </a>
                    {/* TODO: if no owned group - do not show */}
                    {/* TODO: show tip with this text: You can create groups and publish posts from its account! Create one here <link> */}
                  </div>
                </div>
                <div>
                  {formReady ? (
                    <button className="btn btn-sm btn-purple-moon rounded-pill" type="submit">Опубликовать</button>
                  ) : (
                    <button className="btn btn-sm text-bg-gray rounded-pill">Опубликовать</button>
                  )}
                </div>
              </div>
              {formReady && (
                <div
                  id="post-progressbar"
                  className="progress mb-3"
                  role="progressbar"
                  aria-valuenow="100"
                  aria-valuemin="0"
                  aria-valuemax="100"
                  style={{height: '10px'}}
                >
                  <div
                    className="progress-bar progress-bar-striped progress-bar-animated"
                    style={{width: '100%'}}
                  ></div>
                </div>
              )}
              {errorMessage && <FormErrorContainer errorMessage={errorMessage}/>}
              <div className="mb-3">
                <div className="form-floating">
                    <textarea
                      className="form-control"
                      id="id_title"
                      name="title"
                      rows={5}
                      style={{ height: '100%' }}
                      placeholder="Описание"
                      value={postTitle}
                      onChange={(e) => setPostTitle(e.target.value)}
                    ></textarea>
                  <label htmlFor="id_title">Добавьте подпись...</label>
                </div>
                <div className="form-input-description">
                  <span id="id_title_length"></span>
                  <span> / 512</span>
                </div>
              </div>
              <div className="accordion" id="postExtraSettings">
                <div className="accordion-item">
                  <h2 className="accordion-header">
                    <button
                      className="accordion-button collapsed"
                      type="button"
                      data-bs-toggle="collapse"
                      data-bs-target="#flush-collapseOne"
                      aria-expanded="false"
                      aria-controls="flush-collapseOne"
                    >
                      Расширенные настройки
                    </button>
                  </h2>
                  <div id="flush-collapseOne" className="accordion-collapse collapse" data-bs-parent="#postExtraSettings">
                    <div className="accordion-body">
                      <div className="mb-0">
                        <div className="form-check form-switch">
                          <input
                            id="id_is_allow_comments"
                            type="checkbox"
                            role="switch"
                            className="form-check-input"
                            name="id_is_allow_comments"
                            checked={isAllowComments}
                            onChange={(e) => setIsAllowComments(e.target.checked)}
                          />
                          <label htmlFor="id_is_allow_comments">Разрешить комментарии</label>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </form>
    </>
  )
}