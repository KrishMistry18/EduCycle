# EduCycle Frontend

A modern React frontend for the EduCycle student marketplace platform.

## Features

- **Modern React 18** with hooks and functional components
- **Material-UI (MUI)** for beautiful, responsive design
- **Redux Toolkit** for state management
- **React Router** for navigation
- **JWT Authentication** with automatic token refresh
- **Dark Mode** support
- **Responsive Design** for all devices
- **Real-time Features** (WebSocket ready)
- **Form Validation** with error handling
- **Toast Notifications** for user feedback

## Tech Stack

- React 18.2.0
- Material-UI 5.14.20
- Redux Toolkit 1.9.7
- React Router DOM 6.20.1
- Axios 1.6.2
- React Hot Toast 2.4.1
- Socket.io Client 4.7.4

## Getting Started

### Prerequisites

- Node.js 16+ 
- npm or yarn
- Backend Django server running on port 8000

### Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The app will open at [http://localhost:3000](http://localhost:3000).

### Available Scripts

- `npm start` - Start development server
- `npm build` - Build for production
- `npm test` - Run tests
- `npm eject` - Eject from Create React App

## Project Structure

```
frontend/
├── public/
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── Auth/           # Authentication components
│   │   ├── Layout/         # Layout components
│   │   └── ...
│   ├── pages/              # Page components
│   │   ├── Auth/           # Authentication pages
│   │   ├── Items/          # Item-related pages
│   │   ├── Cart/           # Cart pages
│   │   └── ...
│   ├── store/              # Redux store
│   │   ├── slices/         # Redux slices
│   │   └── index.js        # Store configuration
│   ├── hooks/              # Custom React hooks
│   ├── utils/              # Utility functions
│   ├── App.js              # Main app component
│   └── index.js            # App entry point
├── package.json
└── README.md
```

## Features Implemented

### ✅ Completed
- [x] JWT Authentication with automatic token refresh
- [x] Redux store with slices for auth, items, cart, user, UI
- [x] Material-UI theme with dark mode support
- [x] Responsive header with navigation
- [x] Modern homepage with hero section
- [x] Login page with form validation
- [x] Protected routes
- [x] Toast notifications
- [x] Error handling

### 🚧 In Progress
- [ ] Item listing and detail pages
- [ ] Cart functionality
- [ ] User profile management
- [ ] Order management
- [ ] Real-time chat
- [ ] Search and filtering

### 📋 Planned
- [ ] Registration page
- [ ] Item creation/editing forms
- [ ] Payment integration
- [ ] Image upload
- [ ] Advanced search
- [ ] Notifications system

## API Integration

The frontend communicates with the Django backend API:

- **Base URL**: `http://localhost:8000`
- **API Endpoints**: `/api/`
- **Authentication**: JWT tokens
- **CORS**: Configured for development

## Development

### Adding New Features

1. Create Redux slice for state management
2. Add API calls in the slice
3. Create React components
4. Add routing in App.js
5. Update navigation as needed

### Styling

- Use Material-UI components and styling
- Follow the established theme
- Use `sx` prop for component-specific styles
- Maintain responsive design

### State Management

- Use Redux Toolkit for global state
- Use React hooks for local state
- Follow Redux best practices
- Keep slices focused and modular

## Deployment

### Production Build

```bash
npm run build
```

### Environment Variables

Create `.env` file for environment-specific configuration:

```
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENVIRONMENT=development
```

## Contributing

1. Follow the established code structure
2. Use TypeScript for new components (optional)
3. Add proper error handling
4. Test on different screen sizes
5. Follow Material-UI design principles

## Troubleshooting

### Common Issues

1. **CORS errors**: Ensure backend CORS is configured
2. **API connection**: Check if Django server is running
3. **Build errors**: Clear node_modules and reinstall
4. **Hot reload not working**: Check file watchers

### Development Tips

- Use React DevTools for debugging
- Use Redux DevTools for state inspection
- Check browser console for errors
- Test authentication flow thoroughly

