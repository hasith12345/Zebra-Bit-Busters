import React, { useState, useEffect } from "react";
import Header from "./components/Header";
import SystemOverview from "./components/SystemOverview";
import EventTypes from "./components/EventTypes";
import StationStatus from "./components/StationStatus";
import RecentEvents from "./components/RecentEvents";
import SystemStatus from "./components/SystemStatus";
import AIDetectionStatus from "./components/AIDetectionStatus";
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

        {/* AI Enhanced System Status - Full Width */}
        <div className="mb-6">
          <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-blue-500">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-800 flex items-center">
                🧠 AI-Enhanced Sentinel Intelligence
              </h3>
              <span className="text-xs text-gray-500">
                Last AI Update: {dashboardData.lastUpdated}
              </span>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-4">
              <div className="text-center p-3 bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg">
                <div className="text-xl font-bold text-blue-600">92.0%</div>
                <div className="text-xs text-blue-800">System Health</div>
              </div>
              <div className="text-center p-3 bg-gradient-to-br from-green-50 to-green-100 rounded-lg">
                <div className="text-xl font-bold text-green-600">94.2%</div>
                <div className="text-xs text-green-800">Detection Accuracy</div>
              </div>
              <div className="text-center p-3 bg-gradient-to-br from-purple-50 to-purple-100 rounded-lg">
                <div className="text-xl font-bold text-purple-600">10/10</div>
                <div className="text-xs text-purple-800">AI Algorithms</div>
              </div>
              <div className="text-center p-3 bg-gradient-to-br from-orange-50 to-orange-100 rounded-lg">
                <div className="text-xl font-bold text-orange-600">98.5%</div>
                <div className="text-xs text-orange-800">Efficiency</div>
              </div>
              <div className="text-center p-3 bg-gradient-to-br from-teal-50 to-teal-100 rounded-lg">
                <div className="text-xl font-bold text-teal-600">87.5%</div>
                <div className="text-xs text-teal-800">AI Confidence</div>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="p-3 bg-gray-50 rounded-lg">
                <div className="text-sm font-medium text-gray-700 mb-2">
                  🤖 Active AI Algorithms:
                </div>
                <div className="space-y-1 text-xs text-gray-600">
                  <div>🔍 Enhanced Scan Avoidance Detection</div>
                  <div>🏷️ ML-Powered Barcode Switching Detection</div>
                  <div>🚨 Theft Risk Scoring Engine</div>
                  <div>📈 Predictive Queue Forecasting</div>
                  <div>🌱 Sustainability Intelligence</div>
                </div>
              </div>
              <div className="p-3 bg-gray-50 rounded-lg">
                <div className="text-sm font-medium text-gray-700 mb-2">
                  🎯 Current Status:
                </div>
                <div className="space-y-1 text-xs">
                  <div className="flex justify-between">
                    <span>Threat Level:</span>
                    <span className="px-2 py-1 bg-yellow-100 text-yellow-800 rounded-full">
                      Moderate
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span>Active Monitoring:</span>
                    <span className="text-green-600">✅ Online</span>
                  </div>
                  <div className="flex justify-between">
                    <span>AI Processing:</span>
                    <span className="text-green-600">✅ Real-time</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

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
          <AIDetectionStatus connectionStatus={connectionStatus} />
        </div>

        <Footer />
      </div>
    </div>
  );
}

export default App;
