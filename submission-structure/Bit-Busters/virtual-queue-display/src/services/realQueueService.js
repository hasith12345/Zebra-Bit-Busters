// Real data service that connects to the Python backend API
// This replaces the mock service with actual API calls

import axios from 'axios';

const API_BASE_URL = 'http://localhost:5001/api';

class RealQueueDataService {
  constructor() {
    this.subscribers = [];
    this.pollingInterval = null;
    this.startPolling();
  }

  // Start polling for real-time updates
  startPolling() {
    this.pollingInterval = setInterval(() => {
      this.fetchStationData().then(data => {
        this.subscribers.forEach(callback => callback(data.stations));
      }).catch(error => {
        console.error('Error fetching station data:', error);
      });
    }, 2000); // Poll every 2 seconds
  }

  // Fetch all station data from backend
  async fetchStationData() {
    try {
      const response = await axios.get(`${API_BASE_URL}/stations`);
      return response.data;
    } catch (error) {
      console.error('Error fetching station data:', error);
      // Fallback to mock data if API is unavailable
      return this.getMockData();
    }
  }

  // Mock data fallback
  getMockData() {
    return {
      stations: [
        { id: 'SCC1', status: 'Active', customerCount: 7, averageDwellTime: 162.9 },
        { id: 'SCC2', status: 'Active', customerCount: 3, averageDwellTime: 45.2 },
        { id: 'SCC3', status: 'Active', customerCount: 6, averageDwellTime: 76.2 },
        { id: 'SCC4', status: 'Active', customerCount: 2, averageDwellTime: 32.1 },
        { id: 'RC1', status: 'Active', customerCount: 1, averageDwellTime: 15.5 }
      ],
      totalCustomers: 19,
      virtualQueueStations: ['SCC1', 'SCC3']
    };
  }

  // Get current station data (for initial load)
  async getCurrentStationData() {
    const data = await this.fetchStationData();
    return data.stations;
  }

  // Get total customers in queue
  async getTotalCustomersInQueue() {
    const data = await this.fetchStationData();
    return data.totalCustomers;
  }

  // Get stations needing virtual queue
  async getStationsNeedingVirtualQueue() {
    const data = await this.fetchStationData();
    return data.virtualQueueStations;
  }

  // Join virtual queue for a station
  async generateVirtualQueueToken(stationId) {
    try {
      const response = await axios.post(`${API_BASE_URL}/virtual-queue/join`, {
        station_id: stationId
      });
      return response.data.token;
    } catch (error) {
      console.error('Error joining virtual queue:', error);
      // Fallback to mock token generation
      return `VQ-${stationId}-${Date.now().toString(36).toUpperCase()}`;
    }
  }

  // Check queue status for a token
  async checkQueueStatus(token) {
    try {
      const response = await axios.get(`${API_BASE_URL}/virtual-queue/status/${token}`);
      return response.data;
    } catch (error) {
      console.error('Error checking queue status:', error);
      // Fallback mock status
      return {
        token,
        stationId: token.split('-')[1] || 'SCC1',
        isReady: Math.random() > 0.7, // 30% chance ready
        estimatedTime: Math.floor(Math.random() * 10) + 1,
        queuePosition: Math.floor(Math.random() * 5) + 1,
        totalInQueue: 15
      };
    }
  }

  // Subscribe to real-time updates
  subscribe(callback) {
    this.subscribers.push(callback);
    
    // Return unsubscribe function
    return () => {
      this.subscribers = this.subscribers.filter(sub => sub !== callback);
    };
  }

  // Cleanup
  destroy() {
    if (this.pollingInterval) {
      clearInterval(this.pollingInterval);
    }
    this.subscribers = [];
  }
}

export default new RealQueueDataService();