import React, { useState, useEffect } from "react";

const AIInsights = () => {
  const [aiData, setAiData] = useState({
    threatDetection: {
      riskScore: 85,
      activeThreats: 2,
      highRiskCustomers: 3,
      totalEvents: 12,
    },
    predictiveAnalytics: {
      queueForecast: "Peak expected in 15 minutes",
      systemHealth: 92,
      inventoryAlerts: 4,
      staffingRecommendations: 2,
    },
    intelligentAutomation: {
      alertsSuppressed: 8,
      autoResolvedIssues: 15,
      detectionAccuracy: 94.2,
      processingEfficiency: 98.5,
    },
    recentInsights: [
      {
        id: 1,
        type: "Critical",
        message: "Coordinated fraud activity detected across 3 stations",
        confidence: 95,
        timestamp: new Date(Date.now() - 5 * 60000).toLocaleTimeString(),
      },
      {
        id: 2,
        type: "High",
        message: "Predictive queue congestion in 10 minutes at CHECKOUT-001",
        confidence: 87,
        timestamp: new Date(Date.now() - 8 * 60000).toLocaleTimeString(),
      },
      {
        id: 3,
        type: "Medium",
        message: "Energy optimization opportunity identified at SCO-003",
        confidence: 78,
        timestamp: new Date(Date.now() - 12 * 60000).toLocaleTimeString(),
      },
    ],
  });

  const [selectedInsight, setSelectedInsight] = useState(null);

  useEffect(() => {
    const fetchAIData = async () => {
      try {
        const response = await fetch("/api/ai-insights");
        if (response.ok) {
          const data = await response.json();
          setAiData(data);
        }
      } catch (error) {
        console.error("Error fetching AI insights:", error);
      }
    };

    fetchAIData();
    const interval = setInterval(fetchAIData, 15000); // Update every 15 seconds

    return () => clearInterval(interval);
  }, []);

  const getConfidenceColor = (confidence) => {
    if (confidence >= 90) return "text-green-500";
    if (confidence >= 80) return "text-yellow-500";
    return "text-red-500";
  };

  const getTypeColor = (type) => {
    switch (type) {
      case "Critical":
        return "bg-red-500 text-white";
      case "High":
        return "bg-orange-500 text-white";
      case "Medium":
        return "bg-yellow-500 text-black";
      case "Low":
        return "bg-green-500 text-white";
      default:
        return "bg-gray-500 text-white";
    }
  };

  const getRiskScoreColor = (score) => {
    if (score >= 80) return "text-red-500";
    if (score >= 60) return "text-yellow-500";
    return "text-green-500";
  };

  return (
    <div className="space-y-6">
      {/* AI Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white p-4 rounded-lg shadow-md border-l-4 border-red-500">
          <h3 className="text-sm font-medium text-gray-500 mb-1">
            Threat Detection
          </h3>
          <div className="flex items-center justify-between">
            <span
              className={`text-2xl font-bold ${getRiskScoreColor(
                aiData.threatDetection.riskScore
              )}`}
            >
              {aiData.threatDetection.riskScore}%
            </span>
            <div className="text-right text-xs text-gray-500">
              <div>🚨 {aiData.threatDetection.activeThreats} Active</div>
              <div>⚠️ {aiData.threatDetection.highRiskCustomers} High-Risk</div>
            </div>
          </div>
        </div>

        <div className="bg-white p-4 rounded-lg shadow-md border-l-4 border-blue-500">
          <h3 className="text-sm font-medium text-gray-500 mb-1">
            Predictive Analytics
          </h3>
          <div className="text-lg font-semibold text-blue-600 mb-1">
            {aiData.predictiveAnalytics.systemHealth}% Health
          </div>
          <div className="text-xs text-gray-600">
            📈 {aiData.predictiveAnalytics.queueForecast}
          </div>
        </div>

        <div className="bg-white p-4 rounded-lg shadow-md border-l-4 border-green-500">
          <h3 className="text-sm font-medium text-gray-500 mb-1">
            Detection Accuracy
          </h3>
          <div className="text-lg font-semibold text-green-600 mb-1">
            {aiData.intelligentAutomation.detectionAccuracy}%
          </div>
          <div className="text-xs text-gray-600">
            🤖 {aiData.intelligentAutomation.autoResolvedIssues} Auto-Resolved
          </div>
        </div>

        <div className="bg-white p-4 rounded-lg shadow-md border-l-4 border-purple-500">
          <h3 className="text-sm font-medium text-gray-500 mb-1">
            Processing Efficiency
          </h3>
          <div className="text-lg font-semibold text-purple-600 mb-1">
            {aiData.intelligentAutomation.processingEfficiency}%
          </div>
          <div className="text-xs text-gray-600">
            🔇 {aiData.intelligentAutomation.alertsSuppressed} Alerts Suppressed
          </div>
        </div>
      </div>

      {/* AI Insights Dashboard */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent AI Insights */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-800">
              🧠 AI Intelligence Feed
            </h3>
            <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded-full">
              Live Insights
            </span>
          </div>
          <div className="space-y-3 max-h-64 overflow-y-auto">
            {aiData.recentInsights.map((insight) => (
              <div
                key={insight.id}
                className={`p-3 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50 transition-colors ${
                  selectedInsight?.id === insight.id
                    ? "bg-blue-50 border-blue-300"
                    : ""
                }`}
                onClick={() => setSelectedInsight(insight)}
              >
                <div className="flex items-start justify-between mb-2">
                  <span
                    className={`text-xs px-2 py-1 rounded-full ${getTypeColor(
                      insight.type
                    )}`}
                  >
                    {insight.type}
                  </span>
                  <span className="text-xs text-gray-500">
                    {insight.timestamp}
                  </span>
                </div>
                <div className="text-sm text-gray-700 mb-2">
                  {insight.message}
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-xs text-gray-500">
                    Confidence:{" "}
                    <span className={getConfidenceColor(insight.confidence)}>
                      {insight.confidence}%
                    </span>
                  </span>
                  <span className="text-xs text-blue-600 hover:text-blue-800">
                    View Details →
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* AI Capabilities Overview */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">
            🤖 AI Capabilities Active
          </h3>
          <div className="space-y-4">
            <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg border border-green-200">
              <div className="flex items-center space-x-3">
                <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
                <span className="text-sm font-medium text-green-800">
                  Enhanced Scan Avoidance Detection
                </span>
              </div>
              <span className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded">
                Active
              </span>
            </div>

            <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg border border-blue-200">
              <div className="flex items-center space-x-3">
                <div className="w-3 h-3 bg-blue-500 rounded-full animate-pulse"></div>
                <span className="text-sm font-medium text-blue-800">
                  ML-Powered Barcode Switching Detection
                </span>
              </div>
              <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">
                Active
              </span>
            </div>

            <div className="flex items-center justify-between p-3 bg-purple-50 rounded-lg border border-purple-200">
              <div className="flex items-center space-x-3">
                <div className="w-3 h-3 bg-purple-500 rounded-full animate-pulse"></div>
                <span className="text-sm font-medium text-purple-800">
                  Predictive Queue Forecasting
                </span>
              </div>
              <span className="text-xs bg-purple-100 text-purple-800 px-2 py-1 rounded">
                Active
              </span>
            </div>

            <div className="flex items-center justify-between p-3 bg-orange-50 rounded-lg border border-orange-200">
              <div className="flex items-center space-x-3">
                <div className="w-3 h-3 bg-orange-500 rounded-full animate-pulse"></div>
                <span className="text-sm font-medium text-orange-800">
                  Theft Risk Scoring Engine
                </span>
              </div>
              <span className="text-xs bg-orange-100 text-orange-800 px-2 py-1 rounded">
                Active
              </span>
            </div>

            <div className="flex items-center justify-between p-3 bg-yellow-50 rounded-lg border border-yellow-200">
              <div className="flex items-center space-x-3">
                <div className="w-3 h-3 bg-yellow-500 rounded-full animate-pulse"></div>
                <span className="text-sm font-medium text-yellow-800">
                  Intelligent Staffing Optimization
                </span>
              </div>
              <span className="text-xs bg-yellow-100 text-yellow-800 px-2 py-1 rounded">
                Active
              </span>
            </div>

            <div className="flex items-center justify-between p-3 bg-teal-50 rounded-lg border border-teal-200">
              <div className="flex items-center space-x-3">
                <div className="w-3 h-3 bg-teal-500 rounded-full animate-pulse"></div>
                <span className="text-sm font-medium text-teal-800">
                  Sustainability Intelligence
                </span>
              </div>
              <span className="text-xs bg-teal-100 text-teal-800 px-2 py-1 rounded">
                Active
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Detailed Insight View */}
      {selectedInsight && (
        <div className="bg-white p-6 rounded-lg shadow-md border-l-4 border-blue-500">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-800">
              📊 Detailed AI Analysis
            </h3>
            <button
              onClick={() => setSelectedInsight(null)}
              className="text-gray-500 hover:text-gray-700"
            >
              ✕
            </button>
          </div>
          <div className="space-y-4">
            <div className="flex items-center space-x-4">
              <span
                className={`px-3 py-1 rounded-full ${getTypeColor(
                  selectedInsight.type
                )}`}
              >
                {selectedInsight.type} Priority
              </span>
              <span className="text-sm text-gray-500">
                Detected at {selectedInsight.timestamp}
              </span>
            </div>
            <div className="p-4 bg-gray-50 rounded-lg">
              <p className="text-gray-700 mb-2">{selectedInsight.message}</p>
              <div className="text-sm text-gray-600">
                <strong>AI Confidence Level:</strong>{" "}
                <span
                  className={getConfidenceColor(selectedInsight.confidence)}
                >
                  {selectedInsight.confidence}%
                </span>
              </div>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
              <div className="p-3 bg-blue-50 rounded-lg">
                <div className="font-medium text-blue-800">
                  Recommended Action
                </div>
                <div className="text-blue-600">
                  Immediate investigation required
                </div>
              </div>
              <div className="p-3 bg-green-50 rounded-lg">
                <div className="font-medium text-green-800">Impact Level</div>
                <div className="text-green-600">High - Requires attention</div>
              </div>
              <div className="p-3 bg-purple-50 rounded-lg">
                <div className="font-medium text-purple-800">
                  Auto-Resolution
                </div>
                <div className="text-purple-600">Manual review needed</div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* AI Performance Metrics */}
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">
          📈 AI Performance Metrics
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="text-center p-4 bg-gradient-to-r from-blue-50 to-blue-100 rounded-lg">
            <div className="text-2xl font-bold text-blue-600">
              {aiData.intelligentAutomation.detectionAccuracy}%
            </div>
            <div className="text-sm text-blue-800">Detection Accuracy</div>
          </div>
          <div className="text-center p-4 bg-gradient-to-r from-green-50 to-green-100 rounded-lg">
            <div className="text-2xl font-bold text-green-600">
              {aiData.intelligentAutomation.processingEfficiency}%
            </div>
            <div className="text-sm text-green-800">Processing Efficiency</div>
          </div>
          <div className="text-center p-4 bg-gradient-to-r from-purple-50 to-purple-100 rounded-lg">
            <div className="text-2xl font-bold text-purple-600">
              {aiData.intelligentAutomation.autoResolvedIssues}
            </div>
            <div className="text-sm text-purple-800">Auto-Resolved Issues</div>
          </div>
          <div className="text-center p-4 bg-gradient-to-r from-orange-50 to-orange-100 rounded-lg">
            <div className="text-2xl font-bold text-orange-600">
              {aiData.intelligentAutomation.alertsSuppressed}
            </div>
            <div className="text-sm text-orange-800">Alerts Suppressed</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AIInsights;
