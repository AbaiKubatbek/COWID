# CowID Frontend - React Application

Modern React-based frontend for the CowID cow face recognition system with real-time camera integration and mobile support.

## Features

✨ **Core Features**
- 🔍 Cow face recognition from uploaded images
- 📷 Real-time camera capture for instant recognition
- 📋 Complete medical records management
- ⚙️ Admin panel for cow database management
- 💊 Insemination tracking and medical history
- 📱 Fully responsive mobile-first design
- 🔐 Secure API communication

## Tech Stack

- **Framework:** React 18.2
- **State Management:** Zustand
- **Styling:** Tailwind CSS
- **HTTP Client:** Axios
- **Build Tool:** Vite 5
- **Routing:** React Router v6
- **UI Pattern:** Component-based architecture

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── AdminPanel.jsx           # Cow management interface
│   │   ├── RecognitionForm.jsx      # Recognition UI with camera
│   │   ├── MedicalCard.jsx          # Cow medical records display
│   │   ├── CameraModal.jsx          # Camera capture modal
│   │   └── InseminationForm.jsx     # Insemination data form
│   ├── pages/                       # Page components
│   ├── services/
│   │   └── api.js                   # API client
│   ├── store/
│   │   └── store.js                 # Zustand state management
│   ├── utils/
│   │   └── cameraUtils.js           # Camera handling utilities
│   ├── App.jsx                      # Main app component
│   ├── main.jsx                     # Entry point
│   └── index.css                    # Global styles
├── public/                          # Static assets
├── package.json                     # Dependencies
├── vite.config.js                  # Vite configuration
├── vercel.json                     # Vercel deployment config
├── netlify.toml                    # Netlify deployment config
├── .env.example                    # Environment variables template
└── Dockerfile.prod                 # Production Docker image
```

## Getting Started

### Prerequisites
- Node.js 18+ and npm
- Backend API running on `http://localhost:8000`

### Installation

```bash
# Install dependencies
npm install

# Create environment file
cp .env.example .env.local

# Update .env.local with your backend URL
VITE_API_URL=http://localhost:8000
```

### Development

```bash
# Start development server
npm run dev

# Open browser to http://localhost:5173
```

### Build for Production

```bash
# Build application
npm run build

# Preview production build locally
npm run preview
```

## Environment Variables

Create `.env.local` file:

```env
# Backend API URL
VITE_API_URL=http://localhost:8000

# Environment
VITE_ENV=development
```

For production, update `VITE_API_URL` to your deployed backend URL.

## Components Guide

### RecognitionForm
Handles cow face recognition with two input methods:
- File upload with preview
- Real-time camera capture
- Recognition results with confidence score

**Features:**
- Drag-and-drop file support
- Camera modal integration
- Medical record display
- Error handling

### AdminPanel
Complete CRUD interface for cow management:
- Cow list with search
- Add/edit/delete operations
- Medical record management
- Photo upload or camera capture
- Insemination tracking

**Features:**
- Responsive grid layout
- Photo preview
- Validation
- Loading states
- Error messages

### MedicalCard
Displays comprehensive cow information:
- Basic details (breed, age, weight)
- Photo display
- **Insemination status and date**
- Medical history with timestamps
- Record type categorization

### CameraModal
Reusable camera capture component:
- Real-time video preview
- Photo capture
- Preview and confirmation
- Mobile optimized
- Error handling

## Styling & Responsiveness

### Mobile-First Approach
- Minimum button size: 44x44px for touch targets
- Large input fields (44px height)
- Font size: 16px on inputs to prevent iOS zoom
- Flexible layouts using flexbox and grid

### Breakpoints
- Mobile: < 640px
- Tablet: 640px - 1024px
- Desktop: > 1024px

### Color Scheme
- **Primary:** Dark green (#0B3D2E)
- **Secondary:** Green shades (#0B8043, #2E7D32)
- **Accent:** Various greens for status indicators
- **Text:** Gray shades for hierarchy

## API Integration

### Endpoints Used
- `GET /api/cows` - Fetch all cows
- `POST /api/cows` - Create new cow
- `PUT /api/cows/{id}` - Update cow
- `DELETE /api/cows/{id}` - Delete cow
- `POST /api/recognize` - Recognize cow from image
- `POST /api/medical-records` - Add medical record

### Error Handling
All API calls include error handling with user-friendly messages and automatic retry on network failures.

## Camera Integration

### Requirements
- HTTPS in production (camera requires secure context)
- User permission grant
- Modern browser with WebRTC support

### Supported Browsers
- Chrome 75+
- Firefox 70+
- Safari 12.1+
- Edge 79+

### Mobile Support
- iOS 14.5+ (must use camera button, not file upload)
- Android 5+ with Chrome

## State Management (Zustand)

Centralized state for:
- Current page navigation
- Cow list and current selection
- Recognition results
- User interface states

Access store:
```javascript
import { useUIStore, useCowStore, useRecognitionStore } from './store/store';

const { currentPage, setCurrentPage } = useUIStore();
```

## Deployment

### Vercel (Recommended)
```bash
npm run deploy:vercel
```

### Netlify
```bash
npm run deploy:netlify
```

### Docker
```bash
docker build -f Dockerfile.prod -t cowid-frontend .
docker run -p 3000:3000 cowid-frontend
```

See [DEPLOYMENT.md](../DEPLOYMENT.md) for detailed instructions.

## Performance Optimization

- Code splitting with React.lazy
- Image optimization with proper formats
- CSS-in-JS with Tailwind for smaller bundle
- Caching strategies for API calls

## Testing

```bash
# Run linter
npm run lint

# Future: Add test command
npm run test
```

## Browser Support

| Browser | Version | Support |
|---------|---------|---------|
| Chrome | 90+ | ✅ Full |
| Firefox | 88+ | ✅ Full |
| Safari | 14+ | ✅ Full |
| Edge | 90+ | ✅ Full |
| Mobile Safari | 14+ | ✅ Full |

## Troubleshooting

### Camera Not Working
- Check HTTPS is enabled (required for camera)
- Verify browser permissions
- Test in different browser
- Check console for errors

### API Connection Issues
- Verify backend is running
- Check `VITE_API_URL` in .env
- Verify CORS configuration on backend
- Check network tab for failed requests

### Build Errors
```bash
# Clear cache and reinstall
rm -rf node_modules
npm install
npm run build
```

## Development Scripts

```bash
npm run dev              # Start development server
npm run build            # Build for production
npm run preview          # Preview production build
npm run lint             # Run ESLint
npm run deploy:vercel    # Deploy to Vercel
npm run deploy:netlify   # Deploy to Netlify
npm run start            # Alternative to dev
npm run serve            # Alternative to preview
```

## Code Quality

- **Linting:** ESLint with React plugin
- **Formatting:** Consistent with Prettier
- **Naming:** Clear, descriptive component/function names
- **Comments:** JSDoc for complex functions
- **Components:** Functional with hooks
- **Files:** One component per file

## Security

- API communication over HTTPS in production
- Sensitive data not stored in localStorage without encryption
- XSS protection via React's automatic escaping
- CSRF tokens for state-changing operations
- Input validation before API calls

## Contributing

1. Create feature branch: `git checkout -b feature/your-feature`
2. Make changes with clear commits
3. Test thoroughly
4. Create pull request
5. Ensure linter passes: `npm run lint`

## License

Project license - See LICENSE file

## Support

For issues or questions:
1. Check troubleshooting section
2. Review error console
3. Check API backend logs
4. Open GitHub issue with details

---

**Last Updated:** February 2026
**Version:** 1.0.0
**Status:** Production Ready ✅
