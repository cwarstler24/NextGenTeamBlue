/**
 * API Configuration
 * Determines the correct backend URL based on environment
 */

// In Docker: use relative paths (goes through nginx)
// In development (local): use localhost:8000
const getApiBase = () => {
  // Check if we're accessing via localhost:PORT pattern (local dev)
  // The key indicator: if port exists AND it's a dev port (3000, 5173, etc.), use direct backend
  // Otherwise, use relative paths (goes through nginx)
  
  const hostname = window.location.hostname;
  const port = window.location.port;
  
  // Development mode: accessing via localhost:3000, localhost:5173, etc.
  if ((hostname === 'localhost' || hostname === '127.0.0.1') && port && port !== '80' && port !== '443') {
    // Development environment with dev server - direct to backend
    return 'http://127.0.0.1:8000';
  } else {
    // Docker/Production environment - use relative path (goes through nginx)
    return '';
  }
};

export const API_BASE = getApiBase();
