import React from "react";

import {useUser} from "../../context/UserContext";

import PostCreateInjectedScripts from "../../components/Publications/PostCreateInjectedScripts";
import {userProfilePicUrl} from "../../utils/userProfilePicUrl";
import PublicationCreateForm from "../../components/Publication/PublicationCreateForm";
import PublicationCreateFormAccountModal from "../../components/Publication/PublicationCreateFormAccountModal";
import LoaderFullSpace from "../../components/Loaders/LoaderFullSpace";


export default function PostCreatePage() {
  const user = useUser();

  if (!user) {
    return <LoaderFullSpace />;
  }

  return (
    <>
      <style> {`
        body {
            overflow: hidden;
        }
        .container {
            padding: 0!important;
            margin: 0!important;
        }
        #content-top-padding {
            padding: 0!important;
            margin: 0!important;
        }
        .account-choice {
            cursor: pointer;
            display: flex;
            align-items: center;
            border-radius: 1rem;
            border: 2px solid #dee2e6;
            padding: 1rem;
        }
        .account-choice img {
            width: 30px;
            height: 30px;
            margin-right: 1rem;
        }
      `} </style>
      <div className="position-absolute top-50 start-50 translate-middle w-100">
        <div className="text-center mb-3">
          <h1 className="fw-bold text-body-tertiary">СОЗДАТЬ ПУБЛИКАЦИЮ</h1>
        </div>
        <PublicationCreateForm user={user}/>
      </div>
      <div className="wrapper" id="wrapper"></div>
      {/*<div dangerouslySetInnerHTML={{__html: PostCreateInjectedScripts()}}/>*/}
      <PostCreateInjectedScripts />
      <PublicationCreateFormAccountModal user={user}/>
    </>
  )
}