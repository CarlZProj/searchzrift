import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import HeaderBar from "./components/HeaderBar";
import HomePage from "./pages/HomePage";
import LobbyPage from "./pages/LobbyPage";

import { AppContainer } from "./styles";

const App = () => {
	return (
		<Router>
			<div className="app">
				<AppContainer>
					<HeaderBar />
					<Routes>
						<Route exact path="/" element={<HomePage />} />
						<Route exact path="/lobby/" element={<LobbyPage />} />
					</Routes>
				</AppContainer>
			</div>
		</Router>
	);
};

export default App;
