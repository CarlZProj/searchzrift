import { createGlobalState } from "react-hooks-global-state";

const { setGlobalState, useGlobalState } = createGlobalState({
	defaultSearchString: "",
	defaultServer: "",
	defaultLobbyState: -1,
	defaultLobbyData: {},
});

export { useGlobalState, setGlobalState };
