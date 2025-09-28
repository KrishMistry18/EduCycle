import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { refreshToken } from '../store/slices/authSlice';

export const useAuth = () => {
  const dispatch = useDispatch();
  const { isAuthenticated, token, loading } = useSelector(state => state.auth);

  const checkAuthStatus = async () => {
    const accessToken = localStorage.getItem('access_token');
    const refreshTokenValue = localStorage.getItem('refresh_token');
    
    if (accessToken && refreshTokenValue) {
      try {
        await dispatch(refreshToken()).unwrap();
      } catch (error) {
        // Token refresh failed, clear tokens
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
      }
    }
  };

  useEffect(() => {
    checkAuthStatus();
  }, []);

  return {
    isAuthenticated,
    token,
    loading,
    checkAuthStatus,
  };
};
