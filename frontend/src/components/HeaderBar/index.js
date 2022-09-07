import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";

import {
	HeaderBarWrapper,
	ServerSelect,
	ServerOption,
	SummonerSearchBarInput,
	Title,
} from "./styles";
import SearchButton from "../SearchButton";

import { setGlobalState } from "../../state";
import { controller } from "../../pages/LobbyPage";

const options = [
	{
		label: "North America",
		value: "na1",
	},
	{
		label: "Republic of Korea",
		value: "kr",
	},
	{
		label: "Europe West",
		value: "euw1",
	},
	{
		label: "Europe Nordic & East",
		value: "eun1",
	},
	{
		label: "Brazil",
		value: "br1",
	},
	{
		label: "Latin America North",
		value: "la1",
	},
	{
		label: "Latin America South",
		value: "la2",
	},
	{
		label: "Oceania",
		value: "oc1",
	},
	{
		label: "Russia",
		value: "ru",
	},
	{
		label: "Turkey",
		value: "tr1",
	},
	{
		label: "Japan",
		value: "jp1",
	},
];

// note: consider auto generating dropdown for regions
const HeaderBar = () => {
	const navigate = useNavigate();

	useEffect(() => {
		setGlobalState("defaultServer", options[0].value);
	}, []);

	const handleInput = (e) => {
		setGlobalState("defaultSearchString", e.target.value);
	};

	const handleSelect = (e) => {
		setGlobalState("defaultServer", e.target.value);
	};

	return (
		<HeaderBarWrapper>
			<Title
				onClick={() => {
					if (controller) controller.abort();
					setGlobalState("defaultLobbyState", -1);
					navigate("/");
				}}
			>
				SearchZRift
			</Title>
			<SummonerSearchBarInput
				type="text"
				id="summoner-search"
				placeholder="Summoner1, Summoner2, Summoner3, Summoner4, Summoner5"
				onInput={handleInput}
				onKeyPress={() => {}}
			/>
			<ServerSelect
				title="server dropdown"
				id="server-dropdown"
				onChange={handleSelect}
			>
				{options.map((o) => (
					<ServerOption key={o.value} value={o.value}>
						{o.label}
					</ServerOption>
				))}
			</ServerSelect>
			<SearchButton />
		</HeaderBarWrapper>
	);
};

export default HeaderBar;
