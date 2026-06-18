/** @file LatticeView.tsx
 *  @brief Terrain-pattern canvas renderer with agent overlays.
 *
 *  Renders map-backed simulation terrain using the same symbolic color and
 *  stripe language as the generated GIF artifact, while keeping live agents
 *  visible above the terrain layer.
 */

import { useEffect, useRef } from "react";

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

const terrainColors: Record<string, [number, number, number]> = {
  normal: [255, 255, 255],
  boundary: [0, 0, 0],
  densityZeroDark: [136, 0, 21],
  densityZeroLight: [185, 122, 87],
  restricted: [237, 28, 36],
  gate: [255, 127, 39],
  exit: [34, 177, 76],
  typeOne: [63, 72, 204],
  typeTwo: [255, 174, 201],
  light: [248, 250, 247]
};

/** @brief Draw terrain-map pixels with the same color and stripe language used by the GIF artifact. */
function drawTerrainCanvas(canvas: HTMLCanvasElement, terrainMap: TerrainMap) {
  const image = new Image();
  image.onload = () => {
    const width = terrainMap.summary.width || image.naturalWidth;
    const height = terrainMap.summary.height || image.naturalHeight;
    const source = document.createElement("canvas");
    source.width = width;
    source.height = height;
    const sourceContext = source.getContext("2d", { willReadFrequently: true });
    const targetContext = canvas.getContext("2d");
    if (!sourceContext || !targetContext) {
      return;
    }

    canvas.width = width;
    canvas.height = height;
    sourceContext.imageSmoothingEnabled = false;
    sourceContext.drawImage(image, 0, 0, width, height);
    const imageData = sourceContext.getImageData(0, 0, width, height);
    const data = imageData.data;

    for (let y = 0; y < height; y += 1) {
      for (let x = 0; x < width; x += 1) {
        const index = (y * width + x) * 4;
        const color = patternedTerrainColor(data[index], data[index + 1], data[index + 2], x, y);
        data[index] = color[0];
        data[index + 1] = color[1];
        data[index + 2] = color[2];
        data[index + 3] = 255;
      }
    }

    targetContext.imageSmoothingEnabled = false;
    targetContext.putImageData(imageData, 0, 0);
  };
  image.src = terrainMap.asset_path;
}

/** @brief Convert one terrain pixel into a patterned display color. */
function patternedTerrainColor(
  red: number,
  green: number,
  blue: number,
  x: number,
  y: number
): [number, number, number] {
  if (matchesColor(red, green, blue, terrainColors.normal)) {
    return terrainColors.normal;
  }
  if (matchesColor(red, green, blue, terrainColors.boundary)) {
    return terrainColors.boundary;
  }
  if (
    matchesColor(red, green, blue, terrainColors.densityZeroDark) ||
    matchesColor(red, green, blue, terrainColors.densityZeroLight)
  ) {
    return (x + y) % 8 < 3 ? terrainColors.densityZeroDark : terrainColors.light;
  }
  if (matchesColor(red, green, blue, terrainColors.restricted)) {
    return (x + y) % 10 < 3 ? terrainColors.restricted : terrainColors.light;
  }
  if (matchesColor(red, green, blue, terrainColors.gate)) {
    return y % 8 < 3 ? terrainColors.gate : terrainColors.light;
  }
  if (matchesColor(red, green, blue, terrainColors.exit)) {
    return x % 8 < 3 ? terrainColors.exit : terrainColors.light;
  }
  if (matchesColor(red, green, blue, terrainColors.typeOne)) {
    return positiveModulo(x - y, 10) < 3 ? terrainColors.typeOne : terrainColors.light;
  }
  if (matchesColor(red, green, blue, terrainColors.typeTwo)) {
    return (x + y) % 12 < 4 ? terrainColors.typeTwo : terrainColors.light;
  }
  return [red, green, blue];
}

function matchesColor(
  red: number,
  green: number,
  blue: number,
  color: [number, number, number]
) {
  return red === color[0] && green === color[1] && blue === color[2];
}

function positiveModulo(value: number, divisor: number) {
  return ((value % divisor) + divisor) % divisor;
}

export function LatticeView({ width, height, agents, restrictedCells, terrainMap }: Props) {
  const terrainCanvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    if (!terrainMap || !terrainCanvasRef.current) {
      return;
    }
    drawTerrainCanvas(terrainCanvasRef.current, terrainMap);
  }, [terrainMap]);

  if (terrainMap) {
    return (
      <div
        className="terrainViewport"
        style={{ aspectRatio: `${width} / ${height}` }}
        aria-label="Terrain map simulation"
      >
        <canvas
          ref={terrainCanvasRef}
          className="terrainCanvas"
          aria-label="Patterned terrain map"
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
