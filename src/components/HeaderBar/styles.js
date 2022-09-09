import styled from "styled-components";

import Color from "../../assets/colors";

export const HeaderBarWrapper = styled.div`
	height: 10vh;
	min-height: 100px;
	padding: 20px;
	border: 2px solid ${Color.white};
	display: flex;
	justify-content: center;

	@media screen and (max-width: 1025px) {
		height: 40vh;
		min-height: 200px;
		display: flex;
		flex-direction: column;
		align-items: center;
	}
`;

export const Title = styled.button`
	height: 50px;
	min-height: 50px;
	width: 20vw;
	border: none;
	background: ${Color.deep_violet};
	color: ${Color.white};
	font-family: copperplate, fantasy;
	font-size: 40px;

	@media screen and (max-width: 1025px) {
		width: 90vw;
	}
`;

export const SummonerSearchBarInput = styled.input`
	height: 50px;
	min-height: 50px;
	width: 40vw;
	display: inline-flex;
	margin: 0 10px;
	padding: 10px;
	line-height: 50%;
	border-radius: 10px;
	box-shadow: 5px 5px;

	@media screen and (max-width: 1025px) {
		width: 90vw;
	}
`;

export const ServerSelect = styled.select`
	height: 50px;
	min-height: 50px;
	width: 15vw;
	display: inline-flex;
	margin: 0 10px;
	padding: 10px;
	border-radius: 10px;
	box-shadow: 5px 5px;

	@media screen and (max-width: 1025px) {
		width: 50vw;
	}
`;

export const ServerOption = styled.option`
	height: 50px;
	min-height: 50px;
	width: 10vw;
	display: inline-flex;
	margin: 0 10px;
	padding: 10px;
`;
