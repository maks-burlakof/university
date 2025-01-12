import BasePublication from "../Base/BasePublication";
import UserPublicationOwnerLink from "./UserPublicationOwnerLink";

export default function UserPublication({publication}) {
  return (
    <BasePublication
      publication={publication}
      publicationOwnerLink={<UserPublicationOwnerLink publication={publication} />}
    />
  )
}