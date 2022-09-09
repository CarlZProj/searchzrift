import React from "react";

import { HomePageWrapper, Img } from "./styles";

const summonersRiftImage = require("../../assets/summoners_rift.jpg");

const HomePage = () => {
	return (
		<HomePageWrapper>
			<Img src={summonersRiftImage} alt="summoner's rift" />
		</HomePageWrapper>
	);
};

export default HomePage;
