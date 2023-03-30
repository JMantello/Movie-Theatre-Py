let apiURL;

if (process.env.NODE_ENV === 'development') {
    apiURL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:5000/';
} else {
    apiURL = '/'
}

export default apiURL;