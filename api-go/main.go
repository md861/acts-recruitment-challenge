package main

import (
	"context"
	"encoding/json"
	"log"
	"net/http"
	"os"
	"time"

	"acts-recruitment-challenge/api-go/internal/contracts"
	"acts-recruitment-challenge/api-go/internal/modelclient"
)

type server struct {
	model *modelclient.Client
}

func main() {
	modelBaseURL := env("MODEL_BASE_URL", "http://127.0.0.1:8001")
	addr := env("API_ADDR", "127.0.0.1:18080")

	s := &server{model: modelclient.New(modelBaseURL)}
	mux := http.NewServeMux()
	mux.HandleFunc("/api/health", s.withCORS(s.health))
	mux.HandleFunc("/api/snapshot", s.withCORS(s.snapshot))
	mux.HandleFunc("/api/step", s.withCORS(s.step))
	mux.HandleFunc("/api/reset", s.withCORS(s.reset))

	log.Printf("[api] listening on http://%s", addr)
	log.Fatal(http.ListenAndServe(addr, mux))
}

func (s *server) health(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		writeJSON(w, http.StatusMethodNotAllowed, contracts.APIError{Error: "method not allowed"})
		return
	}
	ctx, cancel := context.WithTimeout(r.Context(), 2*time.Second)
	defer cancel()
	if err := s.model.Health(ctx); err != nil {
		writeJSON(w, http.StatusServiceUnavailable, contracts.Health{Status: "degraded", Model: err.Error()})
		return
	}
	writeJSON(w, http.StatusOK, contracts.Health{Status: "ok", Model: "ok"})
}

func (s *server) snapshot(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		writeJSON(w, http.StatusMethodNotAllowed, contracts.APIError{Error: "method not allowed"})
		return
	}
	s.writeSnapshot(w, r, s.model.Snapshot)
}

func (s *server) step(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		writeJSON(w, http.StatusMethodNotAllowed, contracts.APIError{Error: "method not allowed"})
		return
	}
	s.writeSnapshot(w, r, s.model.Step)
}

func (s *server) reset(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		writeJSON(w, http.StatusMethodNotAllowed, contracts.APIError{Error: "method not allowed"})
		return
	}
	s.writeSnapshot(w, r, s.model.Reset)
}

func (s *server) writeSnapshot(
	w http.ResponseWriter,
	r *http.Request,
	fetch func(context.Context) (contracts.ModelSnapshot, error),
) {
	ctx, cancel := context.WithTimeout(r.Context(), 2*time.Second)
	defer cancel()

	modelSnapshot, err := fetch(ctx)
	if err != nil {
		writeJSON(w, http.StatusBadGateway, contracts.APIError{Error: err.Error()})
		return
	}

	warnings := validateSnapshot(modelSnapshot)
	writeJSON(w, http.StatusOK, contracts.APISnapshot{
		Source:     "python-population-model",
		ReceivedAt: time.Now().UTC().Format(time.RFC3339Nano),
		Simulation: modelSnapshot.Simulation,
		Terrain:    modelSnapshot.Terrain,
		Agents:     modelSnapshot.Agents,
		Warnings:   warnings,
	})
}

func validateSnapshot(snapshot contracts.ModelSnapshot) []string {
	warnings := make([]string, 0)
	if snapshot.Simulation.Width <= 0 || snapshot.Simulation.Height <= 0 {
		warnings = append(warnings, "simulation dimensions are invalid")
	}
	if snapshot.Simulation.AgentCount != len(snapshot.Agents) {
		warnings = append(warnings, "agent_count does not match number of agents")
	}
	for _, agent := range snapshot.Agents {
		if agent.Position.X < 0 || agent.Position.X >= snapshot.Simulation.Width ||
			agent.Position.Y < 0 || agent.Position.Y >= snapshot.Simulation.Height {
			warnings = append(warnings, "one or more agents are outside the lattice")
			break
		}
	}
	return warnings
}

func (s *server) withCORS(next http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type")
		if r.Method == http.MethodOptions {
			w.WriteHeader(http.StatusNoContent)
			return
		}
		next(w, r)
	}
}

func writeJSON(w http.ResponseWriter, status int, payload any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	if err := json.NewEncoder(w).Encode(payload); err != nil {
		log.Printf("[api] failed to write response: %v", err)
	}
}

func env(name string, fallback string) string {
	value := os.Getenv(name)
	if value == "" {
		return fallback
	}
	return value
}
