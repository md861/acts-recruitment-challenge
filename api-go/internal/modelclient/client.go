package modelclient

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"strings"
	"time"

	"acts-recruitment-challenge/api-go/internal/contracts"
)

type Client struct {
	baseURL    string
	httpClient *http.Client
}

func New(baseURL string) *Client {
	return &Client{
		baseURL: strings.TrimRight(baseURL, "/"),
		httpClient: &http.Client{
			Timeout: 2 * time.Second,
		},
	}
}

func (c *Client) Health(ctx context.Context) error {
	req, err := http.NewRequestWithContext(ctx, http.MethodGet, c.baseURL+"/health", nil)
	if err != nil {
		return err
	}
	resp, err := c.httpClient.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()
	if resp.StatusCode >= 300 {
		return fmt.Errorf("model health returned status %d", resp.StatusCode)
	}
	return nil
}

func (c *Client) Snapshot(ctx context.Context) (contracts.ModelSnapshot, error) {
	return c.getSnapshot(ctx, http.MethodGet, "/snapshot")
}

func (c *Client) Step(ctx context.Context) (contracts.ModelSnapshot, error) {
	return c.getSnapshot(ctx, http.MethodPost, "/step")
}

func (c *Client) Reset(ctx context.Context) (contracts.ModelSnapshot, error) {
	return c.getSnapshot(ctx, http.MethodPost, "/reset")
}

func (c *Client) getSnapshot(ctx context.Context, method string, path string) (contracts.ModelSnapshot, error) {
	var snapshot contracts.ModelSnapshot
	req, err := http.NewRequestWithContext(ctx, method, c.baseURL+path, bytes.NewReader(nil))
	if err != nil {
		return snapshot, err
	}
	resp, err := c.httpClient.Do(req)
	if err != nil {
		return snapshot, err
	}
	defer resp.Body.Close()
	if resp.StatusCode >= 300 {
		return snapshot, fmt.Errorf("model returned status %d", resp.StatusCode)
	}
	if err := json.NewDecoder(resp.Body).Decode(&snapshot); err != nil {
		return snapshot, err
	}
	return snapshot, nil
}
