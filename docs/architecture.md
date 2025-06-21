# SMET App Architecture

This document outlines a high level plan for a cross platform application that generates cost estimates for stretch ceilings. The same codebase should support mobile (Android/iOS) and desktop web users.

## Core Features

- **Nomenclature and materials**: A database of stretch-ceiling materials, profiles, and related components.
- **Orders**: Ability to create and track orders with item quantities and pricing.
- **Clients**: Maintain client records with contact information.
- **Estimate calculation**: Compute and display SMET for each order.
- **amoCRM sync**: Automatically synchronize clients and orders with amoCRM via its API.

## Technology Stack

1. **Frontend**
   - Use a single codebase built with React for the web interface.
   - For mobile apps, use React Native or a Progressive Web App approach so that most logic is shared.
2. **Backend**
   - Node.js with Express for REST API endpoints.
   - Store data in a SQL or NoSQL database (e.g., PostgreSQL or MongoDB).
3. **amoCRM Integration**
   - Use amoCRM API OAuth credentials to create/update leads and contacts.
   - Store amoCRM tokens securely on the backend.
4. **Deployment**
   - Host backend using a cloud provider (e.g., AWS, DigitalOcean) or a server you control.
   - The web client can be served as static files from the backend or a CDN.

## Synchronization Flow

1. User creates or updates an order or client in the SMET app.
2. Backend sends the relevant data to amoCRM via REST API.
3. amoCRM responds with lead/contact IDs, which are saved in the local database for future updates.
4. Any changes on amoCRM can be pulled periodically (e.g., via webhooks or scheduled tasks).

## Next Steps

1. Prototype a simple React-based interface with forms for materials and orders.
2. Implement a minimal Node.js backend with endpoints for orders and clients.
3. Integrate amoCRM authentication and basic data push from the backend.
4. Design a simple database schema to store materials, orders, and clients.

