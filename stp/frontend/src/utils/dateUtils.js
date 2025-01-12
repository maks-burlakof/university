export function getTimeAgo(created) {
  const now = new Date();
  const createdDate = new Date(created);
  const diffInSeconds = Math.floor((now - createdDate) / 1000);
  const diffInDays = Math.floor(diffInSeconds / (60 * 60 * 24));

  if (diffInDays === 0) {
    if (diffInSeconds < 5) {
      return "только что";
    } else if (diffInSeconds < 60) {
      return `${diffInSeconds} сек.`;
    } else if (diffInSeconds < 60 * 60) {
      return `${Math.floor(diffInSeconds / 60)} мин.`;
    } else {
      return `${Math.floor(diffInSeconds / (60 * 60))} ч.`;
    }
  } else if (diffInDays === 1) {
    return "Вчера";
  } else if (diffInDays === 2) {
    return "Позавчера";
  } else {
    return `${diffInDays} дн.`;
  }
}

export function displayDate(date) {
  const dateObj = new Date(date);
  return dateObj.toLocaleString("ru", {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "numeric",
    minute: "numeric",
  });
}