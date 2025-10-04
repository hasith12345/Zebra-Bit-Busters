import React, { useState, useEffect } from "react";
import { TrendingUp, DollarSign, ShoppingCart, Users } from "lucide-react";

const SalesAnalytics = () => {
  const [salesData, setSalesData] = useState({
    total_revenue: 0,
    total_transactions: 0,
    avg_transaction_value: 0,
    unique_customers: 0,
    top_products: [],
    hourly_sales: [],
    customer_metrics: {
      repeat_customers: 0,
      avg_customer_spending: 0,
    },
  });

  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchSalesData = async () => {
      try {
        const response = await fetch("http://localhost:3001/api/analytics");
        if (response.ok) {
          const data = await response.json();
          setSalesData(data);
        }
      } catch (error) {
        console.warn("Failed to fetch sales analytics:", error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchSalesData();
    const interval = setInterval(fetchSalesData, 5000); // Update every 5 seconds

    return () => clearInterval(interval);
  }, []);

  if (isLoading) {
    return (
      <div className="glass-card p-6">
        <div className="animate-pulse">
          <div className="h-6 bg-blue-300 rounded mb-4"></div>
          <div className="space-y-3">
            <div className="h-4 bg-blue-300 rounded"></div>
            <div className="h-4 bg-blue-300 rounded"></div>
            <div className="h-4 bg-blue-300 rounded"></div>
          </div>
        </div>
      </div>
    );
  }

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat("en-LK", {
      style: "currency",
      currency: "LKR",
      minimumFractionDigits: 0,
    }).format(amount);
  };

  return (
    <div className="glass-card p-6">
      <div className="flex items-center mb-6">
        <TrendingUp className="w-6 h-6 text-green-400 mr-3" />
        <h2 className="text-xl font-bold text-white">Sales Analytics</h2>
      </div>

      {/* Key Metrics Row */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <div className="bg-gradient-to-r from-green-600 to-green-500 p-4 rounded-lg">
          <div className="flex items-center">
            <DollarSign className="w-5 h-5 text-white mr-2" />
            <div>
              <p className="text-green-100 text-sm">Total Revenue</p>
              <p className="text-white font-bold text-lg">
                {formatCurrency(salesData.total_revenue)}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-gradient-to-r from-blue-600 to-blue-500 p-4 rounded-lg">
          <div className="flex items-center">
            <ShoppingCart className="w-5 h-5 text-white mr-2" />
            <div>
              <p className="text-blue-100 text-sm">Transactions</p>
              <p className="text-white font-bold text-lg">
                {salesData.total_transactions}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-gradient-to-r from-purple-600 to-purple-500 p-4 rounded-lg">
          <div className="flex items-center">
            <TrendingUp className="w-5 h-5 text-white mr-2" />
            <div>
              <p className="text-purple-100 text-sm">Avg Order</p>
              <p className="text-white font-bold text-lg">
                {formatCurrency(salesData.avg_transaction_value)}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-gradient-to-r from-orange-600 to-orange-500 p-4 rounded-lg">
          <div className="flex items-center">
            <Users className="w-5 h-5 text-white mr-2" />
            <div>
              <p className="text-orange-100 text-sm">Customers</p>
              <p className="text-white font-bold text-lg">
                {salesData.unique_customers}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Top Products */}
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-white mb-3">
          Top Selling Products
        </h3>
        <div className="space-y-2">
          {salesData.top_products?.slice(0, 5).map((product, index) => (
            <div
              key={index}
              className="flex justify-between items-center p-3 bg-white bg-opacity-10 rounded"
            >
              <div>
                <p className="text-white font-medium">{product.name}</p>
                <p className="text-gray-300 text-sm">
                  {product.sales_count} units sold
                </p>
              </div>
              <div className="text-right">
                <p className="text-green-400 font-bold">
                  {formatCurrency(product.revenue)}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Hourly Sales Trend */}
      <div>
        <h3 className="text-lg font-semibold text-white mb-3">
          Sales Timeline
        </h3>
        <div className="flex items-end space-x-2 h-20">
          {salesData.hourly_sales?.map((hour, index) => {
            const maxRevenue = Math.max(
              ...salesData.hourly_sales.map((h) => h.revenue)
            );
            const height =
              maxRevenue > 0 ? (hour.revenue / maxRevenue) * 100 : 0;

            return (
              <div key={index} className="flex-1 flex flex-col items-center">
                <div
                  className="w-full bg-gradient-to-t from-blue-500 to-blue-300 rounded-sm transition-all duration-500"
                  style={{ height: `${height}%` }}
                  title={`${hour.hour}: ${formatCurrency(hour.revenue)}`}
                ></div>
                <p className="text-xs text-gray-400 mt-1">
                  {hour.hour.slice(0, 2)}
                </p>
              </div>
            );
          })}
        </div>
      </div>

      {/* Customer Insights */}
      <div className="mt-6 grid grid-cols-2 gap-4">
        <div className="bg-white bg-opacity-10 p-4 rounded-lg">
          <p className="text-gray-300 text-sm">Repeat Customers</p>
          <p className="text-white font-bold text-xl">
            {salesData.customer_metrics?.repeat_customers || 0}
          </p>
        </div>
        <div className="bg-white bg-opacity-10 p-4 rounded-lg">
          <p className="text-gray-300 text-sm">Avg Customer Spend</p>
          <p className="text-white font-bold text-xl">
            {formatCurrency(
              salesData.customer_metrics?.avg_customer_spending || 0
            )}
          </p>
        </div>
      </div>
    </div>
  );
};

export default SalesAnalytics;
