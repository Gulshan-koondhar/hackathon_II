# Contract: TaskAnalyticsAgent

Logic for calculating statistics.

## Skills

### `get_summary() -> Response`
- **Logic**: Calculate total, completed, and pending counts.
- **Success**: Returns counts.
- **Data**: `{"total": int, "completed": int, "pending": int, "percentage": float}`
