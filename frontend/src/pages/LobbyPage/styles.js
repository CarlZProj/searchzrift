import styled from "styled-components";

import Color from "../../assets/colors";

export const LobbyPageWrapper = styled.div`
    height: 80vh;
	border: 2px solid ${Color.white};

    @media screen and (max-width: 1420px)
		overflow-y: scroll;
	}
`;

export const LobbyDecision = styled.h1`
	height: 10vh;
	width: 100%;
	color: ${Color.white};
	display: flex;
	align-items: center;
	justify-content: center;
	font-size: 64px;
	font-family: copperplate, fantasy;
`;

export const ErrorMessage = styled.p`
	height: 20vh;
	width: 100%;
	color: ${Color.white};
	display: flex;
	align-items: center;
	justify-content: center;
	text-align: center;
	font-size: 36px;
	font-family: copperplate, fantasy;
`;

export const ExampleString = styled.p`
	height: 20vh;
	width: 100%;
	color: ${Color.white};
	display: flex;
	align-items: center;
	justify-content: center;
	text-align: center;
	font-size: 24px;
	font-family: copperplate, fantasy;
`;
