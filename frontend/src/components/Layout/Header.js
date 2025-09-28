import React, { useState } from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  IconButton,
  Box,
  Badge,
  Menu,
  MenuItem,
  Avatar,
  InputBase,
  alpha,
} from '@mui/material';
import {
  Search as SearchIcon,
  ShoppingCart as CartIcon,
  Notifications as NotificationsIcon,
  Brightness4 as DarkIcon,
  Brightness7 as LightIcon,
  Menu as MenuIcon,
  AccountCircle,
} from '@mui/icons-material';
import { useNavigate, Link } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import { styled } from '@mui/material/styles';

// Redux actions
import { logoutUser } from '../../store/slices/authSlice';
import { toggleDarkMode, toggleSidebar } from '../../store/slices/uiSlice';

// Styled components
const Search = styled('div')(({ theme }) => ({
  position: 'relative',
  borderRadius: theme.shape.borderRadius,
  backgroundColor: alpha(theme.palette.common.white, 0.15),
  '&:hover': {
    backgroundColor: alpha(theme.palette.common.white, 0.25),
  },
  marginRight: theme.spacing(2),
  marginLeft: 0,
  width: '100%',
  [theme.breakpoints.up('sm')]: {
    marginLeft: theme.spacing(3),
    width: 'auto',
  },
}));

const SearchIconWrapper = styled('div')(({ theme }) => ({
  padding: theme.spacing(0, 2),
  height: '100%',
  position: 'absolute',
  pointerEvents: 'none',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
}));

const StyledInputBase = styled(InputBase)(({ theme }) => ({
  color: 'inherit',
  '& .MuiInputBase-input': {
    padding: theme.spacing(1, 1, 1, 0),
    paddingLeft: `calc(1em + ${theme.spacing(4)})`,
    transition: theme.transitions.create('width'),
    width: '100%',
    [theme.breakpoints.up('md')]: {
      width: '20ch',
    },
  },
}));

const Header = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { isAuthenticated, user } = useSelector(state => state.auth);
  const { darkMode } = useSelector(state => state.ui);
  const { totalItems } = useSelector(state => state.cart);
  const { unreadNotifications } = useSelector(state => state.ui);

  const [anchorEl, setAnchorEl] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');

  const handleMenu = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    dispatch(logoutUser());
    handleClose();
    navigate('/');
  };

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/items?search=${encodeURIComponent(searchQuery.trim())}`);
    }
  };

  const handleToggleDarkMode = () => {
    dispatch(toggleDarkMode());
  };

  const handleToggleSidebar = () => {
    dispatch(toggleSidebar());
  };

  return (
    <AppBar position="sticky" elevation={1}>
      <Toolbar>
        {/* Mobile Menu Button */}
        <IconButton
          edge="start"
          color="inherit"
          aria-label="menu"
          sx={{ mr: 2, display: { sm: 'none' } }}
          onClick={handleToggleSidebar}
        >
          <MenuIcon />
        </IconButton>

        {/* Logo */}
        <Typography
          variant="h6"
          component={Link}
          to="/"
          sx={{
            flexGrow: { xs: 1, sm: 0 },
            textDecoration: 'none',
            color: 'inherit',
            fontWeight: 'bold',
          }}
        >
          EduCycle
        </Typography>

        {/* Search Bar */}
        <Box sx={{ flexGrow: 1, display: { xs: 'none', md: 'flex' }, mx: 4 }}>
          <Search>
            <SearchIconWrapper>
              <SearchIcon />
            </SearchIconWrapper>
            <form onSubmit={handleSearch}>
              <StyledInputBase
                placeholder="Search items..."
                inputProps={{ 'aria-label': 'search' }}
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </form>
          </Search>
        </Box>

        {/* Navigation Links */}
        <Box sx={{ display: { xs: 'none', sm: 'flex' }, alignItems: 'center' }}>
          <Button
            color="inherit"
            component={Link}
            to="/items"
            sx={{ mx: 1 }}
          >
            Browse
          </Button>
          
          {isAuthenticated && (
            <Button
              color="inherit"
              component={Link}
              to="/items/create"
              sx={{ mx: 1 }}
            >
              Sell
            </Button>
          )}
        </Box>

        {/* Right Side Icons */}
        <Box sx={{ display: 'flex', alignItems: 'center', ml: 'auto' }}>
          {/* Dark Mode Toggle */}
          <IconButton color="inherit" onClick={handleToggleDarkMode}>
            {darkMode ? <LightIcon /> : <DarkIcon />}
          </IconButton>

          {/* Notifications */}
          {isAuthenticated && (
            <IconButton color="inherit" component={Link} to="/notifications">
              <Badge badgeContent={unreadNotifications} color="error">
                <NotificationsIcon />
              </Badge>
            </IconButton>
          )}

          {/* Cart */}
          {isAuthenticated && (
            <IconButton color="inherit" component={Link} to="/cart">
              <Badge badgeContent={totalItems} color="error">
                <CartIcon />
              </Badge>
            </IconButton>
          )}

          {/* User Menu */}
          {isAuthenticated ? (
            <Box sx={{ display: 'flex', alignItems: 'center', ml: 1 }}>
              <IconButton
                onClick={handleMenu}
                color="inherit"
                sx={{ ml: 1 }}
              >
                {user?.profile?.avatar ? (
                  <Avatar src={user.profile.avatar} sx={{ width: 32, height: 32 }} />
                ) : (
                  <AccountCircle />
                )}
              </IconButton>
              <Menu
                anchorEl={anchorEl}
                open={Boolean(anchorEl)}
                onClose={handleClose}
                anchorOrigin={{
                  vertical: 'bottom',
                  horizontal: 'right',
                }}
                transformOrigin={{
                  vertical: 'top',
                  horizontal: 'right',
                }}
              >
                <MenuItem onClick={() => { handleClose(); navigate('/profile'); }}>
                  Profile
                </MenuItem>
                <MenuItem onClick={() => { handleClose(); navigate('/orders'); }}>
                  My Orders
                </MenuItem>
                <MenuItem onClick={() => { handleClose(); navigate('/items/create'); }}>
                  Sell Item
                </MenuItem>
                <MenuItem onClick={handleLogout}>
                  Logout
                </MenuItem>
              </Menu>
            </Box>
          ) : (
            <Box sx={{ display: 'flex', alignItems: 'center', ml: 1 }}>
              <Button
                color="inherit"
                component={Link}
                to="/login"
                sx={{ mx: 1 }}
              >
                Login
              </Button>
              <Button
                variant="contained"
                color="secondary"
                component={Link}
                to="/register"
                sx={{ mx: 1 }}
              >
                Register
              </Button>
            </Box>
          )}
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
