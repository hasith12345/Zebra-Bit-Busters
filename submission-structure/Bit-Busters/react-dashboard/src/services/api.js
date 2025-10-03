// Example API service for integrating with the Python backend
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

class DashboardAPI {
  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 5000,
    });
  }

  // Fetch dashboard data from Python backend
  async getDashboardData() {
    try {
      const response = await this.client.get('/api/dashboard');
      return response.data;
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      throw error;
    }
  }

  // Fetch recent events
  async getRecentEvents(limit = 15) {
    try {
      const response = await this.client.get(`/api/events?limit=${limit}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching events:', error);
      throw error;
    }
  }

  // Fetch station status
  async getStationStatus() {
    try {
      const response = await this.client.get('/api/stations');
      return response.data;
    } catch (error) {
      console.error('Error fetching station status:', error);
      throw error;
    }
  }

  // Fetch system metrics
  async getSystemMetrics() {
    try {
      const response = await this.client.get('/api/metrics');
      return response.data;
    } catch (error) {
      console.error('Error fetching system metrics:', error);
      throw error;
    }
  }
}

export default new DashboardAPI();