# Project Sentinel - React Dashboard

A modern React-based dashboard for the Project Sentinel retail intelligence system, converted from the original HTML/Python implementation to use React with Tailwind CSS.

## Features

- **Real-time Dashboard**: Live updates every 3 seconds showing system status and events
- **Responsive Design**: Built with Tailwind CSS for mobile and desktop compatibility
- **Component-based Architecture**: Modular React components for maintainability
- **Live Animations**: Pulse effects and smooth transitions for better UX
- **Event Monitoring**: Real-time display of system events, station status, and AI detection capabilities

## Components

- **Header**: Main dashboard title with live indicator
- **SystemOverview**: Key metrics (total events, active stations, efficiency)
- **EventTypes**: Visual breakdown of different event types with progress bars
- **StationStatus**: Individual station monitoring with efficiency indicators
- **RecentEvents**: Scrollable list of recent system events
- **SystemStatus**: Overall system health indicators
- **AIDetectionStatus**: List of active AI detection capabilities
- **Footer**: Branding and live status indicator

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn

### Installation

1. Navigate to the dashboard directory:
   ```bash
   cd react-dashboard
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

4. Open [http://localhost:3000](http://localhost:3000) to view the dashboard in your browser.

### Build for Production

```bash
npm run build
```

This creates a `build` folder with production-ready files.

## Project Structure

```
src/
├── components/
│   ├── Header.js
│   ├── SystemOverview.js
│   ├── EventTypes.js
│   ├── StationStatus.js
│   ├── RecentEvents.js
│   ├── SystemStatus.js
│   ├── AIDetectionStatus.js
│   └── Footer.js
├── App.js
├── index.js
└── index.css
```

## Data Integration

The dashboard currently uses mock data for demonstration. To integrate with real data:

1. Replace the mock data in `App.js` with API calls
2. Add axios or fetch requests to your backend endpoints
3. Update the auto-refresh mechanism to fetch live data

Example integration:

```javascript
useEffect(() => {
  const fetchData = async () => {
    try {
      const response = await fetch('/api/dashboard-data');
      const data = await response.json();
      setDashboardData(data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  fetchData();
  const interval = setInterval(fetchData, 3000);
  return () => clearInterval(interval);
}, []);
```

## Styling

This project uses Tailwind CSS for styling. Key features:

- **Gradient Background**: Custom gradient background matching the original design
- **Glass Morphism**: Semi-transparent cards with backdrop blur effects
- **Responsive Grid**: Auto-adjusting layout for different screen sizes
- **Animations**: Pulse effects for live indicators and smooth transitions

## Customization

### Colors

Update the color scheme in `tailwind.config.js`:

```javascript
theme: {
  extend: {
    colors: {
      'custom-blue': '#2563eb',
      'custom-green': '#059669',
      // Add more custom colors
    }
  }
}
```

### Layout

Modify the grid layout in `App.js` to adjust component positioning:

```javascript
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
  {/* Components */}
</div>
```

## Performance

- Components are optimized with React best practices
- Auto-refresh intervals are properly cleaned up
- Efficient state updates prevent unnecessary re-renders

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is part of the Project Sentinel system developed by Team Bit-Busters.