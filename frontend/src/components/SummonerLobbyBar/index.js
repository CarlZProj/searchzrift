import React from "react";

import {
	SummonerLobbyBarWrapper,
	Name,
	TierRank,
	MainRole,
	MainRoleIcon,
	InfoWrapper,
	InfoTextSmall,
	InfoTextLarge,
	TextBox,
} from "./styles";

function round(num) {
	return Math.round(num * 100) / 100;
}

function convertToPercent(num) {
	return Math.ceil(num * 100) + "%";
}

const getMainRoleIcon = (tier, mainRole) => {
	var mainRoleIcon;

	try {
		tier = tier.toLowerCase();
		mainRole = mainRole.toLowerCase();
		mainRoleIcon = require(`../../assets/positions/${tier}_${mainRole}.png`);
	} catch (err) {
		mainRoleIcon = require(`../../assets/positions/iron_${mainRole}.png`);
	}

	return mainRoleIcon;
};

const SummonerLobbyBar = ({ name, data }) => {
	if (data == null) {
		return (
			<SummonerLobbyBarWrapper matchRating={null} dne={true}>
				<Name dne={true}>{name}</Name>
				<TextBox>Could not find summoner</TextBox>
			</SummonerLobbyBarWrapper>
		);
	}

	if (data == "loading") {
		return (
			<SummonerLobbyBarWrapper matchRating={null} dne={true}>
				<Name dne={true}>{name}</Name>
				<TextBox>Loading summoner</TextBox>
			</SummonerLobbyBarWrapper>
		);
	}

	if (data.tier == null) data.tier = "UNRANKED";

	return (
		<SummonerLobbyBarWrapper matchRating={round(data.match_rating)}>
			<Name>{name}</Name>
			<TierRank>
				{data.tier} {data.rank}
			</TierRank>
			<MainRole>
				<MainRoleIcon
					src={getMainRoleIcon(data.tier, data.main_role)}
					alt="Main Role Icon"
				/>
			</MainRole>
			<InfoWrapper responsivePlacement={"left"}>
				<InfoTextSmall>Winrate in last 10</InfoTextSmall>
				<InfoTextLarge>{convertToPercent(data.win_rate)}</InfoTextLarge>
			</InfoWrapper>
			<InfoWrapper size={"large"} responsivePlacement={"center"}>
				<InfoTextSmall>{round(data.kda)} KDA</InfoTextSmall>
				<InfoTextLarge>
					{round(data.avg_kills)} / {round(data.avg_deaths)} /{" "}
					{round(data.avg_assists)}
				</InfoTextLarge>
			</InfoWrapper>
			<InfoWrapper size={"small"} responsivePlacement={"right"}>
				<InfoTextSmall>KP</InfoTextSmall>
				<InfoTextLarge>
					{convertToPercent(round(data.kill_participation))}
				</InfoTextLarge>
			</InfoWrapper>
			<InfoWrapper responsivePlacement={"left"}>
				<InfoTextSmall>Damage Share</InfoTextSmall>
				<InfoTextLarge>
					{convertToPercent(round(data.damage_participation))}
				</InfoTextLarge>
			</InfoWrapper>
			<InfoWrapper responsivePlacement={"center"}>
				<InfoTextSmall>Vision Score / Min</InfoTextSmall>
				<InfoTextLarge>{round(data.vision_score_per_min)}</InfoTextLarge>
			</InfoWrapper>
			<InfoWrapper responsivePlacement={"right"}>
				<InfoTextSmall>Match Rating</InfoTextSmall>
				<InfoTextLarge>{round(data.match_rating)}</InfoTextLarge>
			</InfoWrapper>
		</SummonerLobbyBarWrapper>
	);
};

export default SummonerLobbyBar;
