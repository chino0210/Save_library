import "./index.css"
import Header from "./components/Header"
import NavBar from "./components/NavBar";

import Home from "./views/Home"
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

function App() {
  return (
    <>
      < Header />
      < Router>
        < NavBar />
        < Routes >
          < Route pat="/" element={< Home />}/>
        </Routes>
      </Router>
    </>
  )
}

export default App
