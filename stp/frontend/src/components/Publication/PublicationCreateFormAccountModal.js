import React from "react";

import {userProfilePicUrl} from "../../utils/userProfilePicUrl";

export default function PublicationCreateFormAccountModal({user}) {
  return (
    <div className="modal fade" id="choose-account-modal" tabIndex={-1} aria-hidden="true">
      <div className="modal-dialog modal-dialog-centered modal-dialog-scrollable">
        <div className="modal-content rounded-5 p-4 text-center">
          <div className="modal-header border-0">
            <h3 className="modal-title">Выбрать аккаунт</h3>
            <button id="choose-account-modal-close-btn" type="button" className="btn-close" data-bs-dismiss="modal"
                    aria-label="Close"></button>
          </div>
          <div className="modal-body pt-2">
            <div className="d-flex justify-content-between align-items-center mb-3">
              <div className="account-choice border-primary">
                <img src={userProfilePicUrl(user)} className="profile-photo"/>
                <span className="fw-bold">{user.username}</span>
              </div>
              <span className="text-primary">
                  <i className="fa-solid fa-user-tie"></i>
                </span>
            </div>
            {/* TODO: for group in owned groups */}
            {/*<div class="d-flex justify-content-between align-items-center mb-3">*/}
            {/*  <div class="account-choice">*/}
            {/*    <img src="{{ group.get_profile_pic }}" class="profile-photo">*/}
            {/*      <span class="fw-bold">{group.groupname}</span>*/}
            {/*  </div>*/}
            {/*  <span class="text-muted">*/}
            {/*    <i class="fa-solid fa-user-group"></i>*/}
            {/*  </span>*/}
            {/*</div>*/}
          </div>
        </div>
      </div>
    </div>
  )
}