import styled from "styled-components";

import Color from "../../assets/colors";

export const SearchButtonWrapper = styled.button`
	height: 50px;
	width: 100px;
	display: inline-block;
	border-radius: 10px;
	box-shadow: 5px 5px;

	&:hover {
		background: ${Color.silver};
	}
`;
