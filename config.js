export default {
  mongodb: {
    // The connection URL for the MongoDB database
    // Format: mongodb://[username:password@]host[:port][/database][?options]
    url: process.env.ME_CONFIG_MONGODB_URL || 'mongodb://root:example@mongo:27017/', //Default Url if env variable is empty
    // Whether or not to enable SSL connection (default: false)
    ssl: false,
    // Number of databases to display in the UI (default: 5)
    max_databases: 5,
    // The name of the database to use for Mongo Express itself
    admin: true,
  },

  site: {
    // Base URL for the app
    baseUrl: '/',
    // Web server port (default: 8081)
    port: 8081,
  },

  // Enable HTTP Basic authentication
  basicAuth: {
    username: process.env.ME_CONFIG_MONGODB_ADMINUSERNAME || 'root', //Default Username if env variable is empty
    password: process.env.ME_CONFIG_MONGODB_ADMINPASSWORD || 'cesidil2', //Default Password if env variable is empty
  },

  //Set how collection will be displayed and how
  options: {
    collections: {
      Sensor_Station: {
        displayFields: ['_id', 'Mac_Id', 'Name', 'City', 'Creation_Date'], //All field of Sensor_Station collection who will be shown on the interface
      },
      Statement: {
        displayFields: ['Id_Sensor_Station_F', 'Temperature', 'Humidity', 'Pressure', 'Date', 'Time'],//All field of Statement collection who will be shown on the interface
      },
    },
  },
};