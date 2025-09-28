import React, { useEffect } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import { Box, CssBaseline } from '@mui/material';
import { ThemeProvider, createTheme } from '@mui/material/styles';

// Components
import Layout from './components/Layout/Layout';
import ProtectedRoute from './components/Auth/ProtectedRoute';

// Pages
import HomePage from './pages/HomePage';
import LoginPage from './pages/Auth/LoginPage';
import RegisterPage from './pages/Auth/RegisterPage';
import ItemsPage from './pages/Items/ItemsPage';
import ItemDetailPage from './pages/Items/ItemDetailPage';
import CreateItemPage from './pages/Items/CreateItemPage';
import EditItemPage from './pages/Items/EditItemPage';
import CartPage from './pages/Cart/CartPage';
import CheckoutPage from './pages/Checkout/CheckoutPage';
import ProfilePage from './pages/Profile/ProfilePage';
import OrdersPage from './pages/Orders/OrdersPage';
import OrderDetailPage from './pages/Orders/OrderDetailPage';
import NotFoundPage from './pages/NotFoundPage';

// Redux actions
import { refreshToken } from './store/slices/authSlice';
import { fetchUserProfile } from './store/slices/userSlice';
import { fetchCart } from './store/slices/cartSlice';

// Hooks
import { useAuth } from './hooks/useAuth';

function App() {
  const dispatch = useDispatch();
  const { isAuthenticated, token } = useSelector(state => state.auth);
  const { darkMode } = useSelector(state => state.ui);
  const { checkAuthStatus } = useAuth();

  // Create theme based on dark mode
  const theme = createTheme({
    palette: {
      mode: darkMode ? 'dark' : 'light',
      primary: {
        main: '#1976d2',
        light: '#42a5f5',
        dark: '#1565c0',
      },
      secondary: {
        main: '#dc004e',
        light: '#ff5983',
        dark: '#9a0036',
      },
      background: {
        default: darkMode ? '#121212' : '#f5f5f5',
        paper: darkMode ? '#1e1e1e' : '#ffffff',
      },
    },
    typography: {
      fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    },
    components: {
      MuiButton: {
        styleOverrides: {
          root: {
            textTransform: 'none',
            borderRadius: 8,
          },
        },
      },
      MuiCard: {
        styleOverrides: {
          root: {
            borderRadius: 12,
            boxShadow: darkMode 
              ? '0 2px 8px rgba(255,255,255,0.1)' 
              : '0 2px 8px rgba(0,0,0,0.1)',
          },
        },
      },
    },
  });

  useEffect(() => {
    // Check authentication status on app load
    checkAuthStatus();
  }, [checkAuthStatus]);

  useEffect(() => {
    // Set up axios interceptor for token refresh
    const setupAxiosInterceptors = () => {
      const axios = require('axios');
      
      // Request interceptor to add auth token
      axios.interceptors.request.use(
        (config) => {
          const token = localStorage.getItem('access_token');
          if (token) {
            config.headers.Authorization = `Bearer ${token}`;
          }
          return config;
        },
        (error) => {
          return Promise.reject(error);
        }
      );

      // Response interceptor to handle token refresh
      axios.interceptors.response.use(
        (response) => response,
        async (error) => {
          const originalRequest = error.config;
          
          if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;
            
            try {
              await dispatch(refreshToken()).unwrap();
              const newToken = localStorage.getItem('access_token');
              originalRequest.headers.Authorization = `Bearer ${newToken}`;
              return axios(originalRequest);
            } catch (refreshError) {
              // Refresh failed, redirect to login
              window.location.href = '/login';
              return Promise.reject(refreshError);
            }
          }
          
          return Promise.reject(error);
        }
      );
    };

    setupAxiosInterceptors();
  }, [dispatch]);

  useEffect(() => {
    // Fetch user data if authenticated
    if (isAuthenticated && token) {
      dispatch(fetchUserProfile());
      dispatch(fetchCart());
    }
  }, [isAuthenticated, token, dispatch]);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
        <Layout>
          <Routes>
            {/* Public Routes */}
            <Route path="/" element={<HomePage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/items" element={<ItemsPage />} />
            <Route path="/items/:id" element={<ItemDetailPage />} />
            
            {/* Protected Routes */}
            <Route path="/profile" element={
              <ProtectedRoute>
                <ProfilePage />
              </ProtectedRoute>
            } />
            <Route path="/cart" element={
              <ProtectedRoute>
                <CartPage />
              </ProtectedRoute>
            } />
            <Route path="/checkout" element={
              <ProtectedRoute>
                <CheckoutPage />
              </ProtectedRoute>
            } />
            <Route path="/orders" element={
              <ProtectedRoute>
                <OrdersPage />
              </ProtectedRoute>
            } />
            <Route path="/orders/:id" element={
              <ProtectedRoute>
                <OrderDetailPage />
              </ProtectedRoute>
            } />
            <Route path="/items/create" element={
              <ProtectedRoute>
                <CreateItemPage />
              </ProtectedRoute>
            } />
            <Route path="/items/:id/edit" element={
              <ProtectedRoute>
                <EditItemPage />
              </ProtectedRoute>
            } />
            
            {/* Catch all route */}
            <Route path="*" element={<NotFoundPage />} />
          </Routes>
        </Layout>
      </Box>
    </ThemeProvider>
  );
}

export default App;
