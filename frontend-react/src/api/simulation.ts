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
  };
  terrain: {
    restricted_cells: Position[];
    note: string;
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
