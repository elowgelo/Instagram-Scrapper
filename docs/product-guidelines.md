# Product Guidelines

## Design & UI Aesthetics
- **Theme**: Modern Dark Mode with vibrant accents (Instagram gradients `#405DE6` to `#E1306C`, Glassmorphism elements, sleek cards).
- **Typography**: Clean sans-serif modern typography (Inter / Outfit).
- **Layout**: Dynamic Responsive Dashboard with sidebar navigation, search & keyword filter bar, and grid/table view toggles.
- **Micro-interactions**: Subtle hover animations, progress spinners during scraping, and highlighted keyword tags.

## User Experience (UX) Principles
- **Clarity & Feedback**: Clear progress bars/status badges for scraping operations (Idle, Scraping, Filtering, Completed, Error).
- **Graceful Error Handling**: Informative messages for rate limits, private accounts, or network issues.
- **Instant Filtering**: Real-time text filter and keyword search response.

## Operational & Code Standards
- **Modularity**: Decouple backend scraping logic from frontend UI.
- **Performance**: Asynchronous parsing and non-blocking background fetching.
- **Rate Limit Protection**: Built-in delay controls and user-agent rotation options to protect scraping activity.
