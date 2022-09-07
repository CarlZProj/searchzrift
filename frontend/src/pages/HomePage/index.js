import React from "react";

import { HomePageWrapper, Img } from "./styles";

const SummonersRiftImage = require("../../assets/summoners_rift.jpg");

const HomePage = () => {
	return (
		<HomePageWrapper>
			<Img src={SummonersRiftImage} alt="Summoner's Rift" />
		</HomePageWrapper>
	);
};

export default HomePage;
