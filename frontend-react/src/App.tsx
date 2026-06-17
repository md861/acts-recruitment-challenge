import { useEffect, useState } from "react";

import { getSnapshot, resetSimulation, stepSimulation, type Snapshot } from "./api/simulation";
import { ControlPanel } from "./components/ControlPanel";
import { LatticeView } from "./components/LatticeView";

export function App() {
  const [snapshot, setSnapshot] = useState<Snapshot | null>(null);
  const [isPolling, setIsPolling] = useState(true);
  const [error, setError] = useState<string | null>(null);

  async function refresh() {
    try {
      const next = await getSnapshot();
      setSnapshot(next);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to fetch snapshot");
    }
  }

  useEffect(() => {
    void refresh();
  }, []);

  useEffect(() => {
    if (!isPolling) {
      return;
    }
    const handle = window.setInterval(() => {
      void refresh();
    }, 1000);
    return () => window.clearInterval(handle);
  }, [isPolling]);

  async function step() {
    try {
      setSnapshot(await stepSimulation());
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to step simulation");
    }
  }

  async function reset() {
    try {
      setSnapshot(await resetSimulation());
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to reset simulation");
    }
  }

  return (
    <main className="appShell">
      <section className="workspace">
        <header className="topBar">
          <div>
            <h1>ACTS Mini Simulation</h1>
            <p>Population ABM baseline for a collective training tool.</p>
          </div>
          <span className={isPolling ? "statusLive" : "statusPaused"}>
            {isPolling ? "Live" : "Paused"}
          </span>
        </header>
        {snapshot ? (
          <LatticeView
            width={snapshot.simulation.width}
            height={snapshot.simulation.height}
            agents={snapshot.agents}
            restrictedCells={snapshot.terrain.restricted_cells}
          />
        ) : (
          <div className="loadingState">Loading simulation...</div>
        )}
      </section>
      <ControlPanel
        tick={snapshot?.simulation.tick ?? 0}
        agentCount={snapshot?.agents.length ?? 0}
        isPolling={isPolling}
        error={error}
        warnings={snapshot?.warnings ?? []}
        onTogglePolling={() => setIsPolling((value) => !value)}
        onStep={() => void step()}
        onReset={() => void reset()}
      />
    </main>
  );
}

