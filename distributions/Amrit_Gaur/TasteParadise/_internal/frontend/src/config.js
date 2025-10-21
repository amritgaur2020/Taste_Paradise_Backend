const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'http://127.0.0.1:8002' 
  : 'http://localhost:8002';

export default API_BASE_URL;
