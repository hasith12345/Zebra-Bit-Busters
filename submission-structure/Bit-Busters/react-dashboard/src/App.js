import React, { useState, useEffect } from "react";
import Header from "./components/Header";
import SystemOverview from "./components/SystemOverview";
import EventTypes from "./components/EventTypes";
import StationStatus from "./components/StationStatus";
import RecentEvents from "./components/RecentEvents";
import SystemStatus from "./components/SystemStatus";
import SalesAnalytics from "./components/SalesAnalytics";
import InventoryInsights from "./components/InventoryInsights";
import CustomerBehavior from "./components/CustomerBehavior";
import BusinessSummary from "./components/BusinessSummary";
import Footer from "./components/Footer";
import "./index.css";

const API_BASE_URL = "http://localhost:3001/api";

function App() {
  const [dashboardData, setDashboardData] = useState({
    totalEvents: 0,
    activeStations: 0,
    averageEfficiency: 0,
    eventTypes: [],
    stations: [],
    recentEvents: [],
    lastUpdated: new Date().toLocaleString(),
    systemStatus: {
      rfid_events: 0,
      pos_events: 0,
      queue_events: 0,
      recognition_events: 0,
    },
    isConnected: false,
  });

  const [connectionStatus, setConnectionStatus] = useState("connecting");

  // Fetch dashboard data from API
  const fetchDashboardData = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/dashboard`);
      if (response.ok) {
        const data = await response.json();
        setDashboardData((prevData) => ({
          ...data,
          isConnected: !data.error,
        }));
        setConnectionStatus(data.error ? "disconnected" : "connected");
      } else {
        throw new Error(`HTTP ${response.status}`);
      }
    } catch (error) {
      console.warn("Failed to fetch dashboard data:", error.message);
      setConnectionStatus("disconnected");
      // Keep existing data but mark as disconnected
      setDashboardData((prevData) => ({
        ...prevData,
        isConnected: false,
        lastUpdated: new Date().toLocaleString(),
      }));
    }
  };

  // Initial data fetch and setup auto-refresh
  useEffect(() => {
    // Fetch data immediately
    fetchDashboardData();

    // Set up auto-refresh every 3 seconds
    const interval = setInterval(fetchDashboardData, 3000);

    return () => clearInterval(interval);
  }, []);

  // Show connection status in UI
  const getConnectionIndicator = () => {
    switch (connectionStatus) {
      case "connected":
        return {
          color: "text-green-400",
          text: "LIVE",
          status: "Connected to Sentinel System",
        };
      case "disconnected":
        return {
          color: "text-red-400",
          text: "OFFLINE",
          status: "Disconnected - Showing last known data",
        };
      default:
        return {
          color: "text-yellow-400",
          text: "CONNECTING",
          status: "Connecting to Sentinel System...",
        };
    }
  };

  const connectionInfo = getConnectionIndicator();

  return (
    <div className="min-h-screen bg-gradient-main">
      <div className="p-6">
        {/* Connection Status Banner */}
        {connectionStatus !== "connected" && (
          <div
            className={`text-center p-3 mb-4 rounded-lg ${
              connectionStatus === "disconnected"
                ? "bg-red-900 bg-opacity-50"
                : "bg-yellow-900 bg-opacity-50"
            }`}
          >
            <span className={`font-semibold ${connectionInfo.color}`}>
              {connectionInfo.status}
            </span>
          </div>
        )}

        <Header
          lastUpdated={dashboardData.lastUpdated}
          connectionStatus={connectionStatus}
          connectionInfo={connectionInfo}
        />

        {/* System Overview Row */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
          <SystemOverview
            totalEvents={dashboardData.totalEvents}
            activeStations={dashboardData.activeStations}
            averageEfficiency={dashboardData.averageEfficiency}
          />
          <EventTypes eventTypes={dashboardData.eventTypes} />
          <StationStatus stations={dashboardData.stations} />
        </div>

        {/* Business Analytics Row */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          <SalesAnalytics />
          <InventoryInsights />
        </div>

        {/* Customer & Business Intelligence Row */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          <CustomerBehavior />
          <BusinessSummary />
        </div>

        {/* System Status Row */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
          <RecentEvents events={dashboardData.recentEvents} />
          <SystemStatus
            totalEvents={dashboardData.totalEvents}
            systemStatus={dashboardData.systemStatus}
            connectionStatus={connectionStatus}
          />
        </div>

        <Footer />
      </div>
    </div>
  );
}

export default App;
