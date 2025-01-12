export default function PublicationCard({ publication }) {
  return (
    <div className="col-4">
      <div className="post-image-only">
        <a href={`/post/${publication.id}`}>
          <img className="post-image-only" src={publication.image}/>
        </a>
        <div className="post-overlay">
          <i className="fa-solid fa-heart me-1"></i> {publication.likes_num}
          <i className="fa-solid fa-comment ms-3 me-1"></i> {publication.comments_num}
        </div>
      </div>
    </div>
  );
}