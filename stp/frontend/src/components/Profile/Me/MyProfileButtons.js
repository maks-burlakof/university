import BaseProfileButtons from "../Base/BaseProfileButtons";


export default function MyProfileButtons() {
  return (
    <>
      <a href="/user/edit" className="btn btn-sm text-bg-gray rounded-pill me-2">
        Редактировать
      </a>
      <BaseProfileButtons/>
      <a href="/logout" className="btn btn-sm text-bg-gray rounded-pill ms-2">
        <i className="fa-solid fa-right-from-bracket"></i>
      </a>
    </>
  );
}