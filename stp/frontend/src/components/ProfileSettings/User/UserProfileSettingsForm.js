import React, {useEffect, useState} from "react";
import {apiRequest} from "../../../utils/apiRequest";
import FormErrorContainer from "../../FormError/FormErrorContainer";
import FormSuccessContainer from "../../FormSuccess/FormSuccessContainer";
import {UploadDropzone} from "@bytescale/upload-widget-react";


export default function UserProfileSettingsForm({ user }) {
  const [first_name, setFirstName] = useState(user.first_name);
  const [last_name, setLastName] = useState(user.last_name);
  const [phone_number, setPhoneNumber] = useState(user.phone_number);
  const [email, setEmail] = useState(user.email);
  const [site_url, setSiteUrl] = useState(user.site_url);
  const [description, setDescription] = useState(user.description);
  const [gender, setGender] = useState(user.gender);
  const [allow_recommends, setAllowRecommends] = useState(user.is_allow_recommends);
  const [profileImage, setProfileImage] = useState(null);

  const [errorMessage, setErrorMessage] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(loading);
  }, [loading]);

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

  const handleUploadComplete = (callback) => {
    if (callback.pendingFiles.length !== 0) {
      setProfileImage(callback.pendingFiles[0].file);
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);

    // Validation
    if (!email) {
      setErrorMessage('Email обязателен');
      setSuccessMessage(null);
      return;
    }
    if (!first_name) {
      setErrorMessage('Имя обязательно');
      setSuccessMessage(null);
      return;
    }
    if (!last_name) {
      setErrorMessage('Фамилия обязательна');
      setSuccessMessage(null);
      return;
    }

    try {
      const formData = new FormData();
      formData.append('first_name', first_name);
      formData.append('last_name', last_name);
      formData.append('phone_number', phone_number);
      formData.append('email', email);
      if (site_url) formData.append('site_url', site_url);
      if (description) formData.append('description', description);
      if (gender) formData.append('gender', gender);
      formData.append('is_allow_recommends', allow_recommends);
      if (profileImage) formData.append('profile_pic', profileImage);

      await apiRequest('/api/user/me', {
        method: 'PATCH',
        body: formData,
      });

      setSuccessMessage('Профиль обновлён');
      setErrorMessage(null);

      if (profileImage) {
        setProfileImage(null);
        window.location.reload();
      }
    } catch (error) {
      setErrorMessage('Произошла ошибка...');
      setSuccessMessage(null);
    }

    setLoading(false);
  }

  const handleDeleteCurrentProfilePicture = async (event) => {
    event.preventDefault();
    try {
      await apiRequest('/api/user/me', {
        method: 'PATCH',
        body: JSON.stringify({
          profile_pic: null,
        }),
      });
      window.location.reload();
    } catch (error) {
      setErrorMessage('Произошла ошибка при удалении фото профиля');
      setSuccessMessage(null);
    }
  };

  return (
    <form encType="multipart/form-data">
      {errorMessage && <FormErrorContainer errorMessage={errorMessage}/>}
      {successMessage && <FormSuccessContainer successMessage={successMessage}/>}
      <div className="mb-3 row">
        <label htmlFor="id_first_name" className="fw-bold col-sm-2 col-form-label">Имя</label>
        <div className="col-sm-10">
          <div>
            <input
              id="id_first_name"
              className="form-control rounded-4"
              name="first_name"
              placeholder="Имя"
              value={first_name}
              onChange={(e) => setFirstName(e.target.value)}
            />
          </div>
        </div>
      </div>
      <div className="mb-3 row">
        <label htmlFor="id_last_name" className="fw-bold col-sm-2 col-form-label">Фамилия</label>
        <div className="col-sm-10">
          <div>
            <input
              id="id_last_name"
              className="form-control rounded-4"
              name="last_name"
              placeholder="Фамилия"
              value={last_name}
              onChange={(e) => setLastName(e.target.value)}
            />
          </div>
        </div>
      </div>
      <div className="mb-3 row">
        <label htmlFor="id_phone_number" className="fw-bold col-sm-2 col-form-label">Номер телефона</label>
        <div className="col-sm-10">
          <div>
            <input
              id="id_phone_number"
              className="form-control rounded-4"
              name="phone_number"
              placeholder="Номер телефона"
              value={phone_number}
              onChange={(e) => setPhoneNumber(e.target.value)}
            />
          </div>
        </div>
      </div>
      <div className="mb-5 row">
        <label htmlFor="id_email" className="fw-bold col-sm-2 col-form-label">E-mail</label>
        <div className="col-sm-10">
          <div>
            <input
              id="id_email"
              className="form-control rounded-4"
              name="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
        </div>
      </div>
      <div className="mb-3 row">
        <label htmlFor="id_site_url" className="fw-bold col-sm-2 col-form-label">Сайт</label>
        <div className="col-sm-10">
          <div>
            <input
              id="id_site_url"
              className="form-control rounded-4"
              name="site_url"
              placeholder="Сайт"
              value={site_url}
              onChange={(e) => setSiteUrl(e.target.value)}
            />
          </div>
        </div>
      </div>
      <div className="mb-3 row">
        <label htmlFor="id_description" className="fw-bold col-sm-2 col-form-label">О себе</label>
        <div className="col-sm-10">
          <div>
            <textarea
              id="id_description"
              className="form-control rounded-4"
              rows={4}
              name="description"
              placeholder="О себе"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />
          </div>
          <div className="form-input-description">
            <span id="id_description_length"></span>
            <span> / 256</span>
          </div>
        </div>
      </div>
      <div className="mb-4 row">
        <label htmlFor="id_gender" className="fw-bold col-sm-2 col-form-label">Пол</label>
        <div className="col-sm-10">
          <div>
            <select
              id={"id_gender"}
              className="form-select rounded-4"
              value={gender}
              onChange={(e) => setGender(e.target.value)}
            >
              <option value={""}>Не выбран</option>
              <option value={"m"}>Мужской</option>
              <option value={"w"}>Женский</option>
            </select>
          </div>
          <span className="form-input-description">
            Эта информация не будет показываться в вашем общедоступном профиле.
          </span>
        </div>
      </div>
      <div className="mb-3 row">
        <label htmlFor="id_is_allow_recommends" className="fw-bold col-sm-4 col-form-label">
          Рекомендовать ваш профиль
        </label>
        <div className="col-sm-8">
          <div className="form-check form-switch">
            <input
              id="id_allow_recommends"
              type="checkbox"
              role="switch"
              className="form-check-input"
              name="allow_recommends"
              checked={allow_recommends}
              onChange={(e) => setAllowRecommends(e.target.checked)}
            />
          </div>
          <span className="form-input-description">Рекомендовать ваш профиль другим пользователям.</span>
        </div>
      </div>

      <button onClick={handleSubmit} className="btn btn-primary rounded-pill">
        Сохранить {loading && <i class="fa-solid fa-circle-notch fa-spin ms-1"></i>}
      </button>

      <div className="modal fade" id="upload-photo-modal" data-bs-backdrop="static" tabIndex="-1" aria-hidden="true">
        <div className="modal-dialog modal-dialog-centered">
          <div className="modal-content rounded-5 p-4">
            <div className="modal-header border-0 pb-1">
              <h5 className="modal-title">
                <i className="fa-regular fa-image me-1"></i> Изменить фото профиля
              </h5>
              <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div className="modal-body">
              <UploadDropzone
                options={ImageUploaderOptions}
                onUpdate={handleUploadComplete}
              />
              {loading && (
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
              <div className="d-flex justify-content-between mt-4">
                <button
                  onClick={handleSubmit}
                  className="btn btn-sm btn-primary rounded-pill"
                >
                  Сохранить {loading && <i class="fa-solid fa-circle-notch fa-spin ms-1"></i>}
                </button>
                <button
                  onClick={handleDeleteCurrentProfilePicture}
                  className="btn btn-sm btn-danger rounded-pill"
                >
                  Удалить текущее фото
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </form>
  )
}