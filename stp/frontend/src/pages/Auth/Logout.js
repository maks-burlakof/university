import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

export default function Logout() {
  const navigate = useNavigate();

  useEffect(() => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');

    navigate('/login');
  }, [navigate]);

  return null;
}