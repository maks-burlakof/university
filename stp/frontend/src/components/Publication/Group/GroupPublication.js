import BasePublication from "../Base/BasePublication";
import GroupPublicationOwnerLink from "./GroupPublicationOwnerLink";

export default function GroupPublication({publication}) {
  return (
    <BasePublication
      publication={publication}
      publicationOwnerLink={<GroupPublicationOwnerLink publication={publication} />}
    />
  )
}