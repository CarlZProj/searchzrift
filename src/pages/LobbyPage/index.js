import React, { useEffect } from "react";
import axios from "axios";

import SummonerLobbyBar from "../../components/SummonerLobbyBar";

import {
	ErrorMessage,
	Footer,
	LobbyDecision,
	LobbyImg,
	LobbyPageWrapper,
	SummonerWrapper,
} from "./styles";

import { useGlobalState, setGlobalState } from "../../state";

const baseUrl =
	process.env.REACT_APP_PROD === "prod"
		? "https://searchzrift.herokuapp.com"
		: "http://127.0.0.1:8000";

const searchLobbyUrl = `${baseUrl}/api/lobby/`;

const lobbyExampleImage = require("../../assets/lobby_example.png");
let summoners = [];
let validString = false;

export let controller = null;

const dodgeOrPlay = (summoners) => {
	var summonerMatchRatings = [];

	for (let i = 0; i < 5; i++) {
		if (summoners[i] != null)
			summonerMatchRatings.push(summoners[i].match_rating);
	}

	const sum = summonerMatchRatings.reduce((a, b) => a + b, 0);
	const avg = sum / summonerMatchRatings.length || 0;

	if (avg > 65) return "PLAY";
	else return "DODGE";
};

const LobbyPage = () => {
	const [server] = useGlobalState("defaultServer");
	const [searchString] = useGlobalState("defaultSearchString");
	const [lobbyState] = useGlobalState("defaultLobbyState");
	const [lobbyData] = useGlobalState("defaultLobbyData");

	function handleSearchString(searchString) {
		let summonerNames = [];

		const joinedTheLobbyRegExp = new RegExp(
			"(.*)(?: joined the lobby)(.*)(?: joined the lobby)(.*)(?: joined the lobby)(.*)(?: joined the lobby)(.*)(?: joined the lobby)"
		);
		const commaRegExp = new RegExp(
			"(.*)(?:, )(.*)(?:, )(.*)(?:, )(.*)(?:, )(.*)"
		);

		if (joinedTheLobbyRegExp.test(searchString)) {
			// DigitalDirty joined the lobby Artavian joined the lobby ONPRaGu joined the lobby Triton4C joined the lobby CarlZLegend joined the lobby
			summonerNames = searchString.split(" joined the lobby ", 5);

			// remove " joined the lobby" from last summoner name
			summonerNames[4] = summonerNames[4].substring(
				0,
				summonerNames[4].length - 17
			);
		} else if (commaRegExp.test(searchString)) {
			// DigitalDirty, Artavian, ONPRaGu, Triton4C, CarlZLegend
			summonerNames = searchString.split(", ", 5);
		} else {
			// error state
			setGlobalState("defaultLobbyState", 2);
		}

		if (summonerNames.length === 0) validString = false;
		else validString = true;
		return summonerNames;
	}

	try {
		useEffect(() => {
			async function getSummoners() {
				controller = new AbortController();
				await axios
					.get(searchLobbyUrl, {
						signal: controller.signal,
						params: {
							server: server,
							summoner1: summoners[0],
							summoner2: summoners[1],
							summoner3: summoners[2],
							summoner4: summoners[3],
							summoner5: summoners[4],
						},
					})
					.then((res) => {
						setGlobalState("defaultLobbyData", res.data);
						setGlobalState("defaultLobbyState", 1);
					})
					.catch(() => console.log("Cancel Request"));
			}

			summoners = handleSearchString(searchString);

			if (lobbyState === -1) setGlobalState("defaultLobbyState", 0); // used to rerender with summoner names when search is pressed
			if (validString && lobbyState === 0) getSummoners();
		}, [lobbyState, server]); // no dependency on searchString
	} catch (err) {
		console.log("Lobby Search Problem Has Occured");
		setGlobalState("defaultLobbyState", 2);
	}

	if (lobbyState === -1 || lobbyState === 0) {
		return (
			<LobbyPageWrapper scroll={false}>
				<LobbyDecision>LOADING</LobbyDecision>
				<SummonerWrapper>
					<SummonerLobbyBar name={summoners[0]} data={"loading"} />
					<SummonerLobbyBar name={summoners[1]} data={"loading"} />
					<SummonerLobbyBar name={summoners[2]} data={"loading"} />
					<SummonerLobbyBar name={summoners[3]} data={"loading"} />
					<SummonerLobbyBar name={summoners[4]} data={"loading"} />
				</SummonerWrapper>
				<Footer />
			</LobbyPageWrapper>
		);
	} else if (lobbyState === 1) {
		return (
			<LobbyPageWrapper scroll={true}>
				<LobbyDecision>
					{dodgeOrPlay([
						lobbyData[summoners[0]],
						lobbyData[summoners[1]],
						lobbyData[summoners[2]],
						lobbyData[summoners[3]],
						lobbyData[summoners[4]],
					])}
				</LobbyDecision>
				<SummonerWrapper>
					<SummonerLobbyBar
						name={summoners[0]}
						data={lobbyData[summoners[0]]}
					/>
					<SummonerLobbyBar
						name={summoners[1]}
						data={lobbyData[summoners[1]]}
					/>
					<SummonerLobbyBar
						name={summoners[2]}
						data={lobbyData[summoners[2]]}
					/>
					<SummonerLobbyBar
						name={summoners[3]}
						data={lobbyData[summoners[3]]}
					/>
					<SummonerLobbyBar
						name={summoners[4]}
						data={lobbyData[summoners[4]]}
					/>
				</SummonerWrapper>
				<Footer />
			</LobbyPageWrapper>
		);
	} else if (lobbyState === 2) {
		return (
			<LobbyPageWrapper scroll={false}>
				<LobbyDecision>ERROR</LobbyDecision>
				<ErrorMessage>
					You may have entered an invalid string. Copy paste the 5 players from
					your champion select lobby in the League of Legends Client.
				</ErrorMessage>
				<LobbyImg src={lobbyExampleImage} alt={"league client lobby"} />
			</LobbyPageWrapper>
		);
	}
};

export default LobbyPage;
