// Engine-neutral selection contract; no rendering imports.
export function receiverMode(policy){const mode=policy?.receiver_lookup?.selected_mode;if(!['raw','receiver-plane'].includes(mode))throw Error('Explicit registered receiver lookup required');return mode;}
