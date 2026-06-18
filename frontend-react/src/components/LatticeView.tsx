import type { Agent, Position, TerrainMap } from "../api/simulation";

type Props = {
  width: number;
  height: number;
  agents: Agent[];
  restrictedCells: Position[];
  terrainMap?: TerrainMap;
};

const roleClass: Record<string, string> = {
  civilian: "agentCivilian",
  staff: "agentStaff",
  patrol: "agentPatrol"
};

export function LatticeView({ width, height, agents, restrictedCells, terrainMap }: Props) {
  if (terrainMap) {
    return (
      <div
        className="terrainViewport"
        style={{ aspectRatio: `${width} / ${height}` }}
        aria-label="Terrain map simulation"
      >
        <img
          className="terrainImage"
          src={terrainMap.asset_path}
          alt="Terrain map"
          draggable={false}
        />
        <div className="agentOverlay" aria-hidden="true">
          {agents.map((agent) => (
            <span
              className={`mapAgent ${roleClass[agent.role] ?? "agentDefault"}`}
              key={agent.id}
              title={`${agent.id} ${agent.role}`}
              style={{
                left: `${(agent.position.x / Math.max(1, width - 1)) * 100}%`,
                top: `${(agent.position.y / Math.max(1, height - 1)) * 100}%`
              }}
            />
          ))}
        </div>
      </div>
    );
  }

  const restricted = new Set(restrictedCells.map((cell) => `${cell.x}:${cell.y}`));
  const agentsByCell = new Map<string, Agent[]>();

  for (const agent of agents) {
    const key = `${agent.position.x}:${agent.position.y}`;
    agentsByCell.set(key, [...(agentsByCell.get(key) ?? []), agent]);
  }

  const cells = [];
  for (let y = 0; y < height; y += 1) {
    for (let x = 0; x < width; x += 1) {
      const key = `${x}:${y}`;
      const cellAgents = agentsByCell.get(key) ?? [];
      const firstAgent = cellAgents[0];
      const classes = [
        "cell",
        restricted.has(key) ? "restrictedCell" : "",
        firstAgent ? "occupiedCell" : ""
      ]
        .filter(Boolean)
        .join(" ");

      cells.push(
        <div className={classes} key={key} title={`x ${x}, y ${y}`}>
          {firstAgent ? (
            <span className={`agent ${roleClass[firstAgent.role] ?? "agentDefault"}`}>
              {cellAgents.length > 1 ? cellAgents.length : firstAgent.role[0]?.toUpperCase()}
            </span>
          ) : null}
        </div>
      );
    }
  }

  return (
    <div
      className="lattice"
      style={{ gridTemplateColumns: `repeat(${width}, minmax(0, 1fr))` }}
      aria-label="Simulation lattice"
    >
      {cells}
    </div>
  );
}
