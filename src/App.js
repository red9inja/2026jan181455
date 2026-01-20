import React, { useState, useEffect } from 'react';
import { Amplify, Auth, Storage, API } from 'aws-amplify';
import { withAuthenticator } from '@aws-amplify/ui-react';
import '@aws-amplify/ui-react/styles.css';
import './App.css';

// Amplify configuration will be set via environment variables
const amplifyConfig = {
  Auth: {
    region: process.env.REACT_APP_AWS_REGION || 'us-east-1',
    userPoolId: process.env.REACT_APP_USER_POOL_ID,
    userPoolWebClientId: process.env.REACT_APP_USER_POOL_CLIENT_ID,
    identityPoolId: process.env.REACT_APP_IDENTITY_POOL_ID,
  },
  Storage: {
    AWSS3: {
      bucket: process.env.REACT_APP_S3_BUCKET,
      region: process.env.REACT_APP_AWS_REGION || 'us-east-1',
    }
  },
  API: {
    endpoints: [
      {
        name: "api",
        endpoint: process.env.REACT_APP_API_ENDPOINT,
        region: process.env.REACT_APP_AWS_REGION || 'us-east-1',
      }
    ]
  }
};

Amplify.configure(amplifyConfig);

function App({ signOut, user }) {
  const [files, setFiles] = useState([]);
  const [uploadStatus, setUploadStatus] = useState('');
  const [apiData, setApiData] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchApiData();
    listFiles();
  }, []);

  const fetchApiData = async () => {
    try {
      setLoading(true);
      const response = await API.get('api', '/users');
      setApiData(response);
    } catch (error) {
      console.error('Error fetching API data:', error);
    } finally {
      setLoading(false);
    }
  };

  const listFiles = async () => {
    try {
      const filesList = await Storage.list('');
      setFiles(filesList);
    } catch (error) {
      console.error('Error listing files:', error);
    }
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    try {
      setUploadStatus('Uploading...');
      const result = await Storage.put(`uploads/${file.name}`, file, {
        contentType: file.type,
      });
      setUploadStatus('Upload successful!');
      listFiles(); // Refresh file list
      setTimeout(() => setUploadStatus(''), 3000);
    } catch (error) {
      console.error('Error uploading file:', error);
      setUploadStatus('Upload failed!');
      setTimeout(() => setUploadStatus(''), 3000);
    }
  };

  const createUser = async () => {
    try {
      const userData = {
        name: user.attributes.name || 'Demo User',
        email: user.attributes.email,
        timestamp: new Date().toISOString()
      };
      
      const response = await API.post('api', '/users', {
        body: userData
      });
      
      console.log('User created:', response);
      fetchApiData(); // Refresh data
    } catch (error) {
      console.error('Error creating user:', error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>AWS Demo Application</h1>
        <div className="user-info">
          <p>Welcome, {user.attributes.email}!</p>
          <button onClick={signOut} className="sign-out-btn">Sign Out</button>
        </div>
      </header>

      <main className="App-main">
        <div className="demo-section">
          <h2>Cognito Authentication</h2>
          <p>User authenticated successfully!</p>
          <p>User ID: {user.attributes.sub}</p>
          <p>Email: {user.attributes.email}</p>
        </div>

        <div className="demo-section">
          <h2>S3 File Upload</h2>
          <input 
            type="file" 
            onChange={handleFileUpload}
            className="file-input"
          />
          {uploadStatus && <p className="status">{uploadStatus}</p>}
          
          <h3>Uploaded Files:</h3>
          <ul className="file-list">
            {files.map((file, index) => (
              <li key={index}>{file.key}</li>
            ))}
          </ul>
        </div>

        <div className="demo-section">
          <h2>Lambda API</h2>
          <button onClick={createUser} className="api-btn">
            Create User via Lambda
          </button>
          <button onClick={fetchApiData} className="api-btn">
            Fetch Data
          </button>
          
          {loading && <p>Loading...</p>}
          {apiData && (
            <div className="api-response">
              <h3>API Response:</h3>
              <pre>{JSON.stringify(apiData, null, 2)}</pre>
            </div>
          )}
        </div>

        <div className="demo-section">
          <h2>Infrastructure Status</h2>
          <div className="status-grid">
            <div className="status-item">
              <span className="status-icon">Active</span>
              <span>Amplify Hosting</span>
            </div>
            <div className="status-item">
              <span className="status-icon">Active</span>
              <span>Cognito Auth</span>
            </div>
            <div className="status-item">
              <span className="status-icon">Active</span>
              <span>S3 Storage</span>
            </div>
            <div className="status-item">
              <span className="status-icon">Active</span>
              <span>Lambda Functions</span>
            </div>
            <div className="status-item">
              <span className="status-icon">Active</span>
              <span>ECS Backend</span>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default withAuthenticator(App);
