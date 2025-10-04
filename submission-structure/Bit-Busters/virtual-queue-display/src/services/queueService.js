// Mock data service that simulates reading from queue_monitoring.jsonl
// In a real implementation, this would connect to your backend API

class QueueDataService {
  constructor() {
    this.currentData = new Map();
    this.virtualQueues = new Map();
    this.simulateRealTimeData();
  }

  // Simulate reading queue monitoring data
  simulateRealTimeData() {
    // Sample data based on the actual queue_monitoring.jsonl structure
    const sampleStations = [
      { 
        station_id: 'SCC1', 
        status: 'Active', 
        customer_count: 7, 
        average_dwell_time: 162.9 
      },
      { 
        station_id: 'SCC2', 
        status: 'Active', 
        customer_count: 3, 
        average_dwell_time: 45.2 
      },
      { 
        station_id: 'SCC3', 
        status: 'Active', 
        customer_count: 6, 
        average_dwell_time: 76.2 
      },
      { 
        station_id: 'SCC4', 
        status: 'Active', 
        customer_count: 2, 
        average_dwell_time: 32.1 
      },
      { 
        station_id: 'RC1', 
        status: 'Active', 
        customer_count: 1, 
        average_dwell_time: 15.5 
      }
    ];

    // Update current data
    sampleStations.forEach(station => {
      this.currentData.set(station.station_id, station);
    });

    // Simulate data updates every 5 seconds
    setInterval(() => {
      this.updateSimulatedData();
    }, 5000);
  }

  updateSimulatedData() {
    // Simulate random changes in queue data
    this.currentData.forEach((station, stationId) => {
      const change = Math.floor(Math.random() * 3) - 1; // -1, 0, or 1
      const newCount = Math.max(0, Math.min(10, station.customer_count + change));
      
      this.currentData.set(stationId, {
        ...station,
        customer_count: newCount,
        average_dwell_time: newCount > 0 ? Math.random() * 180 + 30 : 0
      });
    });
  }

  // Get all current station data
  getCurrentStationData() {
    return Array.from(this.currentData.values()).map(station => ({
      id: station.station_id,
      status: station.status,
      customerCount: station.customer_count,
      averageDwellTime: station.average_dwell_time
    }));
  }

  // Get total customers across all stations
  getTotalCustomersInQueue() {
    return Array.from(this.currentData.values())
      .reduce((total, station) => total + station.customer_count, 0);
  }

  // Get stations that need virtual queue (>= 6 customers)
  getStationsNeedingVirtualQueue() {
    return Array.from(this.currentData.values())
      .filter(station => station.customer_count >= 6)
      .map(station => station.station_id);
  }

  // Generate a virtual queue token
  generateVirtualQueueToken(stationId) {
    const token = `VQ-${stationId}-${Date.now().toString(36).toUpperCase()}`;
    const position = this.currentData.get(stationId)?.customer_count || 0;
    
    this.virtualQueues.set(token, {
      stationId,
      position,
      timestamp: new Date(),
      estimatedWaitTime: this.calculateWaitTime(stationId, position)
    });

    return token;
  }

  // Calculate estimated wait time
  calculateWaitTime(stationId, position) {
    const station = this.currentData.get(stationId);
    if (!station || station.customer_count === 0) return 0;
    
    // Estimate based on average dwell time and queue position
    const avgServiceTime = station.average_dwell_time;
    return Math.round((avgServiceTime * position) / 60); // Convert to minutes
  }

  // Check if customer's turn is ready
  checkQueueStatus(token) {
    const queueData = this.virtualQueues.get(token);
    if (!queueData) return null;

    const currentStation = this.currentData.get(queueData.stationId);
    if (!currentStation) return null;

    // Simulate queue progression - in real app, this would be based on actual queue movement
    const timePassed = (Date.now() - queueData.timestamp.getTime()) / 1000; // seconds
    const isReady = timePassed > 30 || currentStation.customer_count < 3; // Ready after 30 seconds or if queue is short

    return {
      token,
      stationId: queueData.stationId,
      isReady,
      estimatedTime: isReady ? 0 : Math.max(1, queueData.estimatedWaitTime - Math.floor(timePassed / 60)),
      queuePosition: isReady ? 0 : Math.max(1, currentStation.customer_count - 2),
      totalInQueue: this.getTotalCustomersInQueue()
    };
  }

  // Subscribe to real-time updates
  subscribe(callback) {
    const interval = setInterval(() => {
      callback(this.getCurrentStationData());
    }, 2000);

    return () => clearInterval(interval);
  }
}

export default new QueueDataService();