import React, { useState, useEffect } from "react";
import {
  Brain,
  TrendingUp,
  AlertCircle,
  CheckCircle,
  Target,
} from "lucide-react";

const BusinessSummary = () => {
  const [summaryData, setSummaryData] = useState({
    insights: [],
    recommendations: [],
    alerts: [],
    performance_score: 0,
  });

  const [allData, setAllData] = useState({
    analytics: null,
    sales: null,
    inventory: null,
    customer: null,
  });

  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchAllData = async () => {
      try {
        const [analyticsRes, salesRes, inventoryRes, customerRes] =
          await Promise.all([
            fetch("http://localhost:3001/api/analytics"),
            fetch("http://localhost:3001/api/sales"),
            fetch("http://localhost:3001/api/inventory"),
            fetch("http://localhost:3001/api/customer-behavior"),
          ]);

        const analytics = analyticsRes.ok ? await analyticsRes.json() : null;
        const sales = salesRes.ok ? await salesRes.json() : null;
        const inventory = inventoryRes.ok ? await inventoryRes.json() : null;
        const customer = customerRes.ok ? await customerRes.json() : null;

        setAllData({ analytics, sales, inventory, customer });
        generateBusinessInsights({ analytics, sales, inventory, customer });
      } catch (error) {
        console.warn("Failed to fetch business summary data:", error);
      } finally {
        setIsLoading(false);
      }
    };

    const generateBusinessInsights = (data) => {
      const insights = [];
      const recommendations = [];
      const alerts = [];
      let performanceScore = 75; // Base score

      // Sales insights
      if (data.analytics) {
        if (data.analytics.total_revenue > 10000) {
          insights.push({
            type: "positive",
            title: "Strong Revenue Performance",
            description: `Generated LKR ${data.analytics.total_revenue.toLocaleString()} in revenue from ${
              data.analytics.total_transactions
            } transactions`,
          });
          performanceScore += 10;
        }

        if (data.analytics.avg_transaction_value > 400) {
          insights.push({
            type: "positive",
            title: "High Average Order Value",
            description: `Customers spending LKR ${data.analytics.avg_transaction_value.toFixed(
              0
            )} on average per transaction`,
          });
          performanceScore += 5;
        }

        // Top product insights
        if (
          data.analytics.top_products &&
          data.analytics.top_products.length > 0
        ) {
          const topProduct = data.analytics.top_products[0];
          insights.push({
            type: "info",
            title: "Best Selling Product",
            description: `${topProduct.name} leads with ${
              topProduct.sales_count
            } units and LKR ${topProduct.revenue.toLocaleString()} revenue`,
          });
        }
      }

      // Inventory insights and alerts
      if (data.inventory) {
        if (data.inventory.low_stock_count > 0) {
          alerts.push({
            type: "warning",
            title: "Low Stock Alert",
            description: `${data.inventory.low_stock_count} products are running low on inventory`,
          });
          performanceScore -= 5;
        }

        if (data.inventory.out_of_stock_count > 0) {
          alerts.push({
            type: "critical",
            title: "Out of Stock",
            description: `${data.inventory.out_of_stock_count} products are completely out of stock`,
          });
          performanceScore -= 10;

          recommendations.push({
            title: "Immediate Restocking Required",
            description: "Restock out-of-stock items to prevent lost sales",
            priority: "high",
          });
        }

        if (
          data.inventory.fast_moving_items &&
          data.inventory.fast_moving_items.length > 0
        ) {
          insights.push({
            type: "positive",
            title: "Fast Moving Inventory",
            description: `${data.inventory.fast_moving_items.length} products showing high sales velocity`,
          });
        }
      }

      // Customer behavior insights
      if (data.customer) {
        if (data.customer.avg_spending_per_customer > 500) {
          insights.push({
            type: "positive",
            title: "High Customer Value",
            description: `Customers spending LKR ${data.customer.avg_spending_per_customer.toFixed(
              0
            )} on average`,
          });
          performanceScore += 5;
        }

        if (data.customer.total_unique_customers > 20) {
          insights.push({
            type: "positive",
            title: "Good Customer Base",
            description: `Serving ${data.customer.total_unique_customers} unique customers`,
          });
        }

        // Queue efficiency
        if (
          data.customer.queue_analytics &&
          data.customer.queue_analytics.avg_queue_time > 3
        ) {
          alerts.push({
            type: "warning",
            title: "Queue Wait Times",
            description: `Average queue time is ${data.customer.queue_analytics.avg_queue_time.toFixed(
              1
            )} minutes`,
          });

          recommendations.push({
            title: "Optimize Queue Management",
            description:
              "Consider opening additional checkout stations during peak hours",
            priority: "medium",
          });
        }
      }

      // Business recommendations
      if (data.analytics && data.analytics.hourly_sales) {
        const peakHour = data.analytics.hourly_sales.reduce(
          (max, hour) => (hour.revenue > max.revenue ? hour : max),
          { revenue: 0 }
        );

        if (peakHour.revenue > 0) {
          recommendations.push({
            title: "Staff Peak Hours",
            description: `Peak sales at ${peakHour.hour} - ensure adequate staffing`,
            priority: "medium",
          });
        }
      }

      // Marketing recommendations
      if (data.analytics && data.analytics.customer_metrics) {
        const repeatRate =
          (data.analytics.customer_metrics.repeat_customers /
            data.analytics.unique_customers) *
          100;
        if (repeatRate < 50) {
          recommendations.push({
            title: "Customer Retention",
            description:
              "Implement loyalty program to increase repeat customers",
            priority: "high",
          });
        }
      }

      setSummaryData({
        insights,
        recommendations,
        alerts,
        performance_score: Math.max(0, Math.min(100, performanceScore)),
      });
    };

    fetchAllData();
    const interval = setInterval(fetchAllData, 30000); // Update every 30 seconds

    return () => clearInterval(interval);
  }, []);

  if (isLoading) {
    return (
      <div className="glass-card p-6">
        <div className="animate-pulse">
          <div className="h-6 bg-indigo-300 rounded mb-4"></div>
          <div className="space-y-3">
            <div className="h-4 bg-indigo-300 rounded"></div>
            <div className="h-4 bg-indigo-300 rounded"></div>
            <div className="h-4 bg-indigo-300 rounded"></div>
          </div>
        </div>
      </div>
    );
  }

  const getPerformanceColor = (score) => {
    if (score >= 80) return "text-green-400";
    if (score >= 60) return "text-yellow-400";
    return "text-red-400";
  };

  const getAlertIcon = (type) => {
    switch (type) {
      case "critical":
        return <AlertCircle className="w-4 h-4 text-red-400" />;
      case "warning":
        return <AlertCircle className="w-4 h-4 text-yellow-400" />;
      default:
        return <AlertCircle className="w-4 h-4 text-blue-400" />;
    }
  };

  const getInsightIcon = (type) => {
    switch (type) {
      case "positive":
        return <CheckCircle className="w-4 h-4 text-green-400" />;
      case "negative":
        return <AlertCircle className="w-4 h-4 text-red-400" />;
      default:
        return <TrendingUp className="w-4 h-4 text-blue-400" />;
    }
  };

  return (
    <div className="glass-card p-6">
      <div className="flex items-center mb-6">
        <Brain className="w-6 h-6 text-indigo-400 mr-3" />
        <h2 className="text-xl font-bold text-white">Business Intelligence</h2>
      </div>

      {/* Performance Score */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-lg font-semibold text-white">
            Performance Score
          </h3>
          <span
            className={`font-bold text-2xl ${getPerformanceColor(
              summaryData.performance_score
            )}`}
          >
            {summaryData.performance_score}/100
          </span>
        </div>
        <div className="w-full bg-gray-700 rounded-full h-3">
          <div
            className={`h-3 rounded-full transition-all duration-1000 ${
              summaryData.performance_score >= 80
                ? "bg-gradient-to-r from-green-500 to-green-400"
                : summaryData.performance_score >= 60
                ? "bg-gradient-to-r from-yellow-500 to-yellow-400"
                : "bg-gradient-to-r from-red-500 to-red-400"
            }`}
            style={{ width: `${summaryData.performance_score}%` }}
          ></div>
        </div>
      </div>

      {/* Alerts */}
      {summaryData.alerts.length > 0 && (
        <div className="mb-6">
          <h3 className="text-lg font-semibold text-white mb-3 flex items-center">
            <AlertCircle className="w-5 h-5 text-red-400 mr-2" />
            Alerts
          </h3>
          <div className="space-y-2">
            {summaryData.alerts.map((alert, index) => (
              <div
                key={index}
                className="flex items-start p-3 bg-red-900 bg-opacity-30 border border-red-700 rounded"
              >
                {getAlertIcon(alert.type)}
                <div className="ml-3">
                  <p className="text-white font-medium">{alert.title}</p>
                  <p className="text-gray-300 text-sm">{alert.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Key Insights */}
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-white mb-3 flex items-center">
          <TrendingUp className="w-5 h-5 text-blue-400 mr-2" />
          Key Insights
        </h3>
        <div className="space-y-2 max-h-48 overflow-y-auto">
          {summaryData.insights.map((insight, index) => (
            <div
              key={index}
              className="flex items-start p-3 bg-white bg-opacity-10 rounded"
            >
              {getInsightIcon(insight.type)}
              <div className="ml-3">
                <p className="text-white font-medium">{insight.title}</p>
                <p className="text-gray-300 text-sm">{insight.description}</p>
              </div>
            </div>
          ))}
          {summaryData.insights.length === 0 && (
            <div className="text-center py-4">
              <p className="text-gray-400">Analyzing data for insights...</p>
            </div>
          )}
        </div>
      </div>

      {/* Recommendations */}
      <div>
        <h3 className="text-lg font-semibold text-white mb-3 flex items-center">
          <Target className="w-5 h-5 text-purple-400 mr-2" />
          Recommendations
        </h3>
        <div className="space-y-2">
          {summaryData.recommendations.map((rec, index) => (
            <div
              key={index}
              className="flex items-start p-3 bg-purple-900 bg-opacity-30 border border-purple-700 rounded"
            >
              <Target className="w-4 h-4 text-purple-400 mt-0.5" />
              <div className="ml-3 flex-1">
                <div className="flex items-center justify-between">
                  <p className="text-white font-medium">{rec.title}</p>
                  <span
                    className={`text-xs px-2 py-1 rounded ${
                      rec.priority === "high"
                        ? "bg-red-600 text-white"
                        : rec.priority === "medium"
                        ? "bg-yellow-600 text-white"
                        : "bg-green-600 text-white"
                    }`}
                  >
                    {rec.priority?.toUpperCase()}
                  </span>
                </div>
                <p className="text-gray-300 text-sm">{rec.description}</p>
              </div>
            </div>
          ))}
          {summaryData.recommendations.length === 0 && (
            <div className="text-center py-4">
              <p className="text-gray-400">
                No specific recommendations at this time
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default BusinessSummary;
