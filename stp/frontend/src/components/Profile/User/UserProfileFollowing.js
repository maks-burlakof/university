import React from "react";

import {getRuPluralCount} from "../../../utils/getRuPluralCount";


export default function UserProfileFollowing({profileFollowingCount}) {
  return (
    <a className="common-link lh-sm" data-bs-toggle="modal" data-bs-target="#following-list">
      <strong>{profileFollowingCount}</strong> {getRuPluralCount(profileFollowingCount, ["подписка", "подписки", "подписок"])}
    </a>
  )
}