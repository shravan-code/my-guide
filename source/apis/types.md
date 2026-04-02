# 🌐 All Types of APIs — Deep Dive Guide

> A comprehensive, developer-focused reference covering every major API type with architecture diagrams, real-world examples, code samples, and use-case guidance.

---

## 📌 Table of Contents

1. [What is an API?](#1-what-is-an-api)
2. [REST API](#2-rest-api)
3. [GraphQL API](#3-graphql-api)
4. [SOAP API](#4-soap-api)
5. [gRPC API](#5-grpc-api)
6. [WebSocket API](#6-websocket-api)
7. [Webhooks](#7-webhooks)
8. [SSE — Server-Sent Events](#8-sse--server-sent-events)
9. [RPC — Remote Procedure Call](#9-rpc--remote-procedure-call)
10. [JSON-RPC](#10-json-rpc)
11. [XML-RPC](#11-xml-rpc)
12. [API Gateway](#12-api-gateway)
13. [Open API / Swagger](#13-openapi--swagger)
14. [Comparison Summary Table](#14-comparison-summary-table)
15. [How to Choose the Right API](#15-how-to-choose-the-right-api)

---

## 1. What is an API?

An **API (Application Programming Interface)** is a contract between two software systems defining how they communicate. It abstracts internal implementation details and exposes only what is needed.

```
┌──────────────────────────────────────────────────────────┐
│                                                          │
│   CLIENT          API LAYER             SERVER           │
│                                                          │
│  ┌───────┐   Request    ┌─────────┐   ┌──────────────┐  │
│  │ App / │ ──────────►  │  API    │──►│  Business    │  │
│  │Browser│             │Endpoint │   │  Logic +     │  │
│  │Mobile │ ◄──────────  │         │◄──│  Database    │  │
│  └───────┘   Response  └─────────┘   └──────────────┘  │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

**Why APIs matter:**
- Enable systems written in different languages to communicate
- Abstract and protect internal business logic
- Allow third-party integrations and developer ecosystems
- Enable microservices to communicate cleanly
- Power mobile apps, SPAs, IoT devices, and AI integrations

---

## 2. REST API

### What is REST?

**REST (Representational State Transfer)** is an architectural style for distributed hypermedia systems, defined by Roy Fielding in his 2000 doctoral dissertation. It uses standard **HTTP methods** and treats every resource as a uniquely addressable URL.

![REST API Architecture](https://restfulapi.net/wp-content/uploads/REST-API-Architecture.jpg)
*REST API: client sends HTTP request to a resource endpoint, server returns a representation of the resource*

---

### Core Constraints of REST

| Constraint | Description |
|---|---|
| **Stateless** | Each request must contain all the info needed; the server stores no session |
| **Client-Server** | UI and data storage are decoupled |
| **Cacheable** | Responses must define themselves as cacheable or non-cacheable |
| **Uniform Interface** | Consistent resource-based URLs and HTTP verbs |
| **Layered System** | Client cannot tell if it's connected directly or through a proxy |
| **Code on Demand** *(optional)* | Server can send executable code (e.g., JavaScript) |

---

### HTTP Methods in REST

| Method | CRUD | Idempotent | Safe | Example |
|--------|------|------------|------|---------|
| `GET` | Read | ✅ Yes | ✅ Yes | `GET /users/42` |
| `POST` | Create | ❌ No | ❌ No | `POST /users` |
| `PUT` | Replace | ✅ Yes | ❌ No | `PUT /users/42` |
| `PATCH` | Update | ❌ No | ❌ No | `PATCH /users/42` |
| `DELETE` | Delete | ✅ Yes | ❌ No | `DELETE /users/42` |

---

### REST Resource URL Design

```
Good REST URL structure:
GET    /users              → List all users
POST   /users              → Create a new user
GET    /users/{id}         → Get user by ID
PUT    /users/{id}         → Replace user
PATCH  /users/{id}         → Update user fields
DELETE /users/{id}         → Delete user

GET    /users/{id}/posts   → Get all posts by user
POST   /users/{id}/posts   → Create post for user
```

---

### REST Request & Response Example

**Request:**
```http
GET /api/v1/users/42 HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOiJSUzI1NiJ9...
Accept: application/json
```

**Response:**
```json
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": 42,
  "name": "Alice Johnson",
  "email": "alice@example.com",
  "role": "admin",
  "createdAt": "2023-06-15T10:30:00Z",
  "_links": {
    "self": { "href": "/api/v1/users/42" },
    "posts": { "href": "/api/v1/users/42/posts" }
  }
}
```

---

### HTTP Status Codes

| Range | Meaning | Examples |
|-------|---------|---------|
| `2xx` | Success | 200 OK, 201 Created, 204 No Content |
| `3xx` | Redirection | 301 Moved Permanently, 304 Not Modified |
| `4xx` | Client Error | 400 Bad Request, 401 Unauthorized, 404 Not Found |
| `5xx` | Server Error | 500 Internal Server Error, 503 Service Unavailable |

---

### REST — Pros & Cons

| ✅ Pros | ❌ Cons |
|--------|--------|
| Simple, widely understood | Over-fetching (too much data returned) |
| Great HTTP caching support | Under-fetching (multiple roundtrips needed) |
| Stateless = horizontally scalable | API versioning complexity (v1, v2, v3...) |
| Huge ecosystem of tools | No real-time / push support |
| Language and platform agnostic | No strict contract by default |
| Human-readable JSON | Inconsistent implementations between teams |

---

### When to Use REST
- Public APIs consumed by third parties
- Mobile and browser frontends
- CRUD-heavy applications
- When simplicity and broad adoption matter

---

## 3. GraphQL API

### What is GraphQL?

**GraphQL** is a query language for APIs and a runtime for executing those queries, developed by **Facebook (Meta)** in 2012 and open-sourced in 2015. Unlike REST's fixed endpoints, GraphQL exposes a **single endpoint** where clients specify exactly the data they need.

![GraphQL vs REST data fetching](https://www.apollographql.com/blog/static/1_qpyJSVVPkd5c6ItMmivnYg.png)
*REST requires multiple requests; GraphQL fetches all nested data in one single query*

---

### GraphQL Core Concepts

| Concept | Description |
|---------|-------------|
| **Schema** | Strongly-typed definition of all data and operations |
| **Query** | Read operation — fetch data |
| **Mutation** | Write operation — create, update, delete |
| **Subscription** | Real-time operation — subscribe to events |
| **Resolver** | Function that fetches data for each field |
| **Type System** | Every field has a defined type (String, Int, Boolean, etc.) |

---

### GraphQL Schema Definition

```graphql
type User {
  id: ID!
  name: String!
  email: String!
  role: Role!
  posts: [Post!]!
  createdAt: String!
}

type Post {
  id: ID!
  title: String!
  body: String!
  author: User!
  tags: [String!]!
}

enum Role {
  ADMIN
  USER
  VIEWER
}

type Query {
  user(id: ID!): User
  users: [User!]!
  post(id: ID!): Post
}

type Mutation {
  createUser(name: String!, email: String!): User!
  updateUser(id: ID!, name: String): User!
  deleteUser(id: ID!): Boolean!
}

type Subscription {
  newPost: Post!
}
```

---

### GraphQL Query Examples

**Query — Fetch only needed fields:**
```graphql
query GetUserWithPosts {
  user(id: "42") {
    name
    email
    posts {
      title
      tags
    }
  }
}
```

**Response — Exact shape requested, nothing more:**
```json
{
  "data": {
    "user": {
      "name": "Alice Johnson",
      "email": "alice@example.com",
      "posts": [
        { "title": "Intro to GraphQL", "tags": ["api", "graphql"] },
        { "title": "REST vs GraphQL", "tags": ["api", "comparison"] }
      ]
    }
  }
}
```

**Mutation — Create data:**
```graphql
mutation CreateUser {
  createUser(name: "Bob Smith", email: "bob@example.com") {
    id
    name
  }
}
```

**Subscription — Real-time updates:**
```graphql
subscription OnNewPost {
  newPost {
    id
    title
    author {
      name
    }
  }
}
```

---

### GraphQL — Pros & Cons

| ✅ Pros | ❌ Cons |
|--------|--------|
| Fetch exactly the data you need | Steeper learning curve vs REST |
| Single endpoint for all operations | Complex queries can cause N+1 problem |
| Strongly typed — self-documenting | HTTP caching is harder |
| No versioning — evolve the schema | Overkill for simple CRUD apps |
| Reduces number of API requests | Query complexity can strain server |
| Excellent tooling (GraphiQL, Apollo) | File uploads require workarounds |

---

### When to Use GraphQL
- Complex data with deep relationships (social networks, CMS, e-commerce)
- Multiple client types (mobile + web) with different data needs
- Rapid frontend iteration where data requirements change frequently
- When minimizing over-fetching is critical (bandwidth-constrained clients)

---

## 4. SOAP API

### What is SOAP?

**SOAP (Simple Object Access Protocol)** is a **messaging protocol** using **XML** for message format and HTTP, SMTP, or TCP for transport. Unlike REST (an architectural style), SOAP is a formal protocol with a strict specification governed by the W3C.

![SOAP API Architecture](https://www.tutorialspoint.com/soap/images/soap-architecture.jpg)
*SOAP uses XML envelopes with Header and Body sections, transported over HTTP or other protocols*

---

### SOAP Message Structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope
  xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
  xmlns:xsi="http://www.w3.org/1999/XMLSchema-instance">

  <!-- Optional: Authentication, transaction info -->
  <soap:Header>
    <AuthToken>Bearer abc123token</AuthToken>
    <RequestId>REQ-20240115-001</RequestId>
  </soap:Header>

  <!-- Required: The actual request -->
  <soap:Body>
    <GetAccountBalance xmlns="http://bank.example.com/services">
      <AccountNumber>1234567890</AccountNumber>
      <Currency>USD</Currency>
    </GetAccountBalance>
  </soap:Body>

</soap:Envelope>
```

**SOAP Response:**
```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetAccountBalanceResponse>
      <Balance>15432.50</Balance>
      <Currency>USD</Currency>
      <LastUpdated>2024-01-15T09:00:00Z</LastUpdated>
    </GetAccountBalanceResponse>
  </soap:Body>
</soap:Envelope>
```

---

### WSDL — The SOAP Contract

**WSDL (Web Services Description Language)** is an XML document that formally defines the SOAP service — its operations, input/output types, and endpoint location.

```xml
<definitions name="AccountService"
  targetNamespace="http://bank.example.com/services">

  <!-- Data type definitions -->
  <types>
    <schema>
      <element name="AccountNumber" type="string"/>
      <element name="Balance" type="decimal"/>
    </schema>
  </types>

  <!-- Message formats -->
  <message name="GetBalanceRequest">
    <part name="AccountNumber" type="xsd:string"/>
  </message>

  <!-- Available operations -->
  <portType name="AccountPortType">
    <operation name="GetAccountBalance">
      <input message="GetBalanceRequest"/>
      <output message="GetBalanceResponse"/>
    </operation>
  </portType>

</definitions>
```

---

### SOAP Security Standards (WS-Security)

SOAP has built-in enterprise security standards:

| Standard | Purpose |
|---------|---------|
| **WS-Security** | Message-level encryption and signing |
| **WS-Trust** | Token-based authentication (SAML, X.509) |
| **WS-ReliableMessaging** | Guaranteed message delivery |
| **WS-AtomicTransaction** | Distributed ACID transactions |
| **WS-Policy** | Define service requirements and capabilities |

---

### SOAP — Pros & Cons

| ✅ Pros | ❌ Cons |
|--------|--------|
| Formal contract via WSDL | Extremely verbose XML overhead |
| Built-in security (WS-Security) | Slow compared to REST/gRPC |
| ACID transaction support | Complex to implement and debug |
| Strict error handling (SOAP Faults) | Large message size |
| Works over HTTP, SMTP, TCP | Poor readability for humans |
| Language independent | Overkill for modern web/mobile apps |

---

### When to Use SOAP
- Banking, financial services, and payment processing
- Healthcare systems (HL7, FHIR integrations)
- Government and enterprise legacy systems
- When ACID transactions across services are required
- When strict message contracts and formal compliance matter

---

## 5. gRPC API

### What is gRPC?

**gRPC (Google Remote Procedure Call)** is a high-performance, open-source RPC framework developed by **Google**. It uses **HTTP/2** for transport and **Protocol Buffers (protobuf)** for serialization — making it significantly faster than REST/JSON.

![gRPC Architecture](https://grpc.io/img/landing-2.svg)
*gRPC uses generated stubs on both client and server sides to communicate via binary Protocol Buffers*

---

### How gRPC Works

```
┌──────────────────┐                    ┌──────────────────┐
│                  │   Protobuf Binary  │                  │
│   gRPC CLIENT    │ ─────────────────► │   gRPC SERVER    │
│                  │   (HTTP/2 stream)  │                  │
│  Generated Stub  │ ◄───────────────── │  Service Impl    │
│  user.proto      │                    │  user.proto      │
└──────────────────┘                    └──────────────────┘
        │                                        │
        └────── Both sides share .proto ─────────┘
                 (the contract)
```

---

### Protocol Buffer Definition (.proto)

```protobuf
syntax = "proto3";

package user;

// Service definition
service UserService {
  // Unary RPC
  rpc GetUser (GetUserRequest) returns (User);

  // Server-streaming RPC
  rpc ListUsers (ListUsersRequest) returns (stream User);

  // Client-streaming RPC
  rpc CreateUsers (stream CreateUserRequest) returns (CreateUsersResponse);

  // Bidirectional streaming RPC
  rpc ChatWithUser (stream ChatMessage) returns (stream ChatMessage);
}

// Messages
message GetUserRequest {
  int32 id = 1;
}

message User {
  int32 id = 1;
  string name = 2;
  string email = 3;
  Role role = 4;
  int64 created_at = 5;
}

enum Role {
  USER = 0;
  ADMIN = 1;
}

message ListUsersRequest {
  int32 page = 1;
  int32 page_size = 2;
}

message CreateUserRequest {
  string name = 1;
  string email = 2;
}
```

---

### gRPC Streaming Types

| Type | Description | Use Case |
|------|-------------|---------|
| **Unary** | One request → One response | Standard function call |
| **Server Streaming** | One request → Many responses | File download, live feed |
| **Client Streaming** | Many requests → One response | File upload, batch insert |
| **Bidirectional Streaming** | Many requests ↔ Many responses | Chat, real-time collaboration |

---

### gRPC vs REST Performance

```
Payload size comparison (same data):
REST/JSON:   {"id":1,"name":"Alice","email":"alice@example.com"}  = ~50 bytes
gRPC/protobuf: [binary]                                           = ~10 bytes

Speed (internal benchmark, same hardware):
REST:  ~15,000 requests/second
gRPC:  ~80,000 requests/second   (~5x faster)
```

---

### gRPC — Pros & Cons

| ✅ Pros | ❌ Cons |
|--------|--------|
| Extremely fast (binary protobuf) | Not human-readable |
| HTTP/2 multiplexing | Limited browser support (requires grpc-web) |
| 4 streaming patterns | Requires tooling setup (proto compiler) |
| Strongly typed contracts | Smaller community vs REST |
| Auto-generates client/server code | Debugging is harder |
| Supports 10+ programming languages | Overkill for external public APIs |

---

### When to Use gRPC
- Internal microservices communication
- High-throughput, low-latency systems
- Streaming large volumes of data
- Polyglot environments (services in Go, Python, Java, etc.)
- Mobile apps where bandwidth efficiency matters

---

## 6. WebSocket API

### What is WebSocket?

**WebSocket** is a communication protocol providing **full-duplex (bidirectional), persistent connections** over a single TCP connection. After an initial HTTP handshake, the connection is upgraded — allowing the server to **push data to the client at any time**.

![WebSocket vs HTTP](https://assets.website-files.com/5ff66329429d880392f6cba2/63fe388d5ce5fb3a1b3bbfda_Websocket%20Long%20polling.png)
*HTTP requires repeated polling; WebSocket maintains a single open connection for instant two-way communication*

---

### WebSocket Handshake

```http
-- Client HTTP Upgrade Request --
GET /chat HTTP/1.1
Host: ws.example.com
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Sec-WebSocket-Version: 13

-- Server Upgrade Response --
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=

-- Connection is now open! --
Both sides can now send frames at any time.
```

---

### WebSocket JavaScript Client

```javascript
// Connect to WebSocket server
const socket = new WebSocket('wss://chat.example.com/ws');

// Connection opened
socket.addEventListener('open', (event) => {
  console.log('Connected to WebSocket server');
  socket.send(JSON.stringify({
    type: 'join',
    room: 'general',
    user: 'alice'
  }));
});

// Receive messages from server
socket.addEventListener('message', (event) => {
  const data = JSON.parse(event.data);
  console.log('Message received:', data);

  if (data.type === 'chat') {
    displayMessage(data.user, data.text);
  }
});

// Send a message
function sendMessage(text) {
  socket.send(JSON.stringify({
    type: 'chat',
    text: text,
    timestamp: Date.now()
  }));
}

// Handle disconnection
socket.addEventListener('close', (event) => {
  console.log('Disconnected. Code:', event.code);
});

// Handle errors
socket.addEventListener('error', (error) => {
  console.error('WebSocket error:', error);
});
```

---

### WebSocket vs HTTP Polling Comparison

| Feature | HTTP Short Polling | HTTP Long Polling | WebSocket |
|---------|-------------------|------------------|-----------|
| Connection | New per request | Held open | Persistent |
| Latency | High | Medium | Very Low |
| Server Push | ❌ | ❌ (sort of) | ✅ |
| Overhead | High | Medium | Minimal |
| Complexity | Low | Medium | Medium |
| Scalability | Poor | Fair | Good |

---

### WebSocket — Pros & Cons

| ✅ Pros | ❌ Cons |
|--------|--------|
| True real-time bidirectional communication | Persistent connections consume server resources |
| Very low latency | Harder to scale horizontally (sticky sessions) |
| Eliminates repeated HTTP handshake overhead | Not cacheable by HTTP caches |
| Full-duplex — both sides send simultaneously | Firewalls/proxies sometimes block WS |
| Efficient for high-frequency data | More complex than REST |

---

### When to Use WebSocket
- Live chat and messaging (Slack, Discord, WhatsApp Web)
- Multiplayer online games
- Real-time collaborative tools (Google Docs, Figma)
- Live financial data (stock tickers, crypto prices)
- Sports scores and live dashboards
- IoT device command and control

---

## 7. Webhooks

### What is a Webhook?

A **Webhook** is a user-defined HTTP callback — a **reverse API**. Instead of a client polling the server for updates, the **server sends an HTTP POST to the client's URL automatically** when a specified event occurs.

![Webhook flow diagram](https://hyscaler.com/wp-content/uploads/2023/08/Webhooks-Powering-Modern-Event-Driven-Architecture-2048x1462.webp)
*Webhooks push data automatically when events fire, eliminating the need for repeated polling*

---

### Webhook vs Polling

```
❌ Polling (Inefficient):
Client → "Any new payments?"  → Server: "No"
Client → "Any new payments?"  → Server: "No"
Client → "Any new payments?"  → Server: "No"
Client → "Any new payments?"  → Server: "Yes! Here's the data"
(Wasted 3 requests + delay)

✅ Webhook (Efficient):
Server → POST /your-webhook-url → Client
(Instantly, only when event fires)
```

---

### Webhook Payload Example (Stripe Payment)

```json
POST https://yourapp.com/webhooks/stripe
Content-Type: application/json
Stripe-Signature: t=1609459200,v1=abc123...

{
  "id": "evt_1234567890",
  "type": "payment_intent.succeeded",
  "created": 1609459200,
  "data": {
    "object": {
      "id": "pi_abc123",
      "amount": 4999,
      "currency": "usd",
      "status": "succeeded",
      "customer": "cus_xyz789",
      "metadata": {
        "order_id": "ORDER-2024-001"
      }
    }
  }
}
```

---

### Handling Webhooks Securely

```javascript
// Node.js / Express webhook handler
const express = require('express');
const crypto = require('crypto');
const app = express();

app.post('/webhooks/stripe', express.raw({ type: 'application/json' }), (req, res) => {

  // 1. Verify the webhook signature
  const sig = req.headers['stripe-signature'];
  const secret = process.env.STRIPE_WEBHOOK_SECRET;

  let event;
  try {
    event = stripe.webhooks.constructEvent(req.body, sig, secret);
  } catch (err) {
    console.error('Webhook signature verification failed:', err.message);
    return res.status(400).send(`Webhook Error: ${err.message}`);
  }

  // 2. Handle the event type
  switch (event.type) {
    case 'payment_intent.succeeded':
      const paymentIntent = event.data.object;
      fulfillOrder(paymentIntent.metadata.order_id);
      break;

    case 'customer.subscription.deleted':
      handleSubscriptionCancellation(event.data.object);
      break;

    default:
      console.log(`Unhandled event type: ${event.type}`);
  }

  // 3. Return 200 IMMEDIATELY (async processing)
  res.status(200).json({ received: true });
});
```

---

### Webhooks — Pros & Cons

| ✅ Pros | ❌ Cons |
|--------|--------|
| Event-driven — no wasteful polling | Requires a public HTTPS endpoint |
| Extremely efficient and scalable | No guaranteed delivery (retry logic needed) |
| Simple to integrate (just a URL) | Out-of-order delivery possible |
| Reduces server and network load | Security must be handled carefully |
| Works with any language/framework | Debugging and testing can be tricky |

---

### When to Use Webhooks
- Payment and subscription events (Stripe, PayPal)
- CI/CD triggers (GitHub pushes trigger builds)
- Form submission routing (Typeform → CRM)
- E-commerce order lifecycle notifications
- Third-party service event notifications

---

## 8. SSE — Server-Sent Events

### What is SSE?

**Server-Sent Events (SSE)** is a server push technology over a **standard HTTP connection**. The server streams a continuous sequence of events to the client over a long-lived HTTP connection. Unlike WebSocket, SSE is **one-directional** (server → client only).

![SSE vs Polling vs WebSocket](https://miro.medium.com/v2/resize:fit:1400/1*n2Zi1B2SQ6cHhH0Qb0PfpA.png)
*Comparison of short polling, long polling, SSE, and WebSocket connection patterns*

---

### SSE Server Implementation (Node.js)

```javascript
// Server: Express SSE endpoint
app.get('/events/live-feed', (req, res) => {
  // Set SSE headers
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.flushHeaders(); // Flush headers immediately

  let count = 0;

  const sendEvent = setInterval(() => {
    // SSE format: "data: <payload>\n\n"
    const data = JSON.stringify({
      timestamp: Date.now(),
      price: 42000 + Math.random() * 500,
      volume: Math.floor(Math.random() * 10000)
    });

    res.write(`id: ${count}\n`);
    res.write(`event: price-update\n`);
    res.write(`data: ${data}\n\n`); // Double newline ends the event
    count++;
  }, 1000);

  // Cleanup on client disconnect
  req.on('close', () => {
    clearInterval(sendEvent);
    console.log('Client disconnected');
  });
});
```

---

### SSE Client Implementation

```javascript
// Browser: EventSource API
const eventSource = new EventSource('/events/live-feed');

// Listen for specific event types
eventSource.addEventListener('price-update', (event) => {
  const data = JSON.parse(event.data);
  console.log(`Price: $${data.price.toFixed(2)}`);
  updatePriceDisplay(data);
});

// General message handler
eventSource.onmessage = (event) => {
  console.log('Message:', event.data);
};

// Handle errors (auto-reconnects by default!)
eventSource.onerror = (error) => {
  console.error('SSE Error:', error);
};

// Close when done
// eventSource.close();
```

---

### SSE vs WebSocket

| Feature | SSE | WebSocket |
|---------|-----|-----------|
| Direction | Server → Client only | Bidirectional |
| Protocol | Plain HTTP | WS upgrade |
| Auto-reconnect | ✅ Built-in | ❌ Must implement |
| Browser support | ✅ All modern | ✅ All modern |
| IE support | ❌ | ❌ |
| HTTP/2 support | ✅ | ❌ |
| Firewall/proxy friendly | ✅ | ⚠️ Sometimes blocked |
| Use case | News feeds, notifications | Chat, games |

---

### When to Use SSE
- Live news feeds and activity streams
- Real-time notifications (no user reply needed)
- Live dashboards — metrics, logs, analytics
- Progress updates for long-running operations
- Stock prices and sports scores display

---

## 9. RPC — Remote Procedure Call

### What is RPC?

**RPC (Remote Procedure Call)** is a protocol that allows a program to **execute a function on a remote server** as if it were a local call. The complexity of the network communication is hidden from the developer.

![RPC architecture](https://www.techtarget.com/rms/onlineimages/enterprise_ai-remote_procedure_call-f.png)
*RPC: the client stub serializes the call, network transports it, server stub deserializes and invokes the function*

---

### How RPC Works

```
Developer Code (Client):
  result = getUserById(42)        ← looks like a local function call

Behind the scenes:
  1. Client stub serializes:  { method: "getUserById", params: [42] }
  2. Sent over network to server
  3. Server stub deserializes and calls: getUserById(42)
  4. Return value serialized and sent back
  5. Client stub returns result to caller

Developer Code (Server):
  function getUserById(id) {       ← actual implementation
    return database.find(id);
  }
```

---

### RPC vs REST Philosophy

| REST | RPC |
|------|-----|
| Resource-oriented (`/users/42`) | Action-oriented (`getUser(42)`) |
| Nouns in URLs | Verbs in method names |
| HTTP verbs carry meaning | Method name carries meaning |
| Stateless by constraint | Stateless or stateful |
| `GET /orders/1/cancel` ← awkward | `cancelOrder(1)` ← natural |

---

### When to Use RPC
- When operations are action-oriented, not resource-oriented
- Internal service-to-service communication
- When you want remote calls to feel like local calls
- High-performance systems (use gRPC)

---

## 10. JSON-RPC

### What is JSON-RPC?

**JSON-RPC** is a lightweight, **stateless remote procedure call protocol** encoded in **JSON**. It allows calling methods on a remote server with a simple, minimal request/response format.

```json
-- JSON-RPC Request --
{
  "jsonrpc": "2.0",
  "method": "getUserById",
  "params": { "id": 42 },
  "id": 1
}

-- JSON-RPC Response --
{
  "jsonrpc": "2.0",
  "result": {
    "id": 42,
    "name": "Alice Johnson",
    "email": "alice@example.com"
  },
  "id": 1
}

-- JSON-RPC Error Response --
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32602,
    "message": "Invalid params",
    "data": "User id must be a positive integer"
  },
  "id": 1
}
```

---

### JSON-RPC Standard Error Codes

| Code | Meaning |
|------|---------|
| `-32700` | Parse error |
| `-32600` | Invalid Request |
| `-32601` | Method not found |
| `-32602` | Invalid params |
| `-32603` | Internal error |
| `-32000 to -32099` | Server-defined errors |

---

### When to Use JSON-RPC
- Blockchain and cryptocurrency APIs (Ethereum, Bitcoin nodes use JSON-RPC)
- Simple lightweight internal services
- When HTTP REST overhead isn't needed

---

## 11. XML-RPC

### What is XML-RPC?

**XML-RPC** is the predecessor to SOAP — a simple **RPC protocol** that uses **XML** to encode calls and **HTTP** as transport. It predates REST and is considered legacy today, but still powers some older systems.

```xml
-- XML-RPC Request --
POST /RPC2 HTTP/1.1
Host: api.example.com
Content-Type: text/xml

<?xml version="1.0"?>
<methodCall>
  <methodName>getUserById</methodName>
  <params>
    <param>
      <value><int>42</int></value>
    </param>
  </params>
</methodCall>

-- XML-RPC Response --
<?xml version="1.0"?>
<methodResponse>
  <params>
    <param>
      <value>
        <struct>
          <member>
            <name>name</name>
            <value><string>Alice Johnson</string></value>
          </member>
          <member>
            <name>email</name>
            <value><string>alice@example.com</string></value>
          </member>
        </struct>
      </value>
    </param>
  </params>
</methodResponse>
```

---

### When to Use XML-RPC
- Maintaining legacy WordPress/Blogger integrations (WordPress XML-RPC)
- Legacy enterprise system integrations
- When migrating from XML-RPC to modern APIs

---

## 12. API Gateway

### What is an API Gateway?

An **API Gateway** is a server that acts as the **single entry point** for all client requests. It sits in front of your services and handles cross-cutting concerns like authentication, rate limiting, logging, and routing.

![API Gateway Microservices](https://microservices.io/i/apigateway.jpg)
*API Gateway routes incoming requests to the appropriate microservice and aggregates responses*

---

### API Gateway Responsibilities

```
                         ┌────────────────────────────────────┐
                         │           API GATEWAY              │
Clients                  │                                    │
                         │  ┌──────────┐   ┌──────────────┐  │
Mobile  ──────────────►  │  │  Auth /  │   │    Rate      │  │
Browser ──────────────►  │  │  JWT     │   │   Limiter    │  │
IoT     ──────────────►  │  └──────────┘   └──────────────┘  │
                         │                                    │
                         │  ┌──────────┐   ┌──────────────┐  │
                         │  │ Request  │   │   Response   │  │
                         │  │ Router   │   │  Aggregator  │  │
                         │  └──────────┘   └──────────────┘  │
                         │                                    │
                         └────────────┬───────────────────────┘
                                      │
              ┌───────────────────────┼──────────────────────┐
              ▼                       ▼                      ▼
      ┌───────────────┐    ┌──────────────────┐   ┌──────────────────┐
      │  User Service │    │  Product Service │   │  Order Service   │
      │  :3001        │    │  :3002           │   │  :3003           │
      └───────────────┘    └──────────────────┘   └──────────────────┘
```

---

### API Gateway Features

| Feature | Description |
|---------|-------------|
| **Routing** | Direct requests to the right service |
| **Authentication** | Verify JWT, API keys, OAuth tokens |
| **Rate Limiting** | Prevent abuse (100 req/min per user) |
| **SSL Termination** | Handle HTTPS, pass plain HTTP internally |
| **Load Balancing** | Distribute traffic across instances |
| **Caching** | Cache responses to reduce backend load |
| **Logging & Monitoring** | Centralized observability |
| **Response Aggregation** | Combine multiple service responses |
| **Transformation** | Convert REST to gRPC, JSON to XML |

---

### Popular API Gateway Tools

| Tool | Type | Best For |
|------|------|---------|
| **AWS API Gateway** | Managed cloud | AWS-native microservices |
| **Kong** | Open source | Self-hosted, plugin ecosystem |
| **Nginx** | Proxy/Gateway | High performance, custom config |
| **Traefik** | Cloud-native | Kubernetes, auto-discovery |
| **Azure API Management** | Managed cloud | Azure ecosystem |

---

## 13. OpenAPI / Swagger

### What is OpenAPI?

**OpenAPI (formerly Swagger)** is a **specification standard** for describing REST APIs in a machine-readable YAML or JSON format. It enables automatic generation of documentation, client SDKs, and server stubs.

![Swagger UI](https://static1.smartbear.co/swagger/media/images/tools/opensource/swagger_ui.png)
*Swagger UI auto-generates interactive API documentation from an OpenAPI specification file*

---

### OpenAPI Specification Example

```yaml
openapi: 3.0.3
info:
  title: User Management API
  description: API for managing users
  version: 1.0.0
  contact:
    email: api@example.com

servers:
  - url: https://api.example.com/v1

security:
  - bearerAuth: []

paths:
  /users/{id}:
    get:
      summary: Get a user by ID
      operationId: getUserById
      tags: [Users]
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
            example: 42
      responses:
        '200':
          description: User found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          description: User not found
        '401':
          description: Unauthorized

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: integer
          example: 42
        name:
          type: string
          example: Alice Johnson
        email:
          type: string
          format: email
          example: alice@example.com
        role:
          type: string
          enum: [admin, user, viewer]

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
```

---

### OpenAPI Tooling Ecosystem

| Tool | Purpose |
|------|---------|
| **Swagger UI** | Auto-generate interactive HTML documentation |
| **Swagger Editor** | Write and validate OpenAPI specs online |
| **OpenAPI Generator** | Generate client SDKs in 50+ languages |
| **Redoc** | Alternative beautiful API documentation |
| **Stoplight** | API design platform using OpenAPI |
| **Postman** | Import OpenAPI spec to generate test collection |

---

## 14. Comparison Summary Table

| Feature | REST | GraphQL | SOAP | gRPC | WebSocket | Webhook | SSE |
|---------|------|---------|------|------|-----------|---------|-----|
| **Protocol** | HTTP | HTTP | HTTP/SMTP | HTTP/2 | TCP/WS | HTTP | HTTP |
| **Data Format** | JSON/XML | JSON | XML | Protobuf | Any | JSON/XML | Text |
| **Direction** | Req/Res | Req/Res | Req/Res | Both | Full-duplex | Push | Push |
| **Real-time** | ❌ | ❌ | ❌ | ✅ Stream | ✅ | ✅ Events | ✅ |
| **Typed Contract** | ❌ Optional | ✅ Schema | ✅ WSDL | ✅ Proto | ❌ | ❌ | ❌ |
| **Caching** | ✅ | ⚠️ Hard | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Browser Support** | ✅ | ✅ | ✅ | ⚠️ Limited | ✅ | ✅ | ✅ |
| **Learning Curve** | Low | Medium | High | Medium | Medium | Low | Low |
| **Performance** | Medium | Medium | Low | Very High | High | High | High |
| **Best For** | Public APIs | Complex data | Enterprise | Microservices | Live apps | Event triggers | Live feeds |

---

## 15. How to Choose the Right API

```
START
  │
  ▼
Is this real-time / live data?
  │
  ├─ YES → Is it bidirectional (both sides send data)?
  │           ├─ YES → WebSocket
  │           └─ NO  → Is it a discrete event (not a continuous stream)?
  │                       ├─ YES → Webhook
  │                       └─ NO  → SSE
  │
  └─ NO → Is this internal service-to-service?
              │
              ├─ YES → Is performance critical?
              │           ├─ YES → gRPC
              │           └─ NO  → REST or GraphQL
              │
              └─ NO → Is this a legacy or regulated enterprise system?
                          ├─ YES → SOAP
                          └─ NO  → Is the data complex with many relationships?
                                      ├─ YES → GraphQL
                                      └─ NO  → REST ✅
```

### Quick Reference

| Your Situation | Best API Choice |
|---------------|-----------------|
| Building a public web/mobile API | ✅ **REST** |
| Social network, CMS, complex queries | ✅ **GraphQL** |
| Banking, healthcare, enterprise legacy | ✅ **SOAP** |
| Internal microservices, high performance | ✅ **gRPC** |
| Chat, gaming, collaborative apps | ✅ **WebSocket** |
| Payment callbacks, CI/CD triggers | ✅ **Webhook** |
| Live dashboards, news feeds, notifications | ✅ **SSE** |
| Blockchain / crypto node calls | ✅ **JSON-RPC** |
| Need auto-generated docs + SDKs | ✅ **OpenAPI/Swagger** |
| Unified entry point for microservices | ✅ **API Gateway** |

---

## Key Takeaways

- **REST** is the default — simple, stateless, and universally understood
- **GraphQL** eliminates over/under-fetching for complex, relationship-heavy data
- **SOAP** provides the strongest formal contracts and security for enterprise use
- **gRPC** is the fastest option for internal high-throughput services
- **WebSocket** is the only option for true real-time bidirectional communication
- **Webhooks** are the most efficient way to react to third-party events
- **SSE** is the simplest solution for one-way server-to-client streaming
- **RPC/JSON-RPC** are natural for action-oriented (not resource-oriented) thinking
- **OpenAPI** and **API Gateways** are infrastructure concerns that improve every API type

---

*Guide covers: REST · GraphQL · SOAP · gRPC · WebSocket · Webhook · SSE · RPC · JSON-RPC · XML-RPC · API Gateway · OpenAPI*
*Last updated: April 2026*
