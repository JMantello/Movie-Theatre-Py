import './App.css';
import { Route, Routes } from "react-router-dom"
import Login from './page-views/Login'
import Feed from './page-views/Feed'

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/login" element={<Login />} />
        <Route path="/feed" element={<Feed />} />
      </Routes>
    </div>
  );
}

export default App;
