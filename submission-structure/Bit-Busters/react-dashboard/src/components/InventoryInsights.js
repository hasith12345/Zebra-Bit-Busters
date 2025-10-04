import React, { useState, useEffect } from "react";
import { Package, AlertTriangle, TrendingUp, BarChart3 } from "lucide-react";

const InventoryInsights = () => {
  const [inventoryData, setInventoryData] = useState({
    stock_alerts: [],
    fast_moving_items: [],
    total_skus: 0,
    low_stock_count: 0,
    out_of_stock_count: 0,
    product_performance: [],
  });

  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchInventoryData = async () => {
      try {
        const response = await fetch("http://localhost:3001/api/inventory");
        if (response.ok) {
          const data = await response.json();
          setInventoryData(data);
        }
      } catch (error) {
        console.warn("Failed to fetch inventory data:", error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchInventoryData();
    const interval = setInterval(fetchInventoryData, 10000); // Update every 10 seconds

    return () => clearInterval(interval);
  }, []);

  if (isLoading) {
    return (
      <div className="glass-card p-6">
        <div className="animate-pulse">
          <div className="h-6 bg-orange-300 rounded mb-4"></div>
          <div className="space-y-3">
            <div className="h-4 bg-orange-300 rounded"></div>
            <div className="h-4 bg-orange-300 rounded"></div>
            <div className="h-4 bg-orange-300 rounded"></div>
          </div>
        </div>
      </div>
    );
  }

  const getStockStatusColor = (status) => {
    switch (status) {
      case "low":
        return "text-red-400 bg-red-900";
      case "medium":
        return "text-yellow-400 bg-yellow-900";
      default:
        return "text-green-400 bg-green-900";
    }
  };

  const getVelocityColor = (velocity) => {
    switch (velocity) {
      case "high":
        return "text-red-400";
      case "medium":
        return "text-yellow-400";
      default:
        return "text-green-400";
    }
  };

  return (
    <div className="glass-card p-6">
      <div className="flex items-center mb-6">
        <Package className="w-6 h-6 text-orange-400 mr-3" />
        <h2 className="text-xl font-bold text-white">Inventory Insights</h2>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <div className="bg-gradient-to-r from-blue-600 to-blue-500 p-4 rounded-lg">
          <div className="flex items-center">
            <BarChart3 className="w-5 h-5 text-white mr-2" />
            <div>
              <p className="text-blue-100 text-sm">Total SKUs</p>
              <p className="text-white font-bold text-lg">
                {inventoryData.total_skus}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-gradient-to-r from-yellow-600 to-yellow-500 p-4 rounded-lg">
          <div className="flex items-center">
            <AlertTriangle className="w-5 h-5 text-white mr-2" />
            <div>
              <p className="text-yellow-100 text-sm">Low Stock</p>
              <p className="text-white font-bold text-lg">
                {inventoryData.low_stock_count}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-gradient-to-r from-red-600 to-red-500 p-4 rounded-lg">
          <div className="flex items-center">
            <Package className="w-5 h-5 text-white mr-2" />
            <div>
              <p className="text-red-100 text-sm">Out of Stock</p>
              <p className="text-white font-bold text-lg">
                {inventoryData.out_of_stock_count}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-gradient-to-r from-green-600 to-green-500 p-4 rounded-lg">
          <div className="flex items-center">
            <TrendingUp className="w-5 h-5 text-white mr-2" />
            <div>
              <p className="text-green-100 text-sm">Fast Moving</p>
              <p className="text-white font-bold text-lg">
                {inventoryData.fast_moving_items?.length || 0}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Stock Alerts */}
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-white mb-3 flex items-center">
          <AlertTriangle className="w-5 h-5 text-yellow-400 mr-2" />
          Stock Alerts
        </h3>
        <div className="space-y-2 max-h-48 overflow-y-auto">
          {inventoryData.stock_alerts?.slice(0, 8).map((alert, index) => (
            <div
              key={index}
              className="flex justify-between items-center p-3 bg-white bg-opacity-10 rounded"
            >
              <div>
                <p className="text-white font-medium">{alert.sku}</p>
                <span
                  className={`text-xs px-2 py-1 rounded ${getStockStatusColor(
                    alert.status
                  )} bg-opacity-20`}
                >
                  {alert.status.toUpperCase()}
                </span>
              </div>
              <div className="text-right">
                <p className="text-white">Stock: {alert.current_stock}</p>
                <p className="text-gray-400 text-sm">
                  Reorder: {alert.recommended_reorder}
                </p>
              </div>
            </div>
          ))}
          {inventoryData.stock_alerts?.length === 0 && (
            <div className="text-center py-4">
              <p className="text-gray-400">No stock alerts at this time</p>
            </div>
          )}
        </div>
      </div>

      {/* Fast Moving Items */}
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-white mb-3 flex items-center">
          <TrendingUp className="w-5 h-5 text-green-400 mr-2" />
          Fast Moving Items
        </h3>
        <div className="space-y-2 max-h-48 overflow-y-auto">
          {inventoryData.fast_moving_items?.slice(0, 6).map((item, index) => (
            <div
              key={index}
              className="flex justify-between items-center p-3 bg-white bg-opacity-10 rounded"
            >
              <div>
                <p className="text-white font-medium">{item.sku}</p>
                <span
                  className={`text-xs px-2 py-1 rounded ${getVelocityColor(
                    item.velocity
                  )} bg-opacity-20`}
                >
                  {item.velocity.toUpperCase()} VELOCITY
                </span>
              </div>
              <div className="text-right">
                <p className="text-white">Stock: {item.current_stock}</p>
                <p className="text-green-400 text-sm">
                  Sold: {item.units_sold} units
                </p>
              </div>
            </div>
          ))}
          {inventoryData.fast_moving_items?.length === 0 && (
            <div className="text-center py-4">
              <p className="text-gray-400">
                No fast moving items data available
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Product Performance */}
      <div>
        <h3 className="text-lg font-semibold text-white mb-3">
          Top Selling Products
        </h3>
        <div className="space-y-2">
          {inventoryData.product_performance
            ?.slice(0, 5)
            .map((product, index) => (
              <div
                key={index}
                className="flex justify-between items-center p-2 bg-white bg-opacity-5 rounded"
              >
                <div className="flex items-center">
                  <span className="text-gray-400 text-sm w-6">
                    #{index + 1}
                  </span>
                  <p className="text-white ml-2">{product.sku}</p>
                </div>
                <div className="flex items-center">
                  <div className="w-16 bg-gray-700 rounded-full h-2 mr-3">
                    <div
                      className="bg-gradient-to-r from-blue-500 to-green-500 h-2 rounded-full transition-all duration-500"
                      style={{
                        width: `${Math.min(
                          (product.sales_count /
                            Math.max(
                              ...inventoryData.product_performance.map(
                                (p) => p.sales_count
                              )
                            )) *
                            100,
                          100
                        )}%`,
                      }}
                    ></div>
                  </div>
                  <p className="text-white font-bold">{product.sales_count}</p>
                </div>
              </div>
            ))}
        </div>
      </div>
    </div>
  );
};

export default InventoryInsights;
