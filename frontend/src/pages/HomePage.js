import React, { useEffect } from 'react';
import {
  Box,
  Typography,
  Button,
  Grid,
  Card,
  CardContent,
  CardMedia,
  Container,
  Paper,
  Chip,
} from '@mui/material';
import {
  Search as SearchIcon,
  Sell as SellIcon,
  Security as SecurityIcon,
  Support as SupportIcon,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { fetchItems } from '../store/slices/itemsSlice';

const HomePage = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { items, loading } = useSelector(state => state.items);
  const { isAuthenticated } = useSelector(state => state.auth);

  useEffect(() => {
    // Fetch featured items
    dispatch(fetchItems({ limit: 6 }));
  }, [dispatch]);

  const features = [
    {
      icon: <SearchIcon sx={{ fontSize: 40 }} />,
      title: 'Easy Search',
      description: 'Find exactly what you need with our advanced search and filtering system.',
    },
    {
      icon: <SellIcon sx={{ fontSize: 40 }} />,
      title: 'Sell Your Items',
      description: 'Turn your unused items into cash. List items easily and securely.',
    },
    {
      icon: <SecurityIcon sx={{ fontSize: 40 }} />,
      title: 'Secure Transactions',
      description: 'Safe and secure payment processing with buyer and seller protection.',
    },
    {
      icon: <SupportIcon sx={{ fontSize: 40 }} />,
      title: '24/7 Support',
      description: 'Get help whenever you need it with our comprehensive support system.',
    },
  ];

  const featuredItems = items.slice(0, 6);

  return (
    <Box>
      {/* Hero Section */}
      <Paper
        sx={{
          position: 'relative',
          backgroundColor: 'grey.800',
          color: '#fff',
          mb: 4,
          backgroundSize: 'cover',
          backgroundRepeat: 'no-repeat',
          backgroundPosition: 'center',
          backgroundImage: 'url(https://source.unsplash.com/random?university)',
        }}
      >
        <Box
          sx={{
            position: 'absolute',
            top: 0,
            bottom: 0,
            right: 0,
            left: 0,
            backgroundColor: 'rgba(0,0,0,.3)',
          }}
        />
        <Grid container>
          <Grid item md={6}>
            <Box
              sx={{
                position: 'relative',
                p: { xs: 3, md: 6 },
                pr: { md: 0 },
              }}
            >
              <Typography variant="h2" color="inherit" gutterBottom>
                Welcome to EduCycle
              </Typography>
              <Typography variant="h5" color="inherit" paragraph>
                The student marketplace where you can buy, sell, and trade items with fellow students.
                Save money and reduce waste by giving items a second life.
              </Typography>
              <Box sx={{ mt: 4 }}>
                <Button
                  variant="contained"
                  size="large"
                  onClick={() => navigate('/items')}
                  sx={{ mr: 2, mb: 2 }}
                >
                  Browse Items
                </Button>
                {!isAuthenticated && (
                  <Button
                    variant="outlined"
                    size="large"
                    onClick={() => navigate('/register')}
                    sx={{ mb: 2 }}
                  >
                    Join Now
                  </Button>
                )}
              </Box>
            </Box>
          </Grid>
        </Grid>
      </Paper>

      {/* Features Section */}
      <Container maxWidth="lg" sx={{ mb: 8 }}>
        <Typography variant="h3" component="h2" gutterBottom align="center" sx={{ mb: 6 }}>
          Why Choose EduCycle?
        </Typography>
        <Grid container spacing={4}>
          {features.map((feature, index) => (
            <Grid item xs={12} sm={6} md={3} key={index}>
              <Card sx={{ height: '100%', textAlign: 'center' }}>
                <CardContent>
                  <Box sx={{ color: 'primary.main', mb: 2 }}>
                    {feature.icon}
                  </Box>
                  <Typography variant="h6" component="h3" gutterBottom>
                    {feature.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {feature.description}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Container>

      {/* Featured Items Section */}
      <Container maxWidth="lg" sx={{ mb: 8 }}>
        <Typography variant="h3" component="h2" gutterBottom align="center" sx={{ mb: 6 }}>
          Featured Items
        </Typography>
        <Grid container spacing={4}>
          {featuredItems.map((item) => (
            <Grid item xs={12} sm={6} md={4} key={item.id}>
              <Card 
                sx={{ 
                  height: '100%', 
                  cursor: 'pointer',
                  transition: 'transform 0.2s',
                  '&:hover': {
                    transform: 'translateY(-4px)',
                  },
                }}
                onClick={() => navigate(`/items/${item.id}`)}
              >
                <CardMedia
                  component="img"
                  height="200"
                  image={item.image1 || 'https://source.unsplash.com/random?item'}
                  alt={item.name}
                />
                <CardContent>
                  <Typography variant="h6" component="h3" gutterBottom>
                    {item.name}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" paragraph>
                    {item.description.length > 100 
                      ? `${item.description.substring(0, 100)}...` 
                      : item.description}
                  </Typography>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Chip label={item.category} size="small" color="primary" />
                    <Typography variant="h6" color="primary">
                      ₹{item.price}
                    </Typography>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
        <Box sx={{ textAlign: 'center', mt: 4 }}>
          <Button
            variant="outlined"
            size="large"
            onClick={() => navigate('/items')}
          >
            View All Items
          </Button>
        </Box>
      </Container>

      {/* Call to Action */}
      <Paper sx={{ bgcolor: 'primary.main', color: 'white', py: 8 }}>
        <Container maxWidth="md">
          <Typography variant="h3" component="h2" gutterBottom align="center">
            Ready to Start?
          </Typography>
          <Typography variant="h6" align="center" paragraph>
            Join thousands of students who are already buying and selling on EduCycle.
          </Typography>
          <Box sx={{ textAlign: 'center', mt: 4 }}>
            {!isAuthenticated ? (
              <>
                <Button
                  variant="contained"
                  size="large"
                  onClick={() => navigate('/register')}
                  sx={{ mr: 2, mb: 2 }}
                >
                  Get Started
                </Button>
                <Button
                  variant="outlined"
                  size="large"
                  onClick={() => navigate('/login')}
                  sx={{ mb: 2 }}
                >
                  Sign In
                </Button>
              </>
            ) : (
              <Button
                variant="contained"
                size="large"
                onClick={() => navigate('/items/create')}
              >
                Sell Your First Item
              </Button>
            )}
          </Box>
        </Container>
      </Paper>
    </Box>
  );
};

export default HomePage;
