export default function BaseExploreButtons({currentEntities}) {
  return (
    <div class="d-flex justify-content-center align-items-center mt-1 mb-4">
      <a
        href="/explore/posts/"
        class={`btn text-bg-gray rounded-pill me-2 ${currentEntities === 'posts' && "border border-secondary"}`}
      >
        Публикации
      </a>
      <a
        href="/explore/users/"
        class={`btn text-bg-gray rounded-pill me-2 ${currentEntities === 'users' && "border border-secondary"}`}
      >
        Профили
      </a>
      {/*<a*/}
      {/*  href="/explore/groups/"*/}
      {/*  class={`btn text-bg-gray rounded-pill me-2 ${currentEntities === 'groups' && "border border-secondary"}`}*/}
      {/*>*/}
      {/*  Сообщества*/}
      {/*</a>*/}
    </div>
  );
}