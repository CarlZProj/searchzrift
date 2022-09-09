import React from "react";
import { useNavigate } from "react-router-dom";

import { SearchButtonWrapper } from "./styles";

import { setGlobalState } from "../../state";
import { controller } from "../../pages/LobbyPage";

const SearchButton = () => {
	const navigate = useNavigate();

	return (
		<SearchButtonWrapper
			onClick={() => {
				if (controller) controller.abort();
				setGlobalState("defaultLobbyState", -1);
				navigate("/lobby");
			}}
		>
			Search
		</SearchButtonWrapper>
	);
};

export default SearchButton;
