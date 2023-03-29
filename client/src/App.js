import './App.css';
import { Route, Routes } from "react-router-dom"
import Login from './page-views/Login'

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/login" element={<Login />} />
      </Routes>
    </div>
  );
}

export default App;
