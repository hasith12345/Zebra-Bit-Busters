import React, { useState, useEffect } from "react";
import { Users, UserCheck, Clock, ShoppingBag } from "lucide-react";

const CustomerBehavior = () => {
  const [customerData, setCustomerData] = useState({
    total_unique_customers: 0,
    avg_transactions_per_customer: 0,
    avg_spending_per_customer: 0,
    top_customers: [],
    queue_analytics: {
      total_queue_events: 0,
      avg_queue_time: 0,
      peak_hours: [],
    },
    shopping_patterns: {
      peak_shopping_hours: [],
      most_bought_together: [],
    },
  });

  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchCustomerData = async () => {
      try {
        const response = await fetch(
          "http://localhost:3001/api/customer-behavior"
        );
        if (response.ok) {
          const data = await response.json();
          setCustomerData(data);
        }
      } catch (error) {
        console.warn("Failed to fetch customer behavior data:", error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchCustomerData();
    const interval = setInterval(fetchCustomerData, 15000); // Update every 15 seconds

    return () => clearInterval(interval);
  }, []);

  if (isLoading) {
    return (
      <div className="glass-card p-6">
        <div className="animate-pulse">
          <div className="h-6 bg-purple-300 rounded mb-4"></div>
          <div className="space-y-3">
            <div className="h-4 bg-purple-300 rounded"></div>
            <div className="h-4 bg-purple-300 rounded"></div>
            <div className="h-4 bg-purple-300 rounded"></div>
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
        <Users className="w-6 h-6 text-purple-400 mr-3" />
        <h2 className="text-xl font-bold text-white">Customer Behavior</h2>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <div className="bg-gradient-to-r from-purple-600 to-purple-500 p-4 rounded-lg">
          <div className="flex items-center">
            <Users className="w-5 h-5 text-white mr-2" />
            <div>
              <p className="text-purple-100 text-sm">Total Customers</p>
              <p className="text-white font-bold text-lg">
                {customerData.total_unique_customers}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-gradient-to-r from-blue-600 to-blue-500 p-4 rounded-lg">
          <div className="flex items-center">
            <ShoppingBag className="w-5 h-5 text-white mr-2" />
            <div>
              <p className="text-blue-100 text-sm">Avg Transactions</p>
              <p className="text-white font-bold text-lg">
                {customerData.avg_transactions_per_customer.toFixed(1)}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-gradient-to-r from-green-600 to-green-500 p-4 rounded-lg">
          <div className="flex items-center">
            <UserCheck className="w-5 h-5 text-white mr-2" />
            <div>
              <p className="text-green-100 text-sm">Avg Spending</p>
              <p className="text-white font-bold text-lg">
                {formatCurrency(customerData.avg_spending_per_customer)}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-gradient-to-r from-yellow-600 to-yellow-500 p-4 rounded-lg">
          <div className="flex items-center">
            <Clock className="w-5 h-5 text-white mr-2" />
            <div>
              <p className="text-yellow-100 text-sm">Avg Queue Time</p>
              <p className="text-white font-bold text-lg">
                {customerData.queue_analytics?.avg_queue_time?.toFixed(1) || 0}m
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Top Customers */}
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-white mb-3 flex items-center">
          <UserCheck className="w-5 h-5 text-green-400 mr-2" />
          Top Customers
        </h3>
        <div className="space-y-2">
          {customerData.top_customers?.map((customer, index) => (
            <div
              key={index}
              className="flex justify-between items-center p-3 bg-white bg-opacity-10 rounded"
            >
              <div className="flex items-center">
                <div className="w-8 h-8 bg-gradient-to-r from-purple-500 to-blue-500 rounded-full flex items-center justify-center text-white font-bold text-sm mr-3">
                  {index + 1}
                </div>
                <div>
                  <p className="text-white font-medium">
                    {customer.customer_id}
                  </p>
                  <p className="text-gray-400 text-sm">
                    {customer.transaction_count} transactions
                  </p>
                </div>
              </div>
              <div className="text-right">
                <p className="text-green-400 font-bold">
                  {formatCurrency(customer.total_spent)}
                </p>
                <p className="text-gray-400 text-sm">
                  Avg: {formatCurrency(customer.avg_order_value)}
                </p>
              </div>
            </div>
          ))}
          {customerData.top_customers?.length === 0 && (
            <div className="text-center py-4">
              <p className="text-gray-400">No customer data available</p>
            </div>
          )}
        </div>
      </div>

      {/* Shopping Patterns */}
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-white mb-3">
          Shopping Patterns
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Peak Hours */}
          <div className="bg-white bg-opacity-10 p-4 rounded-lg">
            <h4 className="text-white font-medium mb-2 flex items-center">
              <Clock className="w-4 h-4 mr-2" />
              Peak Shopping Hours
            </h4>
            <div className="space-y-1">
              {customerData.shopping_patterns?.peak_shopping_hours?.map(
                (hour, index) => (
                  <div key={index} className="flex items-center">
                    <div className="w-2 h-2 bg-blue-400 rounded-full mr-2"></div>
                    <p className="text-gray-300 text-sm">{hour}</p>
                  </div>
                )
              )}
            </div>
          </div>

          {/* Popular Combinations */}
          <div className="bg-white bg-opacity-10 p-4 rounded-lg">
            <h4 className="text-white font-medium mb-2 flex items-center">
              <ShoppingBag className="w-4 h-4 mr-2" />
              Popular Combinations
            </h4>
            <div className="space-y-1">
              {customerData.shopping_patterns?.most_bought_together?.map(
                (combo, index) => (
                  <div key={index} className="flex items-center">
                    <div className="w-2 h-2 bg-green-400 rounded-full mr-2"></div>
                    <p className="text-gray-300 text-sm">{combo}</p>
                  </div>
                )
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Queue Analytics */}
      <div>
        <h3 className="text-lg font-semibold text-white mb-3">
          Queue Efficiency
        </h3>
        <div className="grid grid-cols-3 gap-4">
          <div className="bg-white bg-opacity-10 p-4 rounded-lg text-center">
            <p className="text-gray-300 text-sm">Total Queue Events</p>
            <p className="text-white font-bold text-xl">
              {customerData.queue_analytics?.total_queue_events || 0}
            </p>
          </div>
          <div className="bg-white bg-opacity-10 p-4 rounded-lg text-center">
            <p className="text-gray-300 text-sm">Avg Wait Time</p>
            <p className="text-white font-bold text-xl">
              {customerData.queue_analytics?.avg_queue_time?.toFixed(1) || 0}m
            </p>
          </div>
          <div className="bg-white bg-opacity-10 p-4 rounded-lg text-center">
            <p className="text-gray-300 text-sm">Peak Queue Hours</p>
            <p className="text-white font-bold text-sm">
              {customerData.queue_analytics?.peak_hours?.join(", ") || "N/A"}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CustomerBehavior;
