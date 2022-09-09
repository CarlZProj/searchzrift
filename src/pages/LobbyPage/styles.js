import styled from "styled-components";

import Color from "../../assets/colors";

export const LobbyPageWrapper = styled.div`
	height: 90vh;
	width: 100%;
	border: 2px solid ${Color.white};
`;

export const LobbyDecision = styled.h1`
	height: 10vh;
	min-height: 75px;
	width: 100%;
	border-bottom: 2px solid ${Color.white};
	color: ${Color.white};
	display: flex;
	align-items: center;
	justify-content: center;
	font-size: 64px;
	font-family: copperplate, fantasy;
`;

export const SummonerWrapper = styled.div`
	height: 70vh;
	width: 100%;

	@media screen and (max-width: 1025px) {
		height: 42vh;
		overflow-y: scroll;

		&::-webkit-scrollbar {
			display: none;
		}
	}
`;

export const ErrorMessage = styled.p`
	height: 20vh;
	min-height: 200px;
	width: 100%;
	color: ${Color.white};
	display: flex;
	align-items: center;
	justify-content: center;
	text-align: center;
	font-size: 36px;
	font-family: copperplate, fantasy;
`;

export const LobbyImg = styled.img`
	min-height: 100px;
	width: 50%;
	display: block;
	margin: 0 auto;
`;

export const Footer = styled.div`
	height: 10vh;
	min-height: 50px;
	width: 100%;
	border-top: 2px solid ${Color.white};
`;
