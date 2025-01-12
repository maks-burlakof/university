import PublicationCard from "../Publication/PublicationCard";
import React from "react";

export default function PublicationsCardView({ publications }) {
  return (
    <>
      {publications.length === 0 && (
        <span className="opacity-50 small d-flex justify-content-center mt-5 mb-5">
          Публикаций нет
        </span>
      )}
      <div className="row g-2">
        {publications.map((publication, index) => (
          <PublicationCard publication={publication}/>
        ))}
      </div>
    </>
  );
}