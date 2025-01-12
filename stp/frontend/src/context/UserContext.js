import React, { createContext, useState, useEffect, useContext } from 'react';
import { useNavigate } from 'react-router-dom';

const UserContext = createContext(null);

export const UserProvider = ({ children }) => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/user/me`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          },
        });

        if (response.ok) {
          const data = await response.json();
          setUser(data);
        } else if (response.status === 401) {
          // Access token expired, try to refresh it
          const refreshResponse = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/auth/login/refresh`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              refresh: localStorage.getItem('refresh_token'),
            }),
          });

          if (refreshResponse.ok) {
            const refreshData = await refreshResponse.json();
            localStorage.setItem('access_token', refreshData['access']);
            localStorage.setItem('refresh_token', refreshData['refresh']);

            // Retry fetching the user with the new access token
            const retryResponse = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/user/me`, {
              headers: {
                'Authorization': `Bearer ${refreshData['access']}`,
              },
            });

            if (retryResponse.ok) {
              const data = await retryResponse.json();
              setUser(data);
            } else {
              navigate('/login');
              setUser(null);
            }
          } else {
            setUser(null);
          }
        } else {
          setUser(null);
        }
      } catch (error) {
        setUser(null);
      }
    };

    fetchUser();
  }, []);

  return (
    <UserContext.Provider value={user}>
      {children}
    </UserContext.Provider>
  );
};

export const useUser = () => {
  return useContext(UserContext);
};