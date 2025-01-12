export const apiRequest = async (url, options = {}) => {
  const token = localStorage.getItem('access_token');

  const headers = {
    'Authorization': `Bearer ${token}`,
    ...options.headers,
  };

  if (options.body instanceof FormData) {
    delete headers['Content-Type'];
  } else {
    headers['Content-Type'] = 'application/json';
  }

  const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/${url}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    throw new Error('Network response was not ok');
  }

  if (response.status === 204) {
    return null;
  }
  return response.json();
};