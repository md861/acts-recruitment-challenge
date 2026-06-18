/** @file simulation.ts
 *  @brief Frontend API types and helpers for model snapshots.
 */

export type Position = {
  x: number;
  y: number;
};

export type Heading = {
  dx: number;
  dy: number;
};

export type Agent = {
  id: string;
  role: "civilian" | "staff" | "patrol" | string;
  status: string;
  position: Position;
  heading: Heading;
  behaviour_profile?: string;
};

export type TerrainMap = {
  source: string;
  asset_path: string;
  legend: Record<string, { r: number; g: number; b: number }>;
  summary: {
    width: number;
    height: number;
    counts_by_type: Record<string, number>;
  };
};

export type SimulationMetrics = {
  breach_detected?: number;
  breach_handled?: number;
  blocked_boundary_attempts?: number;
  gate_congestion_events?: number;
  exit_events?: number;
  penalty_cell_traversals?: number;
  unresolved_breaches?: number;
  congestion_count?: number;
  congested_cells?: Array<{ x: number; y: number; count: number }>;
  cell_density?: Array<{ x: number; y: number; count: number }>;
  cumulative_cell_visits?: Array<{ x: number; y: number; count: number }>;
  time_spent_by_agent_id?: Record<string, Record<string, number>>;
  time_spent_by_role?: Record<string, Record<string, number>>;
};

export type Snapshot = {
  source: string;
  received_at: string;
  simulation: {
    tick: number;
    status: string;
    width: number;
    height: number;
    agent_count: number;
    seed: number;
    updated_at: string;
    metrics?: SimulationMetrics;
  };
  terrain: {
    restricted_cells: Position[];
    note: string;
    map?: TerrainMap;
  };
  agents: Agent[];
  warnings: string[];
};

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, init);
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `Request failed with ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export function getSnapshot(): Promise<Snapshot> {
  return request<Snapshot>("/api/snapshot");
}

export function resetSimulation(): Promise<Snapshot> {
  return request<Snapshot>("/api/reset", { method: "POST" });
}

export function stepSimulation(): Promise<Snapshot> {
  return request<Snapshot>("/api/step", { method: "POST" });
}
