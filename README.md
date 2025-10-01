# Vakils AI Companion

An AI-powered document quality checking and review management system designed for regulatory compliance and professional document analysis.

## Overview

The Vakils AI Companion provides intelligent document analysis with human-in-the-loop review capabilities. The system uses local AI models for air-gapped environments and follows a modular, agent-based architecture.

## Features

- **AI-Powered Document Analysis**: Multiple specialized agents for different aspects of quality checking
- **Human-in-the-Loop Review**: Intelligent flagging with human decision preservation
- **Regulatory Compliance**: FDA compliance checking and regulatory requirement validation
- **Report Generation**: PDF reports and commented Word documents
- **Air-Gapped Support**: Local AI models with no external dependencies
- **Real-Time Interface**: React frontend with real-time pipeline status updates

## Architecture

### Backend (FastAPI + MCP Server)
- **Model Context Protocol (MCP)**: Standardized resource and tool access
- **Agent-Based Pipeline**: Specialized agents for different analysis types
- **Local AI Models**: TinyLlama integration for offline processing
- **Session Management**: Review session persistence and historical context

### Frontend (Next.js + React)
- **Real-Time Updates**: WebSocket communication with backend
- **Document Upload**: Drag-and-drop document processing
- **Review Interface**: Interactive review and approval workflow
- **Report Viewing**: Integrated PDF and document viewers

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker (optional)

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

### Frontend Setup
```bash
npm install
npm run dev
```

### Docker Deployment
```bash
docker-compose up --build
```

## Documentation

Comprehensive documentation is available in `/backend/docs/`:

- **[Architecture](backend/docs/ARCHITECTURE.md)** - System architecture and design patterns
- **[MCP Server](backend/docs/MCP_SERVER.md)** - Model Context Protocol implementation
- **[Testing](backend/docs/TESTING.md)** - Test suite documentation and guidelines
- **[Features](backend/docs/FEATURES.md)** - Detailed feature descriptions and capabilities

## Development

### Backend Development
The backend follows a modular architecture with:
- Agent-based document processing pipeline
- MCP server for standardized data access
- TypedDict-based state management
- Comprehensive test coverage

### Frontend Development
The frontend uses modern React patterns with:
- Server-side rendering with Next.js
- Real-time updates via WebSocket
- Tailwind CSS for styling
- Component-based architecture

### Testing
```bash
# Backend tests
cd backend && pytest tests/ -v

# Frontend tests
npm test
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Follow the established patterns (agents for backend, components for frontend)
4. Add comprehensive tests
5. Update documentation
6. Submit a pull request

## Technologies Used

- **Backend**: FastAPI, Python 3.11, TinyLlama, MCP Protocol
- **Frontend**: Next.js, React, TypeScript, Tailwind CSS
- **Testing**: pytest, Jest
- **Infrastructure**: Docker, uvicorn

## License

This project is licensed under the MIT License.
