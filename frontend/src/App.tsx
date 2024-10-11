import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Upload from "./components/UploadPage";
import Results from "./components/ResultsPage";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Upload />}></Route>
        <Route path="/result" element={<Results />}></Route>
      </Routes>
    </Router>
  );
}

export default App;
