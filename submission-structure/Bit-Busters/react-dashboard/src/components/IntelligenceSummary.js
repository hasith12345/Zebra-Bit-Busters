import React, { useState, useEffect } from "react";

const IntelligenceSummary = () => {
  const [summary, setSummary] = useState({
    systemHealth: 92,
    totalAlgorithms: 10,
    activeAlgorithms: 10,
    detectionAccuracy: 94.2,
    processingEfficiency: 98.5,
    threatLevel: "Moderate",
    lastAnalysisUpdate: new Date().toLocaleTimeString(),
    keyMetrics: {
      scanAvoidanceDetections: 156,
      barcodeSwitchingEvents: 23,
      weightDiscrepancies: 8,
      systemHealthEvents: 12,
      queuePredictions: 45,
      theftRiskAlerts: 7,
      inventoryAnomalies: 15,
      fraudCorrelations: 3,
      staffingOptimizations: 18,
      sustainabilityInsights: 22,
    },
    performanceDistribution: {
      critical: 3,
      high: 8,
      medium: 15,
      low: 24,
    },
  });

  useEffect(() => {
    const fetchIntelligenceSummary = async () => {
      try {
        const response = await fetch("/api/intelligence-summary");
        if (response.ok) {
          const data = await response.json();
          setSummary(data);
        }
      } catch (error) {
        console.error("Error fetching intelligence summary:", error);
      }
    };

    fetchIntelligenceSummary();
    const interval = setInterval(fetchIntelligenceSummary, 30000); // Update every 30 seconds

    return () => clearInterval(interval);
  }, []);

  const getThreatLevelColor = (level) => {
    switch (level.toLowerCase()) {
      case "critical":
        return "text-red-600 bg-red-100";
      case "high":
        return "text-orange-600 bg-orange-100";
      case "moderate":
        return "text-yellow-600 bg-yellow-100";
      case "low":
        return "text-green-600 bg-green-100";
      default:
        return "text-gray-600 bg-gray-100";
    }
  };

  const getHealthScoreColor = (score) => {
    if (score >= 90) return "text-green-600";
    if (score >= 80) return "text-yellow-600";
    if (score >= 70) return "text-orange-600";
    return "text-red-600";
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-indigo-500">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-bold text-gray-800 flex items-center">
          🧠 Sentinel Intelligence Summary
        </h2>
        <div className="flex items-center space-x-4">
          <span className="text-xs text-gray-500">
            Last Update: {summary.lastAnalysisUpdate}
          </span>
          <span
            className={`px-3 py-1 rounded-full text-xs font-medium ${getThreatLevelColor(
              summary.threatLevel
            )}`}
          >
            Threat Level: {summary.threatLevel}
          </span>
        </div>
      </div>

      {/* Main Intelligence Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4 mb-6">
        <div className="text-center p-4 bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg">
          <div
            className={`text-2xl font-bold ${getHealthScoreColor(
              summary.systemHealth
            )}`}
          >
            {summary.systemHealth}%
          </div>
          <div className="text-sm text-blue-800">System Health</div>
        </div>

        <div className="text-center p-4 bg-gradient-to-br from-green-50 to-green-100 rounded-lg">
          <div className="text-2xl font-bold text-green-600">
            {summary.activeAlgorithms}/{summary.totalAlgorithms}
          </div>
          <div className="text-sm text-green-800">AI Algorithms</div>
        </div>

        <div className="text-center p-4 bg-gradient-to-br from-purple-50 to-purple-100 rounded-lg">
          <div className="text-2xl font-bold text-purple-600">
            {summary.detectionAccuracy}%
          </div>
          <div className="text-sm text-purple-800">Detection Accuracy</div>
        </div>

        <div className="text-center p-4 bg-gradient-to-br from-teal-50 to-teal-100 rounded-lg">
          <div className="text-2xl font-bold text-teal-600">
            {summary.processingEfficiency}%
          </div>
          <div className="text-sm text-teal-800">Processing Efficiency</div>
        </div>

        <div className="text-center p-4 bg-gradient-to-br from-orange-50 to-orange-100 rounded-lg">
          <div className="text-2xl font-bold text-orange-600">
            {Object.values(summary.performanceDistribution).reduce(
              (a, b) => a + b,
              0
            )}
          </div>
          <div className="text-sm text-orange-800">Total Events Today</div>
        </div>
      </div>

      {/* Algorithm Performance Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-3 mb-6">
        <div className="p-3 bg-gradient-to-r from-red-50 to-red-100 rounded-lg border border-red-200">
          <div className="text-lg font-bold text-red-600">
            {summary.keyMetrics.scanAvoidanceDetections}
          </div>
          <div className="text-xs text-red-800">Scan Avoidance</div>
        </div>

        <div className="p-3 bg-gradient-to-r from-blue-50 to-blue-100 rounded-lg border border-blue-200">
          <div className="text-lg font-bold text-blue-600">
            {summary.keyMetrics.barcodeSwitchingEvents}
          </div>
          <div className="text-xs text-blue-800">Barcode Switching</div>
        </div>

        <div className="p-3 bg-gradient-to-r from-yellow-50 to-yellow-100 rounded-lg border border-yellow-200">
          <div className="text-lg font-bold text-yellow-600">
            {summary.keyMetrics.weightDiscrepancies}
          </div>
          <div className="text-xs text-yellow-800">Weight Discrepancies</div>
        </div>

        <div className="p-3 bg-gradient-to-r from-green-50 to-green-100 rounded-lg border border-green-200">
          <div className="text-lg font-bold text-green-600">
            {summary.keyMetrics.queuePredictions}
          </div>
          <div className="text-xs text-green-800">Queue Predictions</div>
        </div>

        <div className="p-3 bg-gradient-to-r from-purple-50 to-purple-100 rounded-lg border border-purple-200">
          <div className="text-lg font-bold text-purple-600">
            {summary.keyMetrics.theftRiskAlerts}
          </div>
          <div className="text-xs text-purple-800">Theft Risk Alerts</div>
        </div>

        <div className="p-3 bg-gradient-to-r from-indigo-50 to-indigo-100 rounded-lg border border-indigo-200">
          <div className="text-lg font-bold text-indigo-600">
            {summary.keyMetrics.inventoryAnomalies}
          </div>
          <div className="text-xs text-indigo-800">Inventory Anomalies</div>
        </div>

        <div className="p-3 bg-gradient-to-r from-pink-50 to-pink-100 rounded-lg border border-pink-200">
          <div className="text-lg font-bold text-pink-600">
            {summary.keyMetrics.fraudCorrelations}
          </div>
          <div className="text-xs text-pink-800">Fraud Correlations</div>
        </div>

        <div className="p-3 bg-gradient-to-r from-orange-50 to-orange-100 rounded-lg border border-orange-200">
          <div className="text-lg font-bold text-orange-600">
            {summary.keyMetrics.staffingOptimizations}
          </div>
          <div className="text-xs text-orange-800">Staffing Optimizations</div>
        </div>

        <div className="p-3 bg-gradient-to-r from-teal-50 to-teal-100 rounded-lg border border-teal-200">
          <div className="text-lg font-bold text-teal-600">
            {summary.keyMetrics.sustainabilityInsights}
          </div>
          <div className="text-xs text-teal-800">Sustainability Insights</div>
        </div>

        <div className="p-3 bg-gradient-to-r from-gray-50 to-gray-100 rounded-lg border border-gray-200">
          <div className="text-lg font-bold text-gray-600">
            {summary.keyMetrics.systemHealthEvents}
          </div>
          <div className="text-xs text-gray-800">System Health</div>
        </div>
      </div>

      {/* Priority Distribution */}
      <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
        <div className="text-sm font-medium text-gray-700">
          Event Priority Distribution:
        </div>
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-1">
            <div className="w-3 h-3 bg-red-500 rounded-full"></div>
            <span className="text-xs text-gray-600">
              Critical: {summary.performanceDistribution.critical}
            </span>
          </div>
          <div className="flex items-center space-x-1">
            <div className="w-3 h-3 bg-orange-500 rounded-full"></div>
            <span className="text-xs text-gray-600">
              High: {summary.performanceDistribution.high}
            </span>
          </div>
          <div className="flex items-center space-x-1">
            <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
            <span className="text-xs text-gray-600">
              Medium: {summary.performanceDistribution.medium}
            </span>
          </div>
          <div className="flex items-center space-x-1">
            <div className="w-3 h-3 bg-green-500 rounded-full"></div>
            <span className="text-xs text-gray-600">
              Low: {summary.performanceDistribution.low}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default IntelligenceSummary;
