package modelclient

import (
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestSnapshot(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/snapshot" {
			t.Fatalf("unexpected path %s", r.URL.Path)
		}
		_ = json.NewEncoder(w).Encode(map[string]any{
			"simulation": map[string]any{
				"tick": 1, "status": "running", "width": 5, "height": 4, "agent_count": 1, "seed": 2, "updated_at": "now",
			},
			"terrain": map[string]any{"restricted_cells": []any{}, "note": ""},
			"agents": []any{
				map[string]any{
					"id": "agent-001", "role": "civilian", "status": "moving",
					"position": map[string]any{"x": 1, "y": 2},
					"heading":  map[string]any{"dx": 1, "dy": 0},
				},
			},
		})
	}))
	defer server.Close()

	client := New(server.URL)
	snapshot, err := client.Snapshot(context.Background())
	if err != nil {
		t.Fatal(err)
	}
	if snapshot.Simulation.Tick != 1 {
		t.Fatalf("expected tick 1, got %d", snapshot.Simulation.Tick)
	}
	if len(snapshot.Agents) != 1 {
		t.Fatalf("expected 1 agent, got %d", len(snapshot.Agents))
	}
}
