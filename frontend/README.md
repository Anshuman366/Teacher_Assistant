# Teacher Assistant Bot - Frontend

React frontend for the Teacher Assistant Bot application.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Start development server:
```bash
npm start
```

Frontend runs on http://localhost:3000

## Build

Create production build:
```bash
npm run build
```

## Features

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Modern UI**: Beautiful gradient-based design
- **Real-time Chat**: Interactive chat interface
- **File Upload**: Drag-and-drop file uploads
- **Tab Navigation**: Easy switching between features

## File Structure

- `src/App.js` - Main application component
- `src/pages/` - Page components for each feature
- `src/components/` - Reusable UI components
- `src/api/` - Axios API client
- `src/index.css` - Global styles
- `public/` - Static assets

## API Integration

The frontend communicates with backend at:
```
http://localhost:8000/api
```

Configure in `.env`:
```
REACT_APP_API_URL=http://localhost:8000/api
```

## Available Scripts

- `npm start` - Run development server
- `npm build` - Create production build
- `npm test` - Run tests
- `npm eject` - Eject configuration (irreversible)

## Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge

## Customization

### Change Color Scheme
Edit `src/index.css` and modify:
```css
--primary-color: #667eea;
--secondary-color: #764ba2;
```

### Add New Pages
1. Create component in `src/pages/NewPage.js`
2. Add route in `src/App.js`
3. Add navigation link in `src/components/Sidebar.js`
