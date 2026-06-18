package contracts

type Position struct {
	X int `json:"x"`
	Y int `json:"y"`
}

type Heading struct {
	DX int `json:"dx"`
	DY int `json:"dy"`
}

type Agent struct {
	ID               string   `json:"id"`
	Role             string   `json:"role"`
	Status           string   `json:"status"`
	Position         Position `json:"position"`
	Heading          Heading  `json:"heading"`
	BehaviourProfile string   `json:"behaviour_profile,omitempty"`
}

type Simulation struct {
	Tick       int    `json:"tick"`
	Status     string `json:"status"`
	Width      int    `json:"width"`
	Height     int    `json:"height"`
	AgentCount int    `json:"agent_count"`
	Seed       int    `json:"seed"`
	UpdatedAt  string `json:"updated_at"`
	Metrics    any    `json:"metrics,omitempty"`
}

type Terrain struct {
	RestrictedCells []Position `json:"restricted_cells"`
	Note            string     `json:"note"`
	Map             any        `json:"map,omitempty"`
}

type ModelSnapshot struct {
	Simulation Simulation `json:"simulation"`
	Terrain    Terrain    `json:"terrain"`
	Agents     []Agent    `json:"agents"`
}

type APISnapshot struct {
	Source     string     `json:"source"`
	ReceivedAt string     `json:"received_at"`
	Simulation Simulation `json:"simulation"`
	Terrain    Terrain    `json:"terrain"`
	Agents     []Agent    `json:"agents"`
	Warnings   []string   `json:"warnings"`
}

type Health struct {
	Status string `json:"status"`
	Model  string `json:"model"`
}

type APIError struct {
	Error string `json:"error"`
}
