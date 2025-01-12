export default function BaseProfileButtons() {
  return (
    <>
      <button
        id="buttonRecommendedItems"
        className="btn btn-sm rounded-pill text-bg-gray me-2"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#collapseRecommendedItems"
        aria-expanded="false"
        aria-controls="collapseRecommendedItems"
      >
        <i className="fa-solid fa-user-plus"></i>
      </button>
      <a
        className="btn btn-sm rounded-pill text-bg-gray"
        data-bs-toggle="modal"
        data-bs-target="#post-share-modal"
        data-type="user"
        data-username={`username`}
      >
        <i className="fa-solid fa-arrow-up-from-bracket"></i>
      </a>
    </>
  )
}