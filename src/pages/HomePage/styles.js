import styled from "styled-components";

import Color from "../../assets/colors";

export const HomePageWrapper = styled.div`
	width: 100vw;
	height: 90vh;
	border: 2px solid ${Color.white};
`;

export const Img = styled.img`
	width: 100vw;
	height: 90vh;

	@media screen and (max-width: 1420px) { # --- 1280px (img) + 100px (header) + 10px * 4 (padding) ---
		height: 150vh;
        object-fit: cover;
        object-position: 70% 1-10h;
	}
`;
