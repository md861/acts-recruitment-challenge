type Props = {
  tick: number;
  agentCount: number;
  isPolling: boolean;
  error: string | null;
  warnings: string[];
  onTogglePolling: () => void;
  onStep: () => void;
  onReset: () => void;
};

export function ControlPanel({
  tick,
  agentCount,
  isPolling,
  error,
  warnings,
  onTogglePolling,
  onStep,
  onReset
}: Props) {
  return (
    <aside className="panel">
      <div className="metric">
        <span>Tick</span>
        <strong>{tick}</strong>
      </div>
      <div className="metric">
        <span>Agents</span>
        <strong>{agentCount}</strong>
      </div>
      <div className="buttonRow">
        <button type="button" onClick={onTogglePolling}>
          {isPolling ? "Pause" : "Resume"}
        </button>
        <button type="button" onClick={onStep}>
          Step
        </button>
        <button type="button" onClick={onReset}>
          Reset
        </button>
      </div>
      {error ? <p className="errorText">{error}</p> : null}
      {warnings.length > 0 ? (
        <div className="warnings">
          {warnings.map((warning) => (
            <p key={warning}>{warning}</p>
          ))}
        </div>
      ) : null}
      <div className="legend">
        <span><i className="swatch civilian" />Civilian</span>
        <span><i className="swatch staff" />Staff</span>
        <span><i className="swatch patrol" />Patrol</span>
        <span><i className="swatch restricted" />Restricted</span>
      </div>
    </aside>
  );
}

